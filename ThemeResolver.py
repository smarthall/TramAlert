import os
import ImageFont, Image

def timage(filename):
  return Image.open(tfile(filename))

def ttruetype(filename, size):
  return ImageFont.truetype(tfile(filename), size)

def tfile(filename):
  paths = [ 'themes/fancy/' + filename,
            'themes/default/' + filename ]

  for p in paths:
    if os.path.exists(p):
      return p

