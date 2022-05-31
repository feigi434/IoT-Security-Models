from itertools import count
from state import *
from certificate import publickey , privateKey
from global_data import state
import messages
from messages import Message
import time, os
import os.path


BEGIN = '-----BEGIN RSA PRIVATE KEY-----'
END = '-----END RSA PRIVATE KEY-----'

def find_master():
	print("Looking for the Master on the network...")
	counter = 2 # two tries for looking after master, if there is a stack in the network
	while(state.status != MASTER_FOUND):
		print("Trying for the #" + str(3-counter) + " time...")
		messages.broadcast(messages.IS_THERE_MASTER) # ask if there is master on the network
		time.sleep(15) # wait for master response (it takes a long time for the IoT to respond... ~10 seconds!)
		counter -= 1
		if(counter == 0 and state.status != MASTER_FOUND): # after 2 tries to find the master, set myself as Master
			messages.broadcast(messages.I_AM_MASTER)
			state.masterIP = state.myIP
			state.status =  MASTER_FOUND
			# feigi
			if not state.PUBLIC_KEY:
				state.public_key = publickey # The public key common to all home network devices
				state.CERTIFIED , lines = check_certificate()
				if (state.CERTIFIED == True and lines == 27):
					with open('certificate.txt', 'a') as wf:
						wf.write('\n'+publickey.decode("utf-8"))
					state.PUBLIC_KEY = True
					return True
			# /feigi

			print("No master is found! Setting myself as master")
			return True
	return False

def publishMe():
	print("Publishing my IP on the network...")
	messages.broadcast(messages.I_AM_ON_THE_NETWORK)

# feigi
def check_certificate():
	print("Looking for the Certificate...")
	if (os.path.exists( r'C:\Users\Feigi Zuzut\Documents\final project\IoT-Security-Models\certificate.txt')):
		with open('certificate.txt', 'r') as rf:
			lines = rf.readlines()
			if len(lines) == 36 :
				# if lines[0].find(BEGIN)!=-1 & lines[26].find(END)!=-1:
				print("CERTIFIED")###### change title
				return True, 36
			if  len(lines) == 27 :
				print("CERTIFIED")###### change title
				return True, 27
			else:
				print("not find certificate")
				return False
	else:
		print("not find certificate")
		return False


# /feigi