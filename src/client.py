from genericpath import exists
import certificate,state, messages
import time, os
import os.path
import shutil

from Crypto.PublicKey import RSA
from base64 import b64decode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from state import *
from global_data import state
# from pydoc import stripid


BEGIN = '-----BEGIN CERTIFICATE-----'
END = '-----END CERTIFICATE-----'

LOCATION = os.getcwd()

def find_master():
	print("Looking for the Master on the network...")
	counter = 2 # two tries for looking after master, if there is a stack in the network
	while(state.status != MASTER_FOUND):
		print("Trying for the #" + str(3-counter) + " time...")
		messages.broadcast(messages.IS_THERE_MASTER) # ask if there is master on the network
		time.sleep(15) # wait for master response (it takes a long time for the IoT to respond... ~10 seconds!)
		counter -= 1
		if not counter and state.status != MASTER_FOUND: # after 2 tries to find the master, set myself as Master
			messages.broadcast(messages.I_AM_MASTER)
			state.masterIP = state.myIP
			state.status = MASTER_FOUND
			# feigi
			if not state.public_key:
				state.public_key = certificate.public_key # The public key common to all home network devices
				state.CERTIFIED , lines = check_certificate()
				if state.CERTIFIED == True and lines == 19:
					with open('../encrypted_files/certificate.crt', 'a') as wf:
						wf.write(certificate.public_key.public_bytes(
							encoding=serialization.Encoding.PEM,
							format=serialization.PublicFormat.PKCS1
						).decode())
					state.PUBLIC_KEY = True
					return True
			# /feigi

			# feigi - checking
			# if not state.public_key:
			# 	state.public_key = certificate.public_key # The public key common to all home network devices
			# 	state.CERTIFIED , lines = check_certificate()
			# 	if state.CERTIFIED == True and lines == 19:
			# 		with open('../encrypted_files/certificate.crt', 'a') as wf:
			# 			try:
			# 				# pem = certificate.public_key.public_bytes(
			# 				# 	encoding=serialization.Encoding.PEM,
			# 				# 	format=serialization.PublicFormat.SubjectPublicKeyInfo
			# 				# )
			# 				publicKey = serialization.load_pem_public_key(
			# 						certificate.public_key.read(),
			# 						backend=default_backend()
			# 					)
			# 				print('*******************', publicKey)
			# 				# wf.write(f'\n{pem}')
			# 			except BaseException as ex:
			# 				print(ex)
			# 		return True
			# /feigi - checking

			print("No master is found! Setting myself as master")
			return True
	return False

def publishMe():
	print("Publishing my IP on the network...")
	messages.broadcast(messages.I_AM_ON_THE_NETWORK)

# Deleting an non-empty folder
def delete_dir(dir):
	path = os.path.join(LOCATION, dir)
	if exists(path):
		shutil.rmtree(path, ignore_errors=False)
		print(f"Deleted '{dir}' directory successfully")
		return True
	else:
		print(f"The directory : '{dir}' not exist")
		return False
# /feigi


# feigi
def check_certificate():
	print("Looking for the Certificate...")
	if (os.path.exists('../encrypted_files/certificate.crt')):
		with open('../encrypted_files/certificate.crt', 'r') as rf:
			lines = rf.readlines()
			if len(lines) == 36:
				# if lines[0].find(BEGIN)!=-1 and lines[26].find(END)!=-1:
				print("CERTIFIED")###### change title
				return True, 36
			if (BEGIN in lines[0]) and (END in lines[18]):
				print("----CERTIFIED----")###### change title
				return True, 19
		print("The certificate is unreliable")
		delete_dir('encrypted_files')
		return False
	else:
		print("not find certificate")
		return False
