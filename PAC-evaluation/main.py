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
        print('>>category: COURS | TD | SAV | SUPPORT | PORTAIL | DS | DIFFICILE | UTILE | GENERAL | TP')
        exit(1)
    elif sys.argv[1] not in categories:
        print('Arg error!')
        print('python main.py <category> <grade>')
        print('>>category: COURS | TD | SAV | SUPPORT | PORTAIL | DS | DIFFICILE | UTILE | GENERAL | TP')
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

    # S = random.randint(1, pow(2, 128))
    S = 137306116852650062182619816270626522680
    print('-' * 80)
    print('S:', S)
    print('-' * 80)

    sha = hashlib.sha256()
    sha.update("{0:08x}".format(S).encode())
    m = sha.hexdigest()

    N = submission[category]['n']
    e = submission[category]['e']

    # r = random.randint(2, N - 1)
    r = 14655749257845349201304025183379820046872341042428654589999957321598948963110281496743691967325012990841257969228187142953174870745621589871147683836328754472077350992142781291133792373966616468745828584943471319288703293095696055868262603371524265514339237154546902461434236801512109239657829395748638914572405308344138671885660526017399099141818247575700320926101338108521935291556363511246325080293746525286523560240280335740698071891736415571275578889570510570734586773500574776911488525752944702463204262674491944123002656138900397474710419779490129595141320747693956076248563264120965920239631744618124556832421
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

    # parameters = { 'category': category, 'blinded': blinded, 'signature': sign }
    # response = server.query('/publication-token/sommerard', parameters)
    # print('-' * 80)
    # print(response)
    # print('-' * 80)

    # blind_signature = response['blind-signature']
    blind_signature = 21329423515113121224163706077070955417458721382908721347938493189113054799161697008664251353482281908713262112561636618330772776060884120877301790708997829773316240305073993990994466121493104181201717258858919376382639465072076392041944719124844382189111523884647448785521388073202950820823289385705794849826231793215133904016817497882690758480641104685642560537748124972953798125332940607357383664225547868417735573075661396026193041030389367012004443255524244897773316946839082141705378780881949659094066780392936540162483720752801933652312345161490554554225954831344583119880227169874116494561380730916988896040854

    if pow(blind_signature, e, N) == (blinded % N):
        print('blind_signature ok!')
    else:
        print('blind_signature error!')
        exit(1)

    mask = invmod(r, N) % N
    token = (mask * blind_signature) % N

    if (token * r) % N == blind_signature:
        print('token ok!')
    else:
        print('token error!')
        exit(1)

    # Sb = random.randint(1, pow(2, 128))
    Sb = 192607743734897343530301259326683250491

    print('-' * 80)
    print('Sb:', Sb)
    print('-' * 80)

    sha = hashlib.sha256()
    sha.update("{0:08x}".format(Sb).encode())
    mb = sha.hexdigest()

    Nb = receipt[category]['n']
    eb = receipt[category]['e']

    # rb = random.randint(2, Nb - 1)
    rb = 17987284948452793863839290589407588110808238868212534020218260021566457090109595368875984215566589230549787705687408004689499337987114127041925272282177006411584793650918705529582655052130767375799326282392416888821338971043572742190794579430925971705096823623738536324554756833625800762224697437892218268726155582666601571624282486534596886295493962644507437931034740625512641466028870346018142145810897171864685181166026963450880625070651072023893772862263891162590423740930753715877821367168412680471091681467846062258894812515024889529284208730353982269273728603099178934093867632045278297193254427283720059148606
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
