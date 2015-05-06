import client
import random
import time
import hashlib
import base64

BASE_URL = 'http://pac.bouillaguet.info/TP5/id-based-signature'


if __name__ == '__main__':
    server = client.Server(BASE_URL)

    seed = int(time.time())
    random.seed(seed)

    response = server.query('/KDC/PK')

    n = response['n']
    e = response['e']

    i = ''
    for j in range(16):
        tmp = "{0:08x}".format(j)
        if len(tmp) % 2 != 0:
            tmp = '0' + tmp
        tmp = tmp.upper()
        print(tmp)

        sha = hashlib.sha256()
        sha.update('sommerard'.encode())
        sha.update(base64.b16decode(tmp))
        tmp = sha.hexdigest()

        print('i:', i)
        print('tmp:', tmp)
        i += tmp
        print('>i:', i)

    i = int(i, base=16) % n
    response = server.query('/KDC/keygen/sommerard')

    secret_key = response['secret-key']

    print(pow(i, e, n))
    print(secret_key)
    print(i)
    print(pow(secret_key, e, n))
    if pow(i, e, n) == secret_key:
        print('i ok!')
    else:
        print('i error!')
        exit(1)

    r = random.randint(1, pow(2, 128))

    t = pow(r, e, n)

    m = '#YOLO'

    tmp = "{0:08x}".format(t)
    if len(tmp) % 2 != 0:
        tmp = '0' + tmp

    tmp = tmp.upper()

    sha = hashlib.sha256()
    sha.update(m.encode())
    sha.update(base64.b16decode(tmp))
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
