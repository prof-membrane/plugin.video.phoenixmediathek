# -*- coding: utf-8 -*-
import libMediathek
import xbmc
import xbmcplugin
import xbmcgui
import json
import _utils
import mediathekxmlservice as xmlservice

baseUrl = 'http://phoenix.de/php/appinterface/appdata.php'

def main():
	response = _utils.getUrl(baseUrl + '?c=videorubriken')
	j = json.loads(response)
	l = []
	for result in j['results']:
		d = {}
		d['name'] = result['name']
		d['url'] = baseUrl + '?c=videos&rub=' + str(result['id'])
		d['mode'] = 'list'
		d['type'] = 'dir'
		l.append(d)
	libMediathek.addEntries(l)
	
def list():
	response = _utils.getUrl(params['url'])
	j = json.loads(response)
	l = []
	for video in j['videos']:
		d = {}
		d['name'] = video['title']
		d['epoch'] = video['datesec']
		d['thumb'] = video['image_ipad'][:-10] + str(int(video['image_ipad'][-10:-4]) - 1) + video['image_ipad'][-4:]
		d['url'] = 'http://www.phoenix.de/php/mediaplayer/data/beitrags_details.php?ak=web&id=' + str(video['id'])
		d['mode'] = 'play'
		d['type'] = 'video'
		l.append(d)
		
	libMediathek.addEntries(l)
	
def play():
	videoUrl,subUrl,offset = xmlservice.getVideoUrl(params['url'])
	listitem = xbmcgui.ListItem(path=videoUrl)
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)


modes = {
'main': main,
'list': list,
'play': play
}	
def list():	
	global params
	params = libMediathek.get_params()
	global pluginhandle
	pluginhandle = int(sys.argv[1])
	
	if not params.has_key('mode'):
		main()
	else:
		modes.get(params['mode'],main)()
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
list()