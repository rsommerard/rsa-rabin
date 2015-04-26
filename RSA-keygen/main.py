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


if __name__ == '__main__':
    server = client.Server(BASE_URL)

    # seed = int(time.time())
    # random.seed(seed)
    #
    # response = server.query('/challenge/sommerard')
    #
    # e = response['e']
    #
    # print('-' * 80)
    # print('e:', e)
    #
    # p = getPrimeNumber()
    #
    # q = getPrimeNumber()
    # fin = (p - 1) * (q - 1)
    #
    # tmp, _, _ = XGCD(e, fin)
    #
    # while tmp != 1:
    #     p = getPrimeNumber()
    #     q = getPrimeNumber()
    #     fin = (p - 1) * (q - 1)
    #     tmp, _, _ = XGCD(e, fin)
    #
    # n = p * q
    #
    # d = invmod(e, fin) % fin
    #
    # print('p:', p)
    # print('q:', q)
    # print('fin:', fin)
    # print('n:', n)
    # print('d:', d)
    # print('-' * 80)

    e = 146673966603310777384544284922718099565
    p = 19803557932480967893106716674050276282535009195733744473575510360101813037962187902875837061653345359650082300876387925441777598970271525179342186636540189682863183296451381193214931073649230573225318600345549931674654309372601681527660506344809675030116197983880139698153622755500367727812090365726833893282626293465731080997525822262922858448487770704637571996710141421110986749340687910238337329842234776936837354093275135878732645743363131439166953269949040995828461657951331159124015190148486000124478524919744545713533210658198408356092025898485506259388055716020345534496986290138428411385710730659540639287537
    q = 4500667513489678897904316007133108800960221375658464777406919058102659757881295042693610493801186287639386001382958501293829921296323211290183360531923201476240705170885977221075617389867549675141583871281967360570760419047363081580535158297846569518693291763439582863020325737146929208765184645324476848644706606061013769296188258864380559902639433526170369589991022194712698780940581840813472828822550434001908793783145411028236907599413844482010550160222044861037438466502376325701041317423539458382512351835817341467908060006468661204441180446483161150017745505335126536215571049336728464693730926914281981825599
    fin = (p - 1) * (q - 1)
    n = p * q
    d = invmod(e, fin) % fin

    parameters = { 'n': n, 'e': e }

    response = server.query('/PK/sommerard', parameters)

    ciphertext = response['ciphertext']

    m = pow(ciphertext, d, n)

    parameters = { 'm': m }

    response = server.query('/confirmation/sommerard', parameters)
    print(response)
