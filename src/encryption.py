from cryptography.fernet import Fernet

# function that encrypting file
def encrypting_file(file, key):
	print('encrypting file '+file)
	with open('../encrypted_files/encrypt.key', 'wb') as encrypt_key:
		encrypt_key.write(key)
	with open('../encrypted_files/encrypt.key', 'rb') as encrypt_key:
		key = encrypt_key.read()
	f = Fernet(key)
	with open(file, 'rb') as original_file:
		original = original_file.read()
	encrypted = f.encrypt(original)
	with open('../encrypted_files/enc_'+file, 'wb') as encrypted_file:
		encrypted_file.write(encrypted)
	return True

# function that decoding file
def decoding_file(file, key):
	print('decoding file '+file)
	f = Fernet(key)
	with open('../encrypted_files/enc_'+file, 'rb') as encrypted_file:
		encrypted = encrypted_file.read()
	decrypted = f.decrypt(encrypted)
	with open('../encrypted_files/dec_'+file, 'wb') as decrypted_file:
		decrypted_file.write(decrypted)
	return True