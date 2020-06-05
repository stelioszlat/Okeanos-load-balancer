#!/usr/bin/python
import threading as th
import time
import logging
import paramiko
import sys

logging.basicConfig(file='log', level=logging.DEBUG, format='(%(threadName)-9s) %(message)s')

client = paramiko.SSHClient()
client.load_system_host_keys()

def get_server_cpu(hostname):
	client.connect(hostname)
	stdin, stdout, stderr = client.exec_command('mpstat | tail -c 6')

	s = stdout.read()
	return str(100 - float(s))

def install_nginx(hostname):
	client.connect(hostname)
	stdin, stdout, stderr = client.exec_command('sudo apt-get install nginx nginx-extras')
	print(stdout.read())

def send_key(hostname, key):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy()

def ADD_NODE():
	print('adding node')
	return

def REMOVE_NODE():
	print('removing node')
	return

def TAKE_DECISION(load):
	high = 0.8
	low = 0.2

	if load > high:
		t1=th.Timer(1, ADD_NODE)
		t1.start()
		t1.join()
	elif load < low:
		t2=th.Timer(1, REMOVE_NODE)
		t2.setName('remove')
		t2.start()
		t2.join()

def MONITOR_CLUSTER():
	s1 = get_server_cpu('montesquieu')
	s2 = get_server_cpu('')

	m = float(s1) + float(s2) / 2

	print(s1)
	print(s2)

	t = TAKE_DECISION(m)

if __name__=='__main__':
	#t = th.Timer(3.0, hello)
	#t.start()
	#t.setName('name')

	install_nginx('montesquieu')

#	try:
#		m = th.Timer(0, MONITOR_CLUSTER)
#		m.start()
#		m.join()
#		while True:
#			m = th.Timer(5, MONITOR_CLUSTER)
#			m.start()
#			m.join()
#	except(KeyboardInterrupt):
#		sys.exit(1)
