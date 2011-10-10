#!/usr/bin/python

# From: http://www.saltycrane.com/blog/2008/10/installing-beanstalkd-and-pybeanstalk-ubuntu/

import logging
import datetime
import os
import sys
import configobj
import json

from beanstalk import serverconn
from beanstalk import job

KEYDIR = '/home/donny/gitosis-admin/keydir/'
GTSCONF = '/home/donny/gitosis-admin/gitosis.conf'

# Setup connection.
connection = serverconn.ServerConn('127.0.0.1', 9000)
connection.job = job.Job

# Setup logging.
logging.basicConfig(filename='worq_gitosis.log',level=logging.INFO)

print 'Listening...'

# Consume data
while True:
	j = connection.reserve()

	data = str(j.data).replace("'", '"')

	logging.info(str(datetime.datetime.now()) + ' ' + data)

	data = json.loads(data)

	action = data['action']

	if data.has_key('username'):
		user = data['username']
	if data.has_key('appname'):
		app = data['appname']
	if data.has_key('publickey'):
		key = data['publickey']

	# Perform the change_public_key action
	if action == 'change_public_key':
		pk_file = open(KEYDIR + '%s.pub' % user, 'w')
		pk_file.write(key)
		pk_file.close()

		gc_file = configobj.ConfigObj(GTSCONF)

		section = 'group ' + user

		if gc_file.has_key(section):
			pass
		else:
			gc_file[section] = {}
			gc_file[section]['members'] = user

		gc_file.write()
		commit_msg = 'CK ' + user

	# Perform the create_application action
	elif action == 'create_application':
		gc_file = configobj.ConfigObj(GTSCONF)

		section = 'group ' + user

		if gc_file.has_key(section):
			if gc_file[section].has_key('writable'):
				gc_file[section]['writable'] += ' ' + app
			else:
				gc_file[section]['writable'] = app
		else:
			gc_file[section] = {}
			gc_file[section]['members'] = user
			gc_file[section]['writable'] = app

		gc_file.write()
		commit_msg = 'CA %s %s' % (user, app)

		host = data['host']
		port = data['port']

		f = open('/home/donny/apps-info/' + app, 'w')
		f.write(host + ':' + port + '\n')
		f.close()

	# Perform the destroy_application action
	elif action == 'destroy_application':
		gc_file = configobj.ConfigObj(GTSCONF)

		section = 'group ' + user

		if gc_file.has_key(section):
			if gc_file[section].has_key('writable'):
				writable = gc_file[section]['writable']
				writable = writable.split(' ')
				del(writable[writable.index(app)])
				if len(writable) >= 1:
					gc_file[section]['writable'] = ' '.join(writable)
				else:
					del(gc_file[section]['writable'])
			else:
				pass
		else:
			pass

		gc_file.write()
		commit_msg = 'DA %s %s' % (user, app)

	else:
		logging.info(str(datetime.datetime.now()) + ' ' + 'ERROR')


	popen_result = os.popen('cd /home/donny/gitosis-admin ; git add . ; git commit -a -m "%s" ; git push' % commit_msg)


	j.Finish()

