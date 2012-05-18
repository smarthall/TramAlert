#!/usr/bin/env python

import os
import struct
import sys
import time
import usb.core
from usb.util import *

class PhotoFrame:
  vendorId = 0x04e8
  prodIdStore = 0x2033
  prodIdDisp  = 0x2034

  chunkSize = 0x4000
  bufferSize = 0x20000

  def __init__(self):
    # Look for a frame in storage mode, and set to display mode
    dev = usb.core.find(idVendor=self.vendorId, idProduct=self.prodIdStore)
    if dev:
      try:
        dev.ctrl_transfer(CTRL_TYPE_STANDARD | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0xfe, 0xfe, 254)
      except usb.core.USBError as e:
        errorStr = str(e)
      time.sleep(1)

    # Look for a frame in display mode
    dev = usb.core.find(idVendor=self.vendorId, idProduct=self.prodIdDisp)
    if dev:
      dev.set_configuration()
      result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x04, 0x00, 0x00, 1)
    else:
      raise "Device not found"

    # Save the USB device
    self.dev = dev

  def chunkyWrite(self, buf):
    pos = 0
    while pos < len(buf):
      self.dev.write(0x02, buf[pos:pos + self.chunkSize])
      pos += self.chunkSize

  def writeImage(self, content):
    size = struct.pack('I', len(content))
    header = b'\xa5\x5a\x09\x04' + size + b'\x46\x00\x00\x00'

    content = header + content

    pos = 0
    while pos < len(content):
      chunk = content[pos:pos + self.bufferSize]
      diff = size - len(chunk)
      chunk += bytes(b'\x00') * diff
      self.chunkyWrite(chunk)
      pos += self.bufferSize


##### Script #####
if len(sys.argv) < 2 or sys.argv[1] == "-":
  content = sys.stdin.read()
else:
  f = open(sys.argv[1])
  content = f.read()
  f.close()

frame = PhotoFrame()
frame.writeImage(content)



