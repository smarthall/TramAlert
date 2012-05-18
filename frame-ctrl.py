#!/usr/bin/env python

import os
import struct
import sys
import time
import usb.core
from usb.util import *

vendorId = 0x04e8
prodIdStore = 0x2033
prodIdDisp  = 0x2034

chunkSize = 0x4000
bufferSize = 0x20000

def paddedBytes(buf, size):
  diff = size - len(buf)
  return buf + bytes(b'\x00') * diff

def chunkyWrite(dev, buf):
  pos = 0
  while pos < bufferSize:
    dev.write(0x02, buf[pos:pos+chunkSize])
    pos += chunkSize

def writeImage(dev):
  if len(sys.argv) < 2 or sys.argv[1] == "-":
    content = sys.stdin.read()
  else:
    f = open(sys.argv[1])
    content = f.read()
    f.close()

  size = struct.pack('I', len(content))
  header = b'\xa5\x5a\x09\x04' + size + b'\x46\x00\x00\x00'

  content = header + content

  pos = 0
  while pos < len(content):
    buf = paddedBytes(content[pos:pos+bufferSize], bufferSize)
    chunkyWrite(dev, buf)
    pos += bufferSize

found = False

dev = usb.core.find(idVendor=vendorId, idProduct=prodIdStore)
if dev:
  try:
    dev.ctrl_transfer(CTRL_TYPE_STANDARD | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0xfe, 0xfe, 254)
  except usb.core.USBError as e:
    errorStr = str(e)
  time.sleep(1)

dev = usb.core.find(idVendor=vendorId, idProduct=prodIdDisp)
if dev:
  dev.set_configuration()
  result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x04, 0x00, 0x00, 1)
  writeImage(dev)
elif not dev:
  print "Device not found"

