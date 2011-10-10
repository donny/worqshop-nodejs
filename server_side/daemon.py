#!/usr/bin/python

import os
import sys
import subprocess
import signal

cmd = sys.argv[1]
app = sys.argv[2]

APPS_DIR = '/home/ec2-user/apps/'
NODE_EXE = '/home/ec2-user/local/bin/node'

app_pid = APPS_DIR + app + '.pid'
app_pid_exist = os.path.isfile(app_pid)

# start
if cmd == 'start':
	if not app_pid_exist:
		proc = subprocess.Popen([NODE_EXE, APPS_DIR + app + '/main.js'])
		f = open(app_pid, 'w')
		f.write(str(proc.pid))
		f.close()

# stop
elif cmd == 'stop':
	if app_pid_exist:
		f = open(app_pid, 'r')
		pid = f.readline()
		os.kill(int(pid), signal.SIGKILL)
		f.close()
		os.unlink(app_pid)

# restart
elif cmd == 'restart':
	if app_pid_exist:
		f = open(app_pid, 'r')
		pid = f.readline()
		os.kill(int(pid), signal.SIGKILL)
		f.close()
		os.unlink(app_pid)

	proc = subprocess.Popen([NODE_EXE, APPS_DIR + app + '/main.js'])
	f = open(app_pid, 'w')
	f.write(str(proc.pid))
	f.close()
