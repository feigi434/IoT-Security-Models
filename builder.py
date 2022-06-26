from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import uuid
import os

one_day = datetime.timedelta(1, 0, 0)

def generate_asym_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

private_key, public_key = generate_asym_key()

builder = x509.CertificateBuilder()
builder = builder.subject_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'openstack-ansible Test CA'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'openstack-ansible'),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'Default CA Deployment'),
]))
builder = builder.issuer_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'openstack-ansible Test CA'),
]))
builder = builder.not_valid_before(datetime.datetime.today() - one_day)
builder = builder.not_valid_after(datetime.datetime(2025, 8, 2))
builder = builder.serial_number(int(uuid.uuid4()))
builder = builder.public_key(public_key)
builder = builder.add_extension(
    x509.BasicConstraints(ca=True, path_length=None), critical=True,
)
certificate = builder.sign(
    private_key=private_key, algorithm=hashes.SHA256(),
    backend=default_backend()
)


# with open("ca.key", "wb") as f:
#     f.write(private_key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.TraditionalOpenSSL,
#         encryption_algorithm=serialization.BestAvailableEncryption(b"openstack-ansible")
#     ))


def make_certificate():
    path = './encrypted_files'
    os.mkdir(path)
    with open('./encrypted_files/certificate.crt', 'wb') as f:
        f.write(certificate.public_bytes(
            encoding=serialization.Encoding.PEM,
        ))

def write_certificate_to_file():
    file_exist = os.path.exists('./encrypted_files/certificate.crt')
    if file_exist:
        make_certificate()
        print('Certificate successfully created')
    else:
        print('Existing Certificate')

make_certificate()



# pattern = '^0x0[0-9A-Z]'
# result = re.match(pattern, '0x07')

# if result:
#   print("Search successful.")
# else:
#   print("Search unsuccessful.")	
