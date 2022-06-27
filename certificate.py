#Creating a certificate confirming the reliability of the IoT device
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_asym_key(bits=2048):
	private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
	public_key = private_key.public_key()
	return public_key, private_key


public_key, private_key = generate_asym_key()


