#Creating a certificate confirming the reliability of the IoT device

from Crypto.PublicKey import RSA
from os.path import exists
from state import *
from global_data import state
import builder


def generate_asym_key(bits=2048):
	# default exponent is: 65537 (0x10001)
	new_key = RSA.generate(bits)
	public_key = new_key.publickey().exportKey("PEM")
	private_key = new_key.exportKey("PEM")
	return public_key, private_key


publickey, privateKey = generate_asym_key()

def write_certificate_to_file():
	file_exists = exists('./certificate.crt')	
	if not file_exists:
		# with open('certificate.txt', 'w') as wf:
		# 	wf.write(privateKey.decode("utf-8"))
		builder.make_certificate()
		return True
	else:
		print('Existing Certificate')


# function that save the key pool to encrypted file
def key_pool_file(pool_keys):
	file_exists = exists('./key_pool.crt')	
	if not file_exists:
		with open('pool_keys.crt', 'w') as wf:
			for key in pool_keys:
				wf.write("%s\n" % key)
			return True
	else:
		print('The file exists')
		return False
