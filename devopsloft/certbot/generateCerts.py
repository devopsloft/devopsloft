#!/usr/bin/env python3
import os
from socket import gethostname

import click
from OpenSSL import crypto


@ click.command()
@ click.option("-s", "--server_name", required=False, default="localhost")
def SelfSignedCertificate(server_name):
    CERT_FILE = "/etc/letsencrypt/live/{0}/fullchain.pem".format(server_name)
    KEY_FILE = "/etc/letsencrypt/live/{0}/privkey.pem".format(server_name)
    os.makedirs("/etc/letsencrypt/live/{0}".format(server_name), exist_ok=True)

    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

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


if __name__ == '__main__':
    SelfSignedCertificate()  # pylint: disable=no-value-for-parameter
