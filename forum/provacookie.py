__author__ = 'davide'

import http.cookiejar as CJ
import urllib.request as urlreq

URL = "http://localhost:8000/gni"

cj = CJ.CookieJar()
opener = urlreq.build_opener(urlreq.HTTPCookieProcessor(cj))
urlreq.install_opener(opener)

#resp = urlreq.urlopen(URL)
#print(resp.read().decode('utf-8', errors="ignore"))
print("*****************" * 10)
resp = urlreq.urlopen(URL + "/gni2")
print(resp.read().decode('utf-8', errors="ignore"))