#Creating a certificate confirming the reliability of the IoT device
from Crypto.PublicKey import RSA


def generate_asym_key(bits=2048):
	# default exponent is: 65537 (0x10001)
	new_key = RSA.generate(bits)
	public_key = new_key.publickey().exportKey("PEM")
	private_key = new_key.exportKey("PEM")
	return public_key, private_key


publickey, privateKey = generate_asym_key()


