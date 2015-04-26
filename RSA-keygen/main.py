import client
import random
import time

BASE_URL = 'http://pac.bouillaguet.info/TP5/RSA-keygen'

def XGCD(a, b):
    u = (1, 0)
    v = (0, 1)

    while(b != 0):
        q, r = divmod(a, b)
        a = b
        b = r
        tmp = (u[0] - q * v[0], u[1] - q * v[1])
        u = v
        v = tmp

    return a, u[0], u[1]


def invmod(a, b):
    g, x, y = XGCD(a, b)
    return x


def _miller_rabin(rn, n):
    """
        Appel interne pour le test de primalité du nombre n avec la méthode de Miller-Rabin.
    """
    b = n - 1
    a = 0

    while b % 2 == 0:
        b //= 2
        a += 1

    if pow(rn, b, n) == 1:
        return True

    for i in range(0, a):
        if pow(rn, b, n) == n-1:
            return True
        b *= 2

    return False


def _isprime(n):
    """
        Appel interne pour le test de primalité du nombre n avec la méthode naive.
    """
    if n < 7:
        if n in (2, 3, 5):
            return True
        else:
            return False

    if n & 1 == 0:
        return False

    k = 3
    sqrtn = heronsqrt(n)

    while k <= sqrtn:
        if n % k == 0:
            return False
        k += 2

    return True


def miller_rabin(n, k=20):
    """
        Test de primalité du nombre n avec la méthode de Miller-Rabin.
    """
    global lpn

    if n <= 1024:
        if n in lpn:
            return True
        else:
            return False

    if n & 1 == 0:
        return False

    for i in range(0, k):
        rn = random.randint(1, n-1)
        if not _miller_rabin(rn, n):
            return False

    return True


def isprime(n):
    """
        Test de primalité du nombre n avec la méthode naive si le nombre n a moins de 9 chiffres, méthode de Miller-Rabin sinon.
    """
    if len(str(n)) > 9:
        return miller_rabin(n)
    else:
        return _isprime(n)


def getPrimeNumber():
    rnd = random.getrandbits(1024)

    while not isprime(rnd):
        if(rnd % 2 == 0):
            rnd += 1
        else:
            rnd += 2

    return rnd


if __name__ == '__main__':
    server = client.Server(BASE_URL)

    random.seed(int(time.time()) + 1239434058324923)

    response = server.query('/challenge/sommerard')

    e = response['e']

    print('-' * 80)
    print('e:', e)

    p = getPrimeNumber()
    q = getPrimeNumber()
    fin = (p - 1) * (q - 1)

    i = 1

    while XGCD(e, fin) != 1:
        print(i)
        q = getPrimeNumber()
        fin = (p - 1) * (q - 1)

        i += 1

    n = p * q

    d = invmod(e) % fin

    print('p:', p)
    print('q:', q)
    print('fin:', fin)
    print('n:', n)
    print('d:', d)
    print('-' * 80)

    parameters = { 'n': n, 'e': e }

    response = server.query('/PK/sommerard', parameters)
    print(response)
