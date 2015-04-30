import client
import random
import time
import hashlib

BASE_URL = 'http://pac.bouillaguet.info/TP5/id-based-signature'


if __name__ == '__main__':
    server = client.Server(BASE_URL)

    seed = int(time.time())
    random.seed(seed)

    response = server.query('/KDC/PK')

    n = response['n']
    e = response['e']

    response = server.query('/KDC/keygen/sommerard')

    secret_key = response['secret-key']

    i = pow(secret_key, e, n)

    r = random.randint(1, pow(2, 128))
    r = 12345

    t = pow(r, e, n)

    m = '#YOLO'

    sha = hashlib.sha256()
    sha.update(m.encode())
    sha.update(str(t).encode())
    tmp = sha.hexdigest()
    print(tmp)

    hashm = int(tmp, base=16)
    s = (secret_key * pow(r, hashm, n)) % n

    if pow(s, e, n) == ((i * pow(t, hashm, n)) % n):
        print('signature ok!')
    else:
        print('signature error!')
        exit(1)

    parameters = { 's': s, 't': t, 'm': m }
    response = server.query('/check/sommerard', parameters)
    print(response)
