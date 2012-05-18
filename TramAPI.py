#!/usr/bin/python
# -*- coding: utf-8
import datetime
import simplejson, urllib, re

############ Functions #############
def datefromyarratrams(ytdate):
  m = re.search('/Date\(([0-9]*)\d{3}\+1000\)/', ytdate)
  ats = int(m.group(1))
  return datetime.datetime.fromtimestamp(ats)

def getnexttraminfo(stopid, route):
  baseurl = "http://extranetdev.yarratrams.com.au/pidsservicejson/Controller/GetNextPredictedRoutesCollection.aspx"
  url = baseurl + "?s=" + str(int(stopid)) + "&r=" + str(int(route))

  result = simplejson.load(urllib.urlopen(url))

  arrival = datefromyarratrams(result['responseObject'][0]['PredictedArrivalDateTime'])
  tram = result['responseObject'][0]['VehicleNo']

  return (arrival, tram)

def gettramarrivaltime(tramid):
  baseurl = "http://extranetdev.yarratrams.com.au/pidsservicejson/Controller/GetNextPredictedArrivalTimeAtStopsForTramNo.aspx"
  url = baseurl + "?t=" + str(int(tramid))

  result = simplejson.load(urllib.urlopen(url))
  predictions = result['responseObject']['NextPredictedStopsDetailsTable']

  ret = {}

  for predict in predictions:
    stop = predict['StopNo']
    ret[stop] = datefromyarratrams(predict['PredictedArrivalDateTime'])

  return ret

