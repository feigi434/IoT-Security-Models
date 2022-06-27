from pydoc import stripid
from state import *
from global_data import state

import certificate
import messages
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
				state.public_key = certificate.public_key # The public key common to all home network devices
				state.CERTIFIED , lines = check_certificate()
				if (state.CERTIFIED == True and lines == 27):
					with open('./encrypted_files/certificate.crt', 'a') as wf:
						wf.write('\n'+certificate.public_key.decode("utf-8"))
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
	if (os.path.exists('./encrypted_files/certificate.crt')):
		with open('./encrypted_files/certificate.crt', 'r') as rf:
			lines = rf.readlines()
			print('*****************lines[0]', BEGIN in lines[0])
			if len(lines) == 36:
				# if lines[0].find(BEGIN)!=-1 & lines[26].find(END)!=-1:
				print("CERTIFIED")###### change title
				return True, 36
			if len(lines) == 19:
				print("CERTIFIED")###### change title
				return True, 19
			else:
				print("The certificate is unreliable")
				return False
	else:
		print("not find certificate")
		return False


# /feigi