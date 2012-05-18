#!/usr/bin/python
# -*- coding: utf-8
import Image, ImageFont, ImageDraw
import datetime
import ThemeResolver, TramAPI

############ Functions #############
def predtext(draw, pos, date, font, colour):
  if date == None:
    text = "Unknown"
  else:
    text = date.strftime('%I:%M%p')

  draw.text(pos, text, font=font, fill=colour)

def buildimage(filename, citywaitm, arrkate, arrdan, boxwaitm, arrbox):
  # Load Fonts
  fntNorm =  ThemeResolver.ttruetype('font/DejaVuSans.ttf', 24)
  fntSmall = ThemeResolver.ttruetype('font/DejaVuSans.ttf', 12)
  fntBold =  ThemeResolver.ttruetype('font/DejaVuSans-Bold.ttf', 72)
  
  # Make some colours
  black = (0, 0, 0)
  white = (255, 255, 255)
  
  # Make a white image
  im = ThemeResolver.timage('morning-tramback.png').convert('RGB')
  draw = ImageDraw.Draw(im)
  
  # Static stuff
  draw.text((20, 5), 'tramTRACKER', font=fntBold, fill=black)
  
  # Times to city
  draw.text((20, 140), 'To City: ' + str(int(citywaitm)) + ' minutes', font=fntNorm, fill=black)
  draw.text((20, 180), 'Arrives at Kate\'s work:', font=fntNorm, fill=black)
  draw.text((20, 210), 'Arrives at Dan\'s work:', font=fntNorm, fill=black)
  
  predtext(draw, (300, 180), arrkate, fntNorm, black)
  predtext(draw, (300, 210), arrdan,  fntNorm, black)
  
  # Times to Box Hill
  draw.text((20, 260), 'To Box Hill: ' + str(int(boxwaitm)) + ' minutes', font=fntNorm, fill=black)
  draw.text((20, 300), 'Arrives at Box Hill:', font=fntNorm, fill=black)

  predtext(draw, (300, 300), arrbox,  fntNorm, black)
  
  # Last updated
  draw.text((20, 460), 'Last Updated: ' + datetime.datetime.now().strftime('%l:%M:%S%p'), font=fntSmall, fill=white)
  
  # Save
  im.save(filename, 'JPEG', quality=100)

############## Fetch Code ##################
# API Information
tramline     = 109
homestopcity = 1749 # Northcote Road to City
homestopbox  = 2749 # Northcote Road to Box Hill
katestop     = 3508 # 101 Collins Street to City
danstop      = 1725 # River Blvd to City
boxstop      = 2757 # Box Hill to Box Hill

# Trams to city
(cityarr, citytram) = TramAPI.getnexttraminfo(homestopcity, tramline)
citydelta = cityarr - datetime.datetime.now()
citywaitm, citywaits = divmod(citydelta.total_seconds(), 60)

# Trams to Box Hill
(boxarr, boxtram) = TramAPI.getnexttraminfo(homestopbox, tramline)
boxdelta = boxarr - datetime.datetime.now()
boxwaitm, boxwaits = divmod(boxdelta.total_seconds(), 60)

# Get predictions for the next trams
arrdan = None
arrkate = None
arrbox = None
if not citytram <= 0:
  citypred = TramAPI.gettramarrivaltime(citytram)
  arrkate = citypred.get(katestop)
  arrdan  = citypred.get(danstop)
if not citytram <= 0:
  boxpred = TramAPI.gettramarrivaltime(boxtram)
  arrbox  = boxpred.get(boxstop)

# Build the image
buildimage('/tmp/out.jpg', citywaitm, arrkate, arrdan, boxwaitm, arrbox)

