#coding:utf-8

from flask import Flask,redirect,url_for,render_template,jsonify
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.restful.representations.json import output_json
from flask.ext import admin
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.mongoengine import ModelView

import auth

import json




app = Flask(__name__)
app.config['SECRET_KEY']='FWAPIAPP#$'
app.config['MONGODB_SETTINGS']={'DB':'testDB','HOST':'192.168.100.115','PORT':27017}

api = Api(app)


#############################db-Model######################
db=MongoEngine()
db.init_app(app)

class  AppAdmin(db.Document):
	"""docstring for  AppAdmin"""
	name=db.StringField(max_length=20)
	appToken=db.StringField(max_length=60)

	def __unicode__(self):
		return self.name
		
class CaptchaAdmin(db.Document):
	phone=db.StringField(max_length=11)
	phoneMessNum=db.StringField(max_length=4)
	#create_time=db.DateTimeField()
	create_time=db.IntField()
	status=db.IntField(default=1)

	def __unicode__(self):
		return self.phone

#input arg
#
parser = reqparse.RequestParser()
parser.add_argument('appName', type=str)
parser.add_argument('appToken', type=str)

parser.add_argument('phoneNum', type=str)
parser.add_argument('stamp', type=str)
def getRandomText():
	import random
	num="0123456789"
	phoneNum=''.join(random.sample(num,4))
	return phoneNum

def datetime2stamp(utcnow):
	import time
	stamp=int(time.mktime(utcnow.utctimetuple()))
	return stamp


def stamp2datetime(stamp):
	pass

def checkRandomText():
	pass

def checkPhoneNum():
	pass

class Captcha(Resource):

	# def get(self):
	# 	self.post('get')

	def post(self,optName):
		print "optName===",optName
		if optName=='get':
			import datetime
			paramDict=parser.parse_args()

			#save db
			now=datetime.datetime.utcnow()
			try:
				cap=CaptchaAdmin.objects.filter(phone=paramDict['phoneNum'])
				if cap.count()>0:
					ca=cap[0]
					now_stamp=datetime2stamp(now)
					num=now_stamp-ca.create_time
					if num<60:
						return output_json({'code':-2,'msg':'wait for 60s'},409)
				else:
					ca=CaptchaAdmin()
				ca.phone=paramDict['phoneNum']
				ca.phoneMessNum=getRandomText()
				ca.create_time=datetime2stamp(now)
				ca.save()
				#send message to phone
				
				return output_json({'code':1,'stamp':ca.create_time},200)
			except Exception, e:
				#import traceback;traceback.print_exc()
				return output_json({'code':-1,'msg':'error'},410)


		elif optName=='check':
			#check stamp and phoneNum
			paramDict=parser.parse_args()
			if paramDict['phoneNum'] and paramDict['stamp'] and paramDict['phone']:
				#print dir(CaptchaAdmin.objects)
				try:
					ca=CaptchaAdmin.objects.get(phoneMessNum=paramDict['phoneNum'],phone=paramDict['phone'],create_time=paramDict['stamp'],status=1)
					print ca ,dir(ca)
					ca.status=0
					ca.save()
					return output_json({'code':1,'msg':'ok'},201)
				except:
					return output_json({'code':-1,'msg':u'please request again!'},411)

			return output_json({'code':-1,'msg':u'please request again!'},303)
		else:
			return output_json({'code':-1,'msg':u'error message'},500)


api.add_resource(Captcha, '/<string:optName>')



###########################admin############

class APIAdminView(auth.AuthModelView):
	pass


@app.route('/')
@auth.requires_auth
def index():
	return render_template('index.html')
	#return redirect(url_for('apiadminview.admin'))


if __name__ == '__main__':
	admin=admin.Admin(app,u'API')
	admin.add_view(APIAdminView(AppAdmin,name=u'app'))
	admin.add_view(APIAdminView(CaptchaAdmin,name=u'captcha'))
	app.run(debug=True)


