# Required imports

import argparse
import random
import time

from pyhylight import *
import numpy as np
import time
import math

from pythonosc import dispatcher
from pythonosc import osc_server

def print_notes(unused_addr, args, notes):
  print("[{0}] ~ {1}".format(args[0], notes))


# Open ard serial port
ard.port = '/dev/ttyACM0' # Change this to your actual transmitter arduino serial port path
ard.open()

port = 32002
ip   = "127.0.0.1"

notes = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']


dispatcher = dispatcher.Dispatcher()
dispatcher.map("/notes", print_notes, "notes")

server = osc_server.ThreadingOSCUDPServer(
      (ip, port), dispatcher)

print("Serving on {}".format(server.server_address))
server.serve_forever()
