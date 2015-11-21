__author__ = 'davide'

import re
import http.cookiejar as CJ
import urllib.request as urlreq
import urllib.parse as urlparse
import hashlib as hl
import getpass

USER = "glennhk"
COOKIE_LENGTH = "-1"
PWD = ""
URL = "http://www.python-it.org/forum/index.php?action="
ACTION_LOGIN2 = "login2"
ACTION2 = urlparse.quote_plus("login2;sa=check;member=7107")


def get_hash(u, p, sess_id):
    m = hl.sha1()
    m.update(u + p)
    d = m.hexdigest().encode()
    m = hl.sha1()
    m.update(d + sess_id)
    return m.hexdigest()


def getpwd():
    return ""


def get_sess_id():
    url = "http://www.python-it.org/forum/index.php"
    regex = r"hashLoginPassword\(this, '(?P<s_id>\w+)'\);"
    u = urlreq.urlopen(url)
    s = re.search(regex, u.read().decode('utf-8', errors='ignore'))
    return s.group("s_id")

if __name__ == "__main__":
    cj = CJ.CookieJar()
    logindata = urlparse.urlencode({'user': USER,
                                    'passwrd': PWD,
                                    'hash_passwrd': get_hash(USER.encode(),
                                                             getpwd().encode(),
                                                             get_sess_id().encode()),
                                    'cookielength': COOKIE_LENGTH})
    opener = urlreq.build_opener(urlreq.HTTPCookieProcessor(cj))
    urlreq.install_opener(opener)
    resp = urlreq.urlopen(URL + ACTION_LOGIN2, logindata.encode('utf-8'))
    print(resp.read().decode('utf-8', errors="ignore"))
    resp = urlreq.urlopen(URL + ACTION2)
    print(resp.read().decode('utf-8', errors="ignore"))

    #resp = urlreq.urlopen(URL + "unread")
    #print(resp.read().decode('utf-8', errors="ignore"))