import client
import random
import time
from hashlib import sha256
import base64

BASE_URL = 'http://pac.bouillaguet.info/TP5/broken-PKCS-signature'


sha256_oid = b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20'

class EMSAError(Exception):
    pass

def emsa_pkcs1_encode(message, k):
    '''Take a message M and return
       the concatenation of length k:

        0x00 || 0x01 || PS || 0x00 || hash-oid || hash

       where PS is a string of length
       k - len(message) - 3 containing 0xfffffff.........

       hash = SHA-256(message)
       hash-oid : the Object Identifier of the hash function
       k - the length of the padded byte string

       >>> m = "toto est content".encode()
       >>> block = emsa_pkcs1_encode(m, 100)
       >>> base64.b16encode(block)
       b'0001FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF003031300D06096086480165030402010500042020EED533D25E17520EC4D8C364A0486242ED49A4E42B82489565C5A6877D1C95'
    '''
    h = sha256(message)
    payload = sha256_oid + h.digest()
    m_len = len(payload)
    print('m_len:', m_len)
    print('k - 11:', k - 11)
    if m_len > k - 11:
        raise EMSAError("k is too short")
    ps_len = k - len(message) - 3
    print('ps_len:', ps_len)
    ps = b'\xff' * ps_len
    print('-' * 80)
    return b'\x00\x01' + ps + b'\x00' + payload


def isqrt(n):
    """ renvoie le plus grand entier k tel que k^3 <= n. Méthode de Newton."""
    x = n
    y = (x + 1) // 3

    while y < x:
        x = y
        y = (2 * x + n // pow(x, 2)) // 3

    return x


if __name__ == '__main__':
    server = client.Server(BASE_URL)

    response = server.query('/PK')

    e = response['e']
    n = response['n']

    X = 1
    Y = 100000
    m = "Virement du compte {0} de {1} euros pour sommerard".format(X, Y).encode()
    k = 8 + len(m) + 3

    print('-' * 80)

    block = emsa_pkcs1_encode(m, k)
    print('block:', base64.b16encode(block))
    print('-' * 80)

    inf = b'\x00' * 194
    sup = b'\xff' * 194

    borne_inf = block + inf
    borne_sup = block + sup

    print('borne_inf:', base64.b16encode(borne_inf))
    print('-' * 80)
    print('borne_sup:', base64.b16encode(borne_sup))
    print(int(base64.b16encode(borne_sup), base=16))
    print('-' * 80)

    x = isqrt(int(base64.b16encode(borne_sup), base=16))
    print('x:', x)
    print('-' * 80)
    print('x**3:', pow(x, 3))

    if pow(x, 3) > int(base64.b16encode(borne_inf), base=16):
        print('x**3 ok!')

    print('-' * 80)

    parameters = { 'signature': x, 'account-number': X,
        'amount': Y }
    response = server.query('/transfer/sommerard', parameters)
    print(response)
