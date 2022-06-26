from os.path import exists
import encryption


# function that save the key pool to encrypted file
def make_key_pool_file(pool_keys):
	file_exists = exists('./encrypted_files/pool_keys.txt')	
	if not file_exists:
		with open('./encrypted_files/pool_keys.txt', 'w') as wf:
			for key in pool_keys:
				wf.write("%s\n" % key)
		key = encryption.Fernet.generate_key()
		encryption.encrypting_file('./encrypted_files/pool_keys.txt', key)
		# encryption.decoding_file('./encrypted_files/pool_keys.txt', key)
		print('------pool_keys.txt------\n----The file was created successfully----')
		return True
	else:
		print('------pool_keys.txt------\n----The file exists----')
		return False

