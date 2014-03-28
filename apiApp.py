#coding:utf-8

from flask import Flask,redirect,url_for,render_template
from flask.ext.restful import reqparse, abort, Api, Resource

from flask.ext import admin
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.mongoengine import ModelView

import auth

import json




app = Flask(__name__)
app.config['SECRET_KEY']='FWAPIAPP#$'
app.config['MONGODB_SETTINGS']={'DB':'testDB','HOST':'192.168.100.142','PORT':27017}

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
	parse_args

def checkRandomText():
	pass


class Captcha(Resource):

	def get(self):
		self.post('get')

	def post(self,optName):
		print "optName===",optName
		if optName=='get':
			import datetime
			paramDict=parser.parse_args()
			#save db
			now=datetime.datetime.utcnow()
			ca=CaptchaAdmin()
			ca.phone=paramDict['phoneNum']
			ca.phoneMessNum=getRandomText()
			ca.create_time=datetime2stamp(now)
			ca.save()

			#send message to phone
			return {'code':'1','stamp':ca.create_time}

		elif optName=='check':
			#check stamp and phoneNum
			paramDict=parser.parse_args()
			if paramDict['phoneNum'] and paramDict['stamp']:
				print dir(Captcha)
				#print Captcha.object.get({'phone':paramDict['phoneNum'],'create_time':paramDict['stamp']})
			return {'e':'e'}
		else:
			return {'code':-1,'msg':u'error message'}


api.add_resource(Captcha, '/<string:optName>')



###########################admin############

class APIAdminView(auth.AuthModelView):
	form_widget_args={
		'app_url':{'style':'width:500px;'},
		'app_description':{'rows':4,'style':'width:500px;'}
	}



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


