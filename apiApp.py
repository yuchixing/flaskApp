#coding:utf-8

from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource

from flask.ext import admin
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.mongoengine import ModelView


app = Flask(__name__)
app.config['SECRET_KEY']='FWAPIAPP#$'
app.config['MONGODB_SETTINGS']={'DB':'testDB','HOST':'192.168.100.77','PORT':27017}

api = Api(app)

#input arg
#
parser = reqparse.RequestParser()
parser.add_argument('appName', type=str)
parser.add_argument('appToken', type=str)

def getRandomText():
	#oath2
	pass

def checkRandomText():
	pass


class Captcha(Resource):

	def get(self):
		self.post('get')

	def post(self,optName):
		print "optName===",optName
		if optName=='get':
			return {'a':'a'}
		elif optName=='check':
			print 'post==',dir(self)
			print parser.parse_args()
			return {'e':'e'}
		else:
			return {'code':-1,'msg':u'error message'}


api.add_resource(Captcha, '/<string:optName>')



#############################admin######################
db=MongoEngine()
db.init_app(app)

class  AppAdmin(db.Document):
	"""docstring for  AppAdmin"""
	def __init__(self, arg):
		super( AppAdmin, self).__init__()
		self.arg = arg
		

if __name__ == '__main__':
    app.run(debug=True)


