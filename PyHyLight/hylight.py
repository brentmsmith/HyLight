import numpy as np
from scipy.integrate import simps
from scipy.interpolate import InterpolatedUnivariateSpline as interp
from scipy.optimize import least_squares
import serial,time

ard = serial.Serial('/dev/cu.usbmodem1481',9600)
maryrgb = {'ab':(247,75,39), 'a':(255,130,155), 'bb':(254,123,13), 'b':(254,183,108), 'c':(255,213,0), 'db':(255,253,175), 'd':(132,255,182), 'eb':(1,50,252), 'e':(168,227,255), 'f':(225,160,255), 'gb':(224,215,255), 'g':(60,186,45)}
leds = np.genfromtxt('hylight_LED_spec.dat', dtype=np.float)
ledhues = np.array([310.7591383551636,256.9803013093145,166.34978775550982,139.8502577003946,111.97934945232399,68.0252777377368,50.80611051592259,45.39216459850199,42.398437976796835,7.108444833828318],dtype=np.float)
ledxyzs = np.array([[401.18038167,100.45272655,2325.33593184],[268.12057298,349.16061572,1952.2485356],[90.29998114,739.69145295,271.60012609],[254.91036914,815.20037745,36.91546091],[631.16507486,924.57265065,45.36602422],[128.983218,92.2200947,0.0136668813],[548.498231,267.216229,.00517271580],[97.2855913,44.2955072,0.000409439786],[159.322201,65.5637038,0.000118704440],[1.29825842,0.0502717880,0]],dtype=np.float)
cmf = np.genfromtxt('cie2006_2deg_xyz_cmf.dat',dtype=np.float,names='lam,x,y,z')
cmfx = interp(cmf['lam'],cmf['x'],ext=3)
cmfy = interp(cmf['lam'],cmf['y'],ext=3)
cmfz = interp(cmf['lam'],cmf['z'],ext=3)
XYZ2RGB = np.array([[0.4124564,0.3575761,0.1804375],[0.2126729,0.7151522,0.0721750],[0.0193339,0.1191920,0.9503041]]) #sRGB
d65dty = np.array([1.16032906e-1,1.39729247e-5,1.18129236e-1,4.82461989e-2,7.83347664e-2,1.00472835e-1,1.94122895e-1,1.06648045e-1,1.36764269e-1,1.01234875e-1])*0.035*4096 #Percent duty cycles normalized to sum of scales that minimize RMS from CIE D65 reference spectrum
d65XYZ = np.array([38806.58723704,40954.58091754,44049.35046552],dtype=np.float)
idxcor = [0,7,8,6,5,4,3,2,1,9]

def labf(t):
	'''
	Function used to calulate the Lightness in the L*a*b* color space from
	the relative luminance of XYZ values to reference white, in this case D65. 
	
	Args:
		t: float
			The relative luminance of an X, Y, or Z value

	Returns:
		output: float
			The functional output used for calculating L*a*b* values from the
			XYZ relative luminance values
	'''
	if t>216./24389.:
		return t**(1./3.)
	return ((24389./27.)*t+16.)/116.

def xyz2lab(xyz):
	'''
	Converts tristimulus XYZ values into CIE L*a*b* color space values.
	
	Args:
		xyz: array_like
			The XYZ value to be converted into L*a*b* values.

	Returns:
		lab: ndarray
			The CIE L*a*b* values calculated from the input XYZ values.	
	'''
	if np.sum(xyz)<3.04:
		xyz = xyz*100.
	fx = labf(xyz[0]/94.811)
	fy = labf(xyz[1]/100.)
	fz = labf(xyz[2]/107.304)
	l = 116.*fy -16.
	a = 500.*(fx-fy)
	b = 200.*(fy-fz)
	return np.array([l,a,b])

def lab2lch(lab):
	'''
	Converts CIE L*a*b* color space values to CIE LCh color space values
	
	Args:
		lab: array_like
			The CIELab value to be converted into sRGB values.

	Returns:
		lch: ndarray
			The LCh values calculated from the input L*a*b* values.	
	'''
	l = lab[0]
	c = np.sqrt(lab[1]**2+lab[2]**2)
	h = np.arctan2(lab[2],lab[1])*180./np.pi
	if h<0:
		h+=360.
	return np.array([l,c,h])

def calxyz(wave,inten,norm=True):
	'''
	Calculates the tristimulus XYZ values of an input spectrum using the
	CIE 2006 2-degree "spline-interpolated" color matching functions. 
	
	Args:
		wave: array_like
			The wavelength data of the spectrum in nanometer units
		inten: array_like
			The intensity of the spectrum per wavelength bin. Can be
			arbitrary spectral radiance units, e.g., W/sr/m**2/nm
		norm: bool
			If True, XYZ will be normalized to the sum of the three
			values. XYZ will not be normalized if False. 

	Returns:
		xyz: ndarray
			The XYZ values calculated from the input spectral data.	
	'''
	X = simps(cmfx(wave)*inten,x=wave)
	Y = simps(cmfy(wave)*inten,x=wave)
	Z = simps(cmfz(wave)*inten,x=wave)
	if np.sum([X,Y,Z])!=0:
		if norm:
			return np.array([X,Y,Z])/np.sum([X,Y,Z])
		return np.array([X,Y,Z])
	return np.array([0,0,0])

def xyz2rgb(xyz):
	'''
	Converts XYZ values to sRGB values using the CIE D65 standard 
	illuminant as reference white.
	
	Args:
		xyz: array_like
			The XYZ value to be converted into sRGB values.

	Returns:
		rgb: ndarray
			The sRGB values calculated from the input XYZ values.	
	'''
	xyz = np.asarray(xyz,dtype=np.float)
	rgb = np.matmul(np.linalg.inv(XYZ2RGB),xyz)
	idx=0
	while idx<3:
		if rgb[idx] <= 0.0031308:
			rgb[idx] *= 12.92
		else:
			rgb[idx] = 1.055*rgb[idx]**(1./2.4)-0.055
		idx+=1
	return rgb

def rgb2xyz(rgb):
	'''
	Converts RGB values to tristimulus XYZ values using the CIE D65 standard 
	illuminant as reference white, assuming the RGB values are sRGB.
	
	Args:
		rgb: array_like
			The RGB value to be converted into XYZ values.

	Returns:
		xyz: ndarray
			The XYZ values calculated from the input RGB values.	
	'''
	rgb = np.asarray(rgb,dtype=float)
	idx=0
	while idx<3:
		if rgb[idx] > 1.0:
			rgb[idx] /= 255.
		if rgb[idx] <= .04045:
			rgb[idx] /= 12.92
		else:
			rgb[idx] = ((rgb[idx]+.055)/1.055)**2.4
		idx+=1
	xyz = np.matmul(XYZ2RGB,rgb)
	return xyz

def calhue(rgb):
	'''
	Calculates the hue of the RGB value in HSV/HSL color space.
	
	Args:
		rgb: array_like
			The RGB value to be used to determine a hue.

	Returns:
		hue: float
			The hue of the RGB value in the HSV/HSL color space.	
	'''
	rgb = np.asarray(rgb,dtype=float)
	idx=0
	while idx<3:
		if rgb[idx] > 1.0:
			rgb[idx] /= 255.
		idx+=1
	rgbmax = np.argmax(rgb)
	rgbrange = np.amax(rgb)-np.amin(rgb)
	if rgbmax==0:
		hue = 60*(0+(rgb[1]-rgb[2])/rgbrange)
	elif rgbmax==1:
		hue = 60*(2+(rgb[2]-rgb[0])/rgbrange)
	elif rgbmax==2:
		hue = 60*(4+(rgb[0]-rgb[1])/rgbrange)
	elif (r==g==b) or (np.amax(rgb)==np.amin(rgb)):
		hue = 0
	if hue<0:
		hue+=360
	return hue

def rgb2hsv(rgb):
	'''
	Converts RGB values to HSV values.
	
	Args:
		rgb: array_like
			The RGB value to be converted into HSV values.

	Returns:
		hsl: ndarray
			The HSV values calculated from the input RGB values.	
	'''
	rgb = np.asarray(rgb,dtype=float)
	idx=0
	while idx<3:
		if rgb[idx] > 1.0:
			rgb[idx] /= 255.
		idx+=1
	h = calhue(rgb)
	rgbmax,rgbmin = np.amax(rgb),np.amin(rgb)
	if (r==g==b==0) or (rgbmax==0):
		s=0
	else:
		s = (rgbmax-rgbmin)/rgbmax
	return np.array([h,s,rgbmax])

def rgb2hsl(rgb):
	'''
	Converts RGB values to HSL values.
	
	Args:
		rgb: array_like
			The RGB value to be converted into HSV values.

	Returns:
		hsl: ndarray
			The HSL values calculated from the input RGB values.	
	'''
	rgb = np.asarray(rgb,dtype=float)
	idx=0
	while idx<3:
		if rgb[idx] > 1.0:
			rgb[idx] /= 255.
		idx+=1
	h = calhue(r,g,b)
	rgbmax,rgbmin = np.amax(rgb),np.amin(rgb)
	if ((r==g==b==0) or (rgbmax==0)) or ((r==g==b==1) or (rgbmin==1)):
		s=0
	else:
		s=(rgbmax-rgbmin)/(1-np.abs(rgbmax+rgbmin-1))
	return np.array([h,s,(rgbmax+rgbmin)/2])

def hylrgb(rgb):
	'''
	Converts RGB values to PWM values to be sent to the HyLight board.
	
	Args:
		rgb: array_like
			The RGB value to be converted into PWM values

	Returns:
		pwm: ndarray
			The PWM values to be sent to the HyLight board.
	'''
	rgb = np.asarray(rgb,dtype=float)
	idx=0
	while idx<3:
		if rgb[idx] > 1.0:
			rgb[idx] /= 255.
		if rgb[idx] <= .04045:
			rgb[idx] /= 12.92
		else:
			rgb[idx] = ((rgb[idx]+.055)/1.055)**2.4
		idx+=1
	XYZ = np.matmul(XYZ2RGB,rgb)*d65XYZ
	hue = lab2lch(xyz2lab(rgb2xyz(rgb)))[2]
	led1 = np.argmin(np.abs(hue-ledhues))
	if hue<ledhues[led1]:
		led2=np.argmin(np.abs(ledhues-np.amax(ledhues[(ledhues<hue) & (ledhues!=led1)])))
	else:
		if hue>ledhues[0]:
			led2 = 9
		else:
			led2=np.argmin(np.abs(ledhues-np.amin(ledhues[(ledhues>hue) & (ledhues!=led1)])))
	led1xyz = calxyz(leds[:,0],leds[:,led1+1],norm=False)
	led2xyz = calxyz(leds[:,0],leds[:,led2+1],norm=False)
	M = np.array([[ledxyzs[led2][0],ledxyzs[led1][0],d65XYZ[0]],[ledxyzs[led2][1],ledxyzs[led1][1],d65XYZ[1]],[ledxyzs[led2][2],ledxyzs[led1][2],d65XYZ[2]]])
	vpwm = np.matmul(np.linalg.inv(M),XYZ)
	pwm = vpwm[2]*d65dty
	pwm[led2] += vpwm[0]
	pwm[led1] += vpwm[1]
	pwm[pwm<0]=0
	return pwm.astype(int)
	
class DangerPWM(Exception):
	'''PWM value is too large, may damage they LED board!'''
	pass
	
class MissingVals(Exception):
	'''List of PWMs to be sent must contain exactly 10 elements'''
	pass
	
def send(addr,pwms,power=1.):
	'''
	Sends an array of PWM values to a designated receiver. The PWM values
	can be scaled using the power argument. 
	
	Args:
		addr: int
			The address of the receiver to be transmitted to. A value of 0
			will transmit to "SciHub HyLighter Receiver #01", a value of 1
			will transmit to "SciHub HyLighter Receiver #02", and so on ...
		pwms: array_like
			An array of 10 PWM values to be transmitted to the designated
			receiver. The 10 PWM values will be set on the HyLight board
			connected to the receiver. 
		power: float
			A scale factor for the PWM values for scaling the brightness of
			all LEDs uniformly by the same constant.			

	Returns:
		None
	'''
	if np.any(pwms[0:8]>4096*.5):
		raise DangerPWM
	if pwms.size!=10:
		raise MissingVals
	pwms = pwms[idxcor].astype(int)
	command = str(addr)+' '
	for pwm in pwms:
		command+=str(pwm)+' '
	ard.write(command.encode())

#This short for-loop shows how one could cycle through Mary's synesthesia using the HyLight board
for note in ['ab','a','bb','b','c','db','d','eb','e','f','gb','g']:
	send(0,hylrgb(maryrgb[note]),power=1)
	time.sleep(1.)