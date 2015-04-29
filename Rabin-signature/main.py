import client
import random
import time

import hashlib

BASE_URL = 'http://pac.bouillaguet.info/TP5/Rabin-signature'

# def XGCD(a, b):
#     u = (1, 0)
#     v = (0, 1)
#
#     while(b != 0):
#         q, r = divmod(a, b)
#         a = b
#         b = r
#         tmp = (u[0] - q * v[0], u[1] - q * v[1])
#         u = v
#         v = tmp
#
#     return a, u[0], u[1]
#
#
# def invmod(a, b):
#     g, x, y = XGCD(a, b)
#     return x

# retourne 1 si racine
def legendre(a, p):
    tmp = (p - 1) // 2
    return pow(a, tmp, p)


def _miller_rabin(rn, n):
    """
        Appel interne pour le test de primalité du nombre n avec la méthode de Miller-Rabin.
    """
    b = n - 1
    a = 0

    while b % 2 == 0:
        b >>= 1
        a += 1

    if pow(rn, b, n) == 1:
        return True

    for i in range(0, a):
        if pow(rn, b, n) == n - 1:
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
    rnd = random.getrandbits(2048)

    while not isprime(rnd):
        if(rnd % 2 == 0):
            rnd += 1
        else:
            rnd += 2

    return rnd


def heronsqrt(n):
    """
        Calcul de la racine carré pour un grand nombre avec la méthode de Héron.
    """
    s1 = 1
    while True:
        s2 = (s1 + n // s1) // 2
        if abs(s1 - s2) < 2:
            if s1 * s1 <= n and (s1 + 1) * (s1 + 1) > n:
                return s1
        s1 = s2


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


def isqrt(n):
    """ renvoie le plus grand entier k tel que k^2 <= n. Méthode de Newton."""
    x = n
    y = (x + 1) // 2

    while y < x:
        x = y
        y = (x + n // x) // 2

    return x


if __name__ == '__main__':
    server = client.Server(BASE_URL)

    seed = int(time.time())
    random.seed(seed)

    # print('-' * 80)
    #
    # p = getPrimeNumber()
    # while p % 4 != 3:
    #     p = getPrimeNumber()
    #
    # print('p:', p)
    #
    # q = getPrimeNumber()
    # while q % 4 != 3:
    #     q = getPrimeNumber()
    #
    # print('q:', q)
    #
    # n = p * q
    #
    # print('n:', n)
    # print('-' * 80)

    p = 13437097018679702243982896796386237550531271376408172623473937511337545063222781451220004308228049359166573689457527961433895716626039215547060947995287862870139838512915393415128852409364892601914355192967970931665667799373806110563723169722041492965735843823842705533018075529636986201102256704489131569849295950504433214372502532035920445493044024147332854321294938883949498654435134421710125069266841338446467425173021656953613931327833658434334703634927926811749914248841879647305649941769716892241144387112609725080030632793636215419035916229004832229239166141982652704289704122955933349772593868057685579076683
    q = 31020600400775637808157586245250887572211915548647731043906784190372842777322668902002892093506464311499121579953651915916189155962835443971937937565276567726627954764651109741742039115894734964711475384032441159309464127332251292664004139095749101426912768635080421004606341641054524929647475201144804230609788041462858252237221954061241771194415647524568439307664592179450375463145187137701526634546424302366055864846435446134238923286692659633907419837964192305901333695772796274975003146905851440115239431168717241360908377863986554986302837628318504026033210650891112737300605814455189666973293473171485778663583
    n = p * q

    if p % 4 == 3:
        print('p % 4 == 3')
    else:
        print('p error: p % 4 != 3')

    if q % 4 == 3:
        print('q % 4 == 3')
    else:
        print('q error: q % 4 != 3')

    if isprime(p):
        print('p prime')
    else:
        print('p not prime')

    if isprime(q):
        print('q prime')
    else:
        print('q not prime')

    if isprime(n):
        print('n prime')
    else:
        print('n not prime')

    parameters = { 'n': n }

    response = server.query('/challenge/sommerard', parameters)

    m = response['m']

    m = int(m, base=16)

    k = 256

    while True:
        U = random.randint(2, pow(2, k))

        sha = hashlib.sha256()

        sha.update("{0:08x}".format(m).encode())
        sha.update("{0:08x}".format(U).encode())

        y = sha.hexdigest()

        if legendre(int(y, base=16), p) != 1:
            print('legendre(int(y, base=16), p) != 1')
            continue

        if legendre(int(y, base=16), q) != 1:
            print('legendre(int(y, base=16), q) != 1')
            continue

        print('U:', U)

        break

    x1p = pow(int(y, base=16), ((p + 1) // 4), p)
    x2p = p - x1p

    print('x1p:', x1p)

    if pow(x1p, 2, p) == int(y, base=16):
        print('x1p OK!')
    else:
        print('x1p error!')

    print('x2p:', x2p)
    if pow(x2p, 2, p) == int(y, base=16):
        print('x2p OK!')
    else:
        print('x2p error!')

    x1q = pow(int(y, base=16), ((q + 1) // 4), q)
    x2q = q - x1q

    print('x1q:', x1q)

    if pow(x1q, 2, q) == int(y, base=16):
        print('x1q OK!')
    else:
        print('x1q error!')

    print('x2q:', x2q)
    if pow(x2q, 2, q) == int(y, base=16):
        print('x2q OK!')
    else:
        print('x2q error!')

    alpha = x1p
    beta = x1q
    _, r, s = XGCD(p, q)
    x = ((beta * r * p) + ( alpha * s * q)) % n

    # np = int(y, base=16) % p
    # nq = int(y, base=16) % q
    #
    # alpha = heronsqrt(np) % p
    # beta = heronsqrt(nq) % q
    #
    # _, r, s = XGCD(p, q)
    #
    # x = ((beta * r * p) + ( alpha * s * q)) % n
    #
    # f = ((r * p) - (s * q)) % n

    print('x:', x)
    # print('fx:', f * x)
    # print('sqtr(y):', isqrt(int(y, base=16)))
    print('x**2:', pow(x, 2, n))
    print('y:', int(y, base=16))

    parameters = { 'n': n, 's': x, 'u': "{0:08x}".format(U)}
    response = server.query('/check/sommerard', parameters)
    print(response)

    # x = heronsqrt(int(y, base=16))
    # print('x:', x)
    #
    # print('y:', int(y, base=16))
    #
    # xpow = pow(x, 2, n)
    # while(xpow != int(y, base=16)):
    #     print('xpow:', xpow)
    #     print('y:', int(y, base=16))
    #     xpow = pow(xpow, 2, n)
    #
    #
    # print('xpow:', xpow)
    # print('y:', int(y, base=16))
    # print('OK!')


    # tmp, _, _ = XGCD(y, n)
    # while tmp != 1:
    #     U = random.randint(2, pow(2, k))
    #     sha = hashlib.sha256()
    #
    #     sha.update("{0:08x}".format(m).encode())
    #     sha.update("{0:08x}".format(U).encode())
    #
    #     y = sha.hexdigest()

    # while pow(x, 2, n) != y:
    #     u += 1
    #     sha = hashlib.sha256()
    #
    #     sha.update("{0:08x}".format(m).encode())
    #     sha.update("{0:08x}".format(u).encode())
    #
    #     y = sha.hexdigest()
    #     x = heronsqrt(int(y, base=16))
    #
    # print('x:', x)
    # print('u:', u)
