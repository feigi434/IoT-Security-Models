from os.path import exists
from cryptography.fernet import Fernet
from state import *
import state


# function that encrypting file
def encrypting_file(file, key):
	print('encrypting_file', file , key)
	with open('mykey.key', 'wb') as mykey:
		mykey.write(key)
	print('11111111111111')
	with open('mykey.key', 'rb') as mykey:
		key = mykey.read()
	print(key)
	f = Fernet(key)
	with open(file, 'rb') as original_file:
		original = original_file.read()
	encrypted = f.encrypt(original)
	with open('enc_'+file, 'wb') as encrypted_file:
		encrypted_file.write(encrypted)
	return True
	

def decoding_file(file, key):
	print('decoding_file', file , key)

	f = Fernet(key)
	with open('enc_'+file, 'rb') as encrypted_file:
		encrypted = encrypted_file.read()
	decrypted = f.decrypt(encrypted)
	with open('dec_'+file, 'wb') as decrypted_file:
		decrypted_file.write(decrypted)
	return True


# function that save the key pool to encrypted file
def make_key_pool_file(pool_keys):
	file_exists = exists('./pool_keys.txt')	
	if not file_exists:
		with open('pool_keys.txt', 'w') as wf:
			for key in pool_keys:
				wf.write("%s\n" % key)
		key = Fernet.generate_key()
		encrypting_file('pool_keys.txt', key)
		decoding_file('pool_keys.txt', key)
		return True
	else:
		print('------pool_keys.txt------\n----The file exists----')
		return False

