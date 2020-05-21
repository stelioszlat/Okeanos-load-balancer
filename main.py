#!/usr/bin/python
import threading as th
import time
import logging
import cluster as c
import paramiko

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

def f():
	logging.debug('thread function running')
	return

def hello():
	print("Hello, Timer")

def send_key(host, key):
	pass

def get_server_cpu(hostname):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.connect(hostname)
	stdin, stdout, stderr = client.exec_command('mpstat | tail -c 6')

	s = stdout.read()
	return str(100 - float(s) 

def send_key(hostname, key):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy()
	
if __name__=='__main__':
	#t = th.Timer(3.0, hello)
	#t.start()

	t1 = th.Timer(5, f)
	t1.setName('t1')
	t2 = th.Timer(5, f)
	t2.setName('t2')


	logging.debug('starting timers...')
	t1.start()
	t2.start()


	logging.debug('waiting before cancelling %s', t2.getName())
	time.sleep(2)
	logging.debug('canceling %s', t2.getName())
	print 'before cancel t2.is_alive() = ', t2.is_alive()
	t2.cancel()
	time.sleep(2)
	print 'after cancel t2.is_alive() = ', t2.is_alive()


	t1.join()
	t2.join()

	logging.debug('done')


def monitor():
	# run MONITOR_CLUSTER
	pass


if __name__=='__main__':
	pass
