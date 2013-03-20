# coding: utf-8
import sys
import os
import json
import cPickle as pickle
from weibo import APIClient
from feedback import Feedback
APP_KEY = '390980247' # app key
APP_SECRET = '63115ec635d078428bef7d47b6c0f500'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
# 生成认证链接
setting={}
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)

def load_setting():
	with open ('setting.pickle','wr') as f:
		setting = pickle.load(f)
def save_setting():
	with open ('setting.pickle','wr') as f:
		pickle.dump(setting,f)
def gen_oauth_url():
	url = client.get_authorize_url()
	fb = Feedback()
	fb.add_item(u'授权',subtitle=u'授权以后将url中code以后的参数填写到微博完成授权中',
		arg=url,icon='24.png')
	return fb

def get_mentions():
	with open ('setting.pickle','rb') as f:
		setting = pickle.load(f)
	client.set_access_token(setting['access_token'], setting['expires_in'])
	data=client.statuses.mentions.get()
	fb = Feedback()
	for x in data.statuses:
		fb.add_item(u'%s'%x.user.screen_name,
			subtitle=x.text,
			arg=str(x.user.id)+','+str(x.id),icon=u'24.png')
	return fb

def get_comments_to_me():
	with open ('setting.pickle','rb') as f:
		setting = pickle.load(f)
	client.set_access_token(setting['access_token'], setting['expires_in'])
	data=client.comments.to_me.get()
	fb = Feedback()
	for x in data.comments:
		fb.add_item(u'%s'%x.user.screen_name,
			subtitle=x.text,
			arg=str(x.user.id)+','+str(x.id),icon=u'24.png')
	return fb
def get_user_timeline():
	with open ('setting.pickle','rb') as f:
		setting = pickle.load(f)
	client.set_access_token(setting['access_token'], setting['expires_in'])
	data=client.statuses.home_timeline.get()
	fb = Feedback()
	for x in data.statuses:
		fb.add_item(u'%s'%x.user.screen_name,
			subtitle=x.text,
			arg=str(x.user.id)+','+str(x.id),icon=u'24.png')
	return fb
# 进行认证
def oauth_with_code(query):
	code=query
	r = client.request_access_token(code)
	access_token = r.access_token 
	expires_in = r.expires_in 
	setting['access_token']=access_token
	setting['expires_in']=expires_in
	client.set_access_token(access_token, expires_in)
	save_setting()
	fb = Feedback()
	fb.add_item(u'go ',subtitle=u'go to weibo ',
	arg=u'完成新浪微博授权',icon=u'24.png')
	return fb

# 发送微博
def send_weibo(query):
	with open ('setting.pickle','rb') as f:
		setting = pickle.load(f)
	client.set_access_token(setting['access_token'], setting['expires_in'])
	result=''
	try:
		client.statuses.update.post(status=query)
		result=u'发送成功'
	except:
		result=u'发送失败'	
	fb = Feedback()
	fb.add_item(u'发送微博',subtitle=u'发送微博信息',
	arg=result,icon=u'24.png')
	return fb
