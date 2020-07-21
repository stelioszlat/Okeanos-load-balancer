#!/usr/bin/python
import threading as th
import subprocess as sb
import time
import logging
import paramiko
import sys
from configure_cluster import *
from configure_nginx import *
from datetime import datetime

client = paramiko.SSHClient()
client.load_system_host_keys()

removed = True
def get_server_cpu(hostname):
	client.connect(hostname)
	stdin, stdout, stderr = client.exec_command('mpstat | tail -c 6')

	s = stdout.read()
	return 100 - float(s)


def install_nginx(hostname):
	client.connect(hostname)
	stdin, stdout, stderr = client.exec_command('sudo apt-get install nginx nginx-extras')
	#print(stdout.read())


def send_key(hostname, key):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy()


def ADD_NODE(host, file):
	print('adding node')
	CONFIGURE_CLUSTER_ADD(host, file)
	sb.call(['sudo', 'nginx', '-s', 'reload'])
	return


def REMOVE_NODE(host, file):
	print('removing node')
	CONFIGURE_CLUSTER_REMOVE(host, file)
	sb.call(['sudo', 'nginx', '-s', 'reload'])
	return


def TAKE_DECISION(load):
	high = 80
	low = 20

	global removed

	if load > high:
		if removed:
			ADD_NODE('rousseau:8080', '/etc/nginx/nginx.conf')
			removed = False
	elif load < low:
		if not removed:
			REMOVE_NODE('rousseau:8080', '/etc/nginx/nginx.conf')
			removed = True

def MONITOR_CLUSTER():
	s1 = get_server_cpu('montesquieu')
	s2 = get_server_cpu('rousseau')
	print(datetime.now().strftime("\n\nTime: %H:%M:%S"))
	print('Server1 load: '+str(s1)+ '\nServer2 load: ' + str(s2))

	global removed

	if removed:
		m = s1
	else:
		m = s1 + s2 / 2

	print('\nCluster average load: ' + str(m))
	t = TAKE_DECISION(m)

def CREATE_LOAD():
	sb.call(['wrk', '-t4', '-c10000', '-d1m', 'http://localhost:8080'])

def join_wrk(c):
	c.join()

if __name__=='__main__':

	for i in range(10):
		print('=========================================================================')
		print('ITERATION' + str(i))
		c = th.Thread(target=CREATE_LOAD)
		c.start()
		while True:
			m = th.Timer(2, MONITOR_CLUSTER)
			m.start()
			m.join()

			a = th.Thread(target=join_wrk, args=[c])
			a.start()
			if not a.is_alive():
				break
