import client
import sys
import random
import time

BASE_URL = 'http://pac.bouillaguet.info/TP5/RSA-reductions'

def isqrt(n):
    """ renvoie le plus grand entier k tel que k^2 <= n. Méthode de Newton."""
    x = n
    y = (x + 1) // 2

    while y < x:
        x = y
        y = (x + n // x) // 2

    return x


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


# def partie_d():
#     # http://stackoverflow.com/questions/2921406/calculate-primes-p-and-q-from-private-exponent-d-public-exponent-e-and-the
#
#     response = server.query('/d/challenge/sommerard')
#
#     d = response['d']
#     e = response['e']
#     n = response['n']
#
#     de = e * d
#     modulusplus1 = n + 1
#     deminus1 = de - 1
#
#     kprima = de // n
#
#     ks = [kprima, kprima - 1, kprima + 1]
#
#     for k in ks:
#         phi = deminus1 // k
#         pplusq = modulusplus1 - phi
#         delta = pow(pplusq, 2) - (4 * n)
#
#         deltasqrt = isqrt(delta)
#
#         p = (pplusq + deltasqrt) // 2
#
#         if n % p != 0:
#             continue
#
#     print('>>p:', p)
#     parameters = { 'p': p }
#     response = server.query('/d/check/sommerard', parameters)
#     print(response)


def partie_d():
    # http://stackoverflow.com/questions/2921406/calculate-primes-p-and-q-from-private-exponent-d-public-exponent-e-and-the
    random.seed(time.time())

    response = server.query('/d/challenge/sommerard')

    d = response['d']
    e = response['e']
    n = response['n']

    k = (e * d) - 1

    if k % 2 == 0:
        print('>>k even')
    else:
        print('>>k odd')

    print('k:', k)

    r = k // 2
    while r % 2 == 0:
        r = r // 2

    print('r:', r)

    t = 1
    tmp = pow(2, t) * r
    while k != tmp:
        t += 1
        tmp = pow(2, t) * r

    print('t:', t)

    flag = False
    for i in range(1, 101):
        flag31 = False
        flag5 = False
        g = random.randint(0, n - 1)
        y = pow(g, r, n)

        if y == 1 or y == n - 1:
            continue

        for j in range(1, t):
            x = pow(y, 2, n)

            if x == 1:
                flag5 = True
                break

            if x == n - 1:
                flag31 = True
                break

            y = x

        if flag5:
            flag = True
            break

        if flag31:
            continue

        x = pow(y, 2, n)

        if x == 1:
            flag = True
            break

    if not flag:
        print('>>Error, prime factor not found!')

    p, _, _ = XGCD(y - 1, n)

    print('>>p:', p)

    q = n // p

    print('q:', q)

    if n == p * q:
        print('>>n == p * q')
        print('>>>>Ok!')

    if isprime(p):
        print('>>p prime')

    if isprime(q):
        print('>>q prime')

    phi = (p - 1) * (q - 1)
    tmp, _, _ = XGCD(e, phi)

    print('tmp:', tmp)

    inve = invmod(e, phi)
    if d % phi == inve:
        print('d % phi == inve')

    if d * e % phi == 1:
        print('d * e % phi == 1')

    parameters = { 'p': p }
    response = server.query('/d/check/sommerard', parameters)
    print(response)


def partie_phi():
    response = server.query('/phi/challenge/sommerard')

    n = response['n']
    phi = response['phi']
    e = response['e']

    # phi(n) = (p - 1)(q - 1)

    # phi(n) = n - (p + q) + 1

    # S = p + q

    # p + q = S
    # p * q = n

    # p * (S - p) = n

    S = -phi + 1 + n
    print('>>S:', S)

    # p.S - p² = n
    # -p² + p.S - n = 0

    # delta = b² - 4ac
    delta = pow(S, 2) - (4 * -1 * -n)
    print('>>delta:', delta)

    x1 = (-S - isqrt(delta)) // -2
    x2 = (-S + isqrt(delta)) // -2

    p = x1
    q = S - p

    if p * q == n:
        print('>>p == x1')
    else:
        p = x1
        q = S - p
        if p * q == n:
            print('>>p == x1')
        else:
            print('>>Erreur!')

    parameters = { 'p': p }
    response = server.query('/phi/check/sommerard', parameters)
    print(response)

if __name__ == '__main__':
    server = client.Server(BASE_URL)

    if len(sys.argv) < 2:
        print('Error, no arg!')
        exit(0)

    if sys.argv[1] == 'phi':
        partie_phi()
    elif sys.argv[1] == 'd':
        partie_d()
    else:
        print('Error, bad arg!')
        exit(0)
