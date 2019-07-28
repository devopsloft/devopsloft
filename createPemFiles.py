from OpenSSL import crypto
from socket import gethostname
import os

CERT_FILE = "web_s2i/cert.pem"
KEY_FILE = "web_s2i/key.pem"


def IsCertExist():
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        return True
    else:
        return False


def SelfSignedCertificate():
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "IL"
    cert.get_subject().ST = "Jerusalem"
    cert.get_subject().L = "Jerusalem"
    cert.get_subject().OU = "DevOps Loft"
    cert.get_subject().CN = gethostname()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    with open(CERT_FILE, "wb") as cert_f:
        cert_f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(KEY_FILE, "wb") as key_f:
        key_f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
