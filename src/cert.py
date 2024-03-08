from cryptography import x509
from cryptography.hazmat.backends import default_backend
import re

def extract_certificates_from_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()

    cert_regex = r"-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----"
    certificates = re.findall(cert_regex, file_content, re.DOTALL)

    return certificates

def get_certificate_info(cert_pem):
    cert = x509.load_pem_x509_certificate(cert_pem.encode(), default_backend())

    subject = cert.subject.rfc4514_string()
    issuer = cert.issuer.rfc4514_string()
    valid_from = cert.not_valid_before
    valid_until = cert.not_valid_after
    serial_number = cert.serial_number

    info = {
        "Subject": subject,
        "Issuer": issuer,
        "Valid From": valid_from,
        "Valid Until": valid_until,
        "Serial Number": serial_number,
    }

    return info


def printcerts( certificates):
    unique_certificates = set(certificates)  

    for cert_pem in unique_certificates:
        cert_info = get_certificate_info(cert_pem)
        print(cert_info)


