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

    # i = ''
    # for l in range(16):
    #     sha = hashlib.sha256()
    #     sha.update('sommerard'.encode())
    #     sha.update("{0:08x}".format(l).encode())
    #     i += sha.hexdigest()
    #
    # print(int(i, base=16))
    # print(int(i, base=16) % n)
    # print(pow(secret_key, e, n))
    #
    # if pow(secret_key, e, n) == (int(i, base=16) % n):
    #     print('secret_key ok!')
    # else:
    #     print('secret_ket error!')
    #     exit(1)

    r = random.randint(1, pow(2, 128))

    t = pow(r, e, n)

    m = '#YOLO'

    sha = hashlib.sha256()
    sha.update(m.encode())
    sha.update("{0:08x}".format(t).encode())
    tmp = sha.hexdigest()

    hashm = int(tmp, base=16)
    s = (secret_key * pow(r, hashm, n)) % n

    parameters = { 's': s, 't': t, 'm': m }
    response = server.query('/KDC/check/sommerard', parameters)
    print(response)
