# coding: utf-8
UPDATE_URL='http://xiangzuoxiangyou-hello.stor.sinaapp.com/update/v.txt'
UPDATE_BASE='http://xiangzuoxiangyou-hello.stor.sinaapp.com/%s/%s'
import urllib

import os
from urllib2 import urlopen, URLError, HTTPError
from feedback import Feedback

def dl_version():
	try:
		f = urlopen(UPDATE_URL)
		lines=f.readlines()
		V=''
		for x in lines:
			if '.' not in x:
				V=x.replace('\n','')
			else:
				dlfile(V,x)
		fb = Feedback()
		fb.add_item(u'更新插件',subtitle=u'开始更新',
		arg=u'完成新浪微博插件更新',icon=u'24.png')
		return fb
	except Exception,e:
		fb = Feedback()
		fb.add_item(u'更新插件',subtitle=u'开始更新',
		arg=u'更新失败',icon=u'24.png')
		return fb
def dlfile(v,filename):
	# Open the url
	url=UPDATE_BASE%(v,filename)
	f = urlopen(url)
	# Open our local file for writing
	with open(filename, "wb") as local_file:
		local_file.write(f.read())
