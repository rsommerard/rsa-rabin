import client
import random
import time
import hashlib
import sys

BASE_URL = 'http://pac.bouillaguet.info/TP5/PAC-evaluation'


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


if __name__ == '__main__':
    server = client.Server(BASE_URL)

    RSA_e = 146673966603310777384544284922718099565
    RSA_p = 19803557932480967893106716674050276282535009195733744473575510360101813037962187902875837061653345359650082300876387925441777598970271525179342186636540189682863183296451381193214931073649230573225318600345549931674654309372601681527660506344809675030116197983880139698153622755500367727812090365726833893282626293465731080997525822262922858448487770704637571996710141421110986749340687910238337329842234776936837354093275135878732645743363131439166953269949040995828461657951331159124015190148486000124478524919744545713533210658198408356092025898485506259388055716020345534496986290138428411385710730659540639287537
    RSA_q = 4500667513489678897904316007133108800960221375658464777406919058102659757881295042693610493801186287639386001382958501293829921296323211290183360531923201476240705170885977221075617389867549675141583871281967360570760419047363081580535158297846569518693291763439582863020325737146929208765184645324476848644706606061013769296188258864380559902639433526170369589991022194712698780940581840813472828822550434001908793783145411028236907599413844482010550160222044861037438466502376325701041317423539458382512351835817341467908060006468661204441180446483161150017745505335126536215571049336728464693730926914281981825599
    RSA_fin = (RSA_p - 1) * (RSA_q - 1)
    RSA_n = RSA_p * RSA_q
    RSA_d = invmod(RSA_e, RSA_fin) % RSA_fin

    categories = ['COURS', 'TD', 'SAV', 'SUPPORT', 'PORTAIL', 'DS', 'DIFFICILE',
        'UTILE', 'GENERAL', 'TP']

    if len(sys.argv) < 2:
        print('Arg error!')
        print('python main.py <category> <grade>')
        exit(1)
    elif sys.argv[1] not in categories:
        print('Arg error!')
        print('python main.py <category> <grade>')
        exit(1)

    category = sys.argv[1]
    grade = int(sys.argv[2])

    response = server.query('/PK')
    print('-' * 80)
    print(response)
    print('-' * 80)

    submission = response['submission']
    receipt = response['receipt']

    seed = int(time.time())
    random.seed(seed)

    S = random.randint(1, pow(2, 128))
    # S = 45966684783666058601339552348901769540
    print('-' * 80)
    print('S:', S)
    print('-' * 80)

    sha = hashlib.sha256()
    sha.update("{0:08x}".format(S).encode())
    m = sha.hexdigest()

    N = submission[category]['n']
    e = submission[category]['e']

    r = random.randint(2, N - 1)
    re = pow(r, e, N)
    tmp, _, _ = XGCD(re, N)
    while tmp != 1:
        r = random.randint(2, N - 1)
        re = pow(r, e, N)
        tmp, _, _ = XGCD(re, N)

    print('-' * 80)
    print('r:', r)
    print('-' * 80)

    blinded = (re * int(m, base=16)) % N

    sign = pow(blinded, RSA_d, RSA_n)

    if pow(sign, RSA_e, RSA_n) == (blinded % RSA_n):
        print('sign ok!')
    else:
        print('sign error!')
        exit(1)

    parameters = { 'category': category, 'blinded': blinded, 'signature': sign }
    response = server.query('/token/sommerard', parameters)
    print('-' * 80)
    print(response)
    print('-' * 80)

    blind_signature = response['blind-signature']

    if pow(blind_signature, e, N) == (blinded % N):
        print('blind_signature ok!')
    else:
        print('blind_signature error!')
        exit(1)

    mask = invmod(r, N) % N
    token = (mask * blind_signature) % N

    Sb = random.randint(1, pow(2, 128))
    # Sb = 222163335339593337246093470171730442793

    print('-' * 80)
    print('Sb:', Sb)
    print('-' * 80)

    sha = hashlib.sha256()
    sha.update("{0:08x}".format(Sb).encode())
    mb = sha.hexdigest()

    Nb = receipt[category]['n']
    eb = receipt[category]['e']

    rb = random.randint(2, Nb - 1)
    rbeb = pow(rb, eb, Nb)
    tmp, _, _ = XGCD(rbeb, Nb)
    while tmp != 1:
        rb = random.randint(2, Nb - 1)
        rbeb = pow(rb, eb, Nb)
        tmp, _, _ = XGCD(rbeb, Nb)

    print('-' * 80)
    print('rb:', rb)
    print('-' * 80)

    blindedb = (rbeb * int(mb, base=16)) % Nb

    signb = pow(blindedb, RSA_d, RSA_n)

    if pow(signb, RSA_e, RSA_n) == (blindedb % RSA_n):
        print('sign ok!')
    else:
        print('sign error!')
        exit(1)

    parameters = { 'category': category, 'grade': grade, 'comment': '#YOLO',
        'submission-token': token, 'S': S, 'blinded': blindedb }

    response = server.query('/post', parameters)

    print('-' * 80)
    print(response)
    print('-' * 80)



    # blind_signature_b = response['blind-signature']
    #
    # if pow(blind_signature_b, eb, Nb) == (blindedb % Nb):
    #     print('blind_signature_b ok!')
    # else:
    #     print('blind_signature_b error!')
    #     exit(1)
    #
    # maskb = invmod(rb, Nb) % Nb
    # tokenb = (maskb * blind_signature_b) % Nb
    #
    # parameters = { 'category': category, 'receipt-token': tokenb, 'S': Sb }
    #
    # response = server.query('/receipt', parameters)
    #
    # print('-' * 80)
    # print(response)
    # print('-' * 80)
