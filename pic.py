#!/usr/bin/python
# -*- coding: utf-8
import Image, ImageFont, ImageDraw
import datetime
import simplejson, urllib, re

############ Functions #############
def getnexttraminfo(stopid, route):
  baseurl = "http://extranetdev.yarratrams.com.au/pidsservicejson/Controller/GetNextPredictedRoutesCollection.aspx"
  url = baseurl + "?s=" + str(int(stopid)) + "&r=" + str(int(route))

  result = simplejson.load(urllib.urlopen(url))

  astr = result['responseObject'][0]['PredictedArrivalDateTime']
  tram = result['responseObject'][0]['VehicleNo']
  m = re.search('/Date\(([0-9]*)\d{3}\+1000\)/', astr)
  ats = m.group(1)

  arrival = datetime.datetime.fromtimestamp(int(ats))

  return (arrival, tram)

def gettramarrivaltime(tramid):
  baseurl = "http://extranetdev.yarratrams.com.au/pidsservicejson/Controller/GetNextPredictedArrivalTimeAtStopsForTramNo.aspx"
  url = baseurl + "?t=" + str(int(tramid))

  result = simplejson.load(urllib.urlopen(url))
  predictions = result['responseObject']['NextPredictedStopsDetailsTable']
  
  ret = {}

  for predict in predictions:
    stop = predict['StopNo']
    m = re.search('/Date\(([0-9]*)\d{3}\+1000\)/', predict['PredictedArrivalDateTime'])
    ats = m.group(1)
    ret[stop] = datetime.datetime.fromtimestamp(int(ats))

  return ret

def predtext(draw, pos, date, font, colour):
  if date == None:
    text = "Unknown"
  else:
    text = date.strftime('%I:%M%p')

  draw.text(pos, text, font=font, fill=colour)

def buildimage(filename, citywaitm, arrkate, arrdan, boxwaitm, arrbox):
  # Load Fonts
  fntNorm = ImageFont.truetype( 'font/DejaVuSans.ttf', 24)
  fntSmall = ImageFont.truetype('font/DejaVuSans.ttf', 12)
  fntBold = ImageFont.truetype( 'font/DejaVuSans-Bold.ttf', 72)
  
  # Make some colours
  black = (0, 0, 0)
  white = (255, 255, 255)
  
  # Make a white image
  im = Image.open('yt-dog-default.png').convert('RGB')
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
(cityarr, citytram) = getnexttraminfo(homestopcity, tramline)
citydelta = cityarr - datetime.datetime.now()
citywaitm, citywaits = divmod(citydelta.total_seconds(), 60)

# Trams to Box Hill
(boxarr, boxtram) = getnexttraminfo(homestopbox, tramline)
boxdelta = boxarr - datetime.datetime.now()
boxwaitm, boxwaits = divmod(boxdelta.total_seconds(), 60)

# Get predictions for the next trams
citypred = gettramarrivaltime(citytram)
boxpred = gettramarrivaltime(boxtram)

# Get stop predictions
arrkate = citypred.get(katestop)
arrdan  = citypred.get(danstop)
arrbox  = boxpred.get(boxstop)

# Build the image
buildimage('/tmp/out.jpg', citywaitm, arrkate, arrdan, boxwaitm, arrbox)

