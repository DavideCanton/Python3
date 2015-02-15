import http.cookiejar as CJ
import urllib.request as urlreq
import urllib.parse as urlparse
from html.parser import HTMLParser
import re

index_url = 'http://icampus.ingegneria.unical.it'
search_url = "http://icampus.ingegneria.unical.it/claroline/auth/courses.php"
remove_url = search_url + "?cmd=exUnreg&course="
add_url = search_url + "?cmd=exReg&course="
login_url = "http://icampus.ingegneria.unical.it/claroline/auth/login.php"

__all__ = ["ICampusCourse", "ICampusHandler",
           "ICampusLoginError", "ICampusParserError"]

class ICampusError(Exception):
    pass

class ICampusParserError(ICampusError):
    pass

class ICampusLoginError(ICampusError):
    pass


class ICampusHandler(object):
    def __init__(self, data):
        self.listaCorsiParser = ListaCorsiParser()
        self.searchCorsiParser = SearchCorsiParser()
        self._openSession(data)

    def getCorsi(self):
        """
        returns una lista:
        corsi = [ corsi ]
        """
        self.listaCorsiParser.reset()
        response = urlreq.urlopen(index_url)
        resp = response.read().decode('utf-8', errors='ignore')
        if "item" not in resp:
            raise ICampusParserError("Error")
        self.listaCorsiParser.feed(resp)
        self.cache = self.listaCorsiParser.data
        return self.cache

    def invalidateCache(self):
        self.cache = None

    def removeCorso(self, corso):
        prev = (self.cache or [])[:]
        urlreq.urlopen(remove_url + corso)
        self.getCorsi()
        return len(prev) > len(self.cache)

    def addCorso(self, corso):
        prev = (self.cache or [])[:]
        urlreq.urlopen(add_url + corso)
        self.getCorsi()
        return len(prev) < len(self.cache)

    def searchCorso(self, corso):
        data = {"cmd": "rqReg",
                "fromAdmin": "",
                "uidToEdit": "142032",
                "keyword": corso}
        data_encoded = urlparse.urlencode(data).encode()
        response = urlreq.urlopen(search_url, data_encoded)
        resp = response.read().decode('utf-8', errors='ignore')
        if "Non ci sono corsi" in resp:
            return None
        self.searchCorsiParser.reset()
        self.searchCorsiParser.feed(resp)
        return self.searchCorsiParser.data

    def _openSession(self, data):
        cj = CJ.CookieJar()
        opener = urlreq.build_opener(urlreq.HTTPCookieProcessor(cj))
        logindata = urlparse.urlencode({'login': data[0], 'password': data[1]})
        urlreq.install_opener(opener)
        resp = urlreq.urlopen(login_url, logindata.encode('utf-8'))
        response = resp.read().decode('utf-8', errors='ignore')
        if "I miei corsi" not in response:
            raise ICampusLoginError("Dati non validi")


#<li class="item"> [o "item_hot"]
#    <a href="/claroline/course/index.php?cid=CODICE">
#        NOME (COD)
#    </a>
#    <br />
#    <small>
#        AUTORE
#    </small>
#</li>


class ICampusCourse:
    def __init__(self, code="", name="", author="", hot=False):
        self.code = code
        self.name = name
        self.author = author
        self.hot = hot

    def __str__(self):
        header = "> [!]" if self.hot else ">"
        return "{}{} di {} ({})".format(header, self.name,
                                        self.author, self.code)


class ListaCorsiParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.regex = re.compile("(?<=cid=)\S+&?")

    def reset(self):
        HTMLParser.reset(self)
        self.data = []
        # il corso corrente
        self.current = ICampusCourse()
        # lo stato
        self.state = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "ul" and self.state == 0:
            self.state = 1
        elif tag == "li"and self.state == 1:
            self.state = 2
            self.current.hot = "hot" in attrs["class"]
        elif tag == "a"and self.state == 2:
            self.state = 3
            code = re.search(self.regex, attrs["href"]).group(0)
            self.current.code = code
        elif tag == "small"and self.state == 4:
            self.state = 5

    def handle_endtag(self, tag):
        if tag == "small" and self.state == 6:
            self.state = 7
        elif tag == "li" and self.state == 7:
            self.state = 1
            self.data.append(self.current)
            self.current = ICampusCourse()

    def handle_data(self, data):
        if self.state == 3:
            self.current.name = data
            self.state = 4
        elif self.state == 5:
            self.current.author = data
            self.state = 6


#<tbody>
#<tr>
#    <td>
#        NOME
#        <br />
#        <small>
#            <a href="..."> AUTORE </a>
#        </small>
#    </td>
#    <td valign="top">
#        { SE NON ISCRITTO }
#        <a href="/claroline/auth/courses.php?cmd=exReg&course=CODICE">
#            <img src="/claroline/img/enroll.gif" border="0" alt="Iscrizione"/>
#        </a>
#        { SE ISCRITTO }
#        <span class="highlight">Gia' iscritto</span>
#    </td>
#</tr>
#</tbody>


class SearchCorsiParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.regex = re.compile("(?<=course=)\S+&?")

    def reset(self):
        HTMLParser.reset(self)
        # lista corsi
        self.data = []
        # il corso corrente
        self.current = ICampusCourse()
        # lo stato
        self.state = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tbody" and self.state == 0:
            self.state = 1
        elif tag == "tr"and self.state == 1:
            self.state = 2
        elif tag == "td"and self.state == 2:
            self.state = 3
        elif tag == "small"and self.state == 4:
            self.state = 5
        elif tag == "a"and self.state == 5:
            self.state = 6
        elif tag == "td"and self.state == 8:
            self.state = 9
        elif tag == "a"and self.state == 9:
            self.state = 10
            code = re.search(self.regex, attrs["href"]).group(0)
            self.current.code = code
        elif tag == "span" and self.state == 9:
            self.state = 10

    def handle_endtag(self, tag):
        if tag == "td" and self.state == 7:
            self.state = 8
        elif tag == "tr" and self.state == 10:
            if self.current.code:
                self.data.append(self.current)
            self.state = 1
            self.current = ICampusCourse()

    def handle_data(self, data):
        if self.state == 3:
            self.current.name = data
            self.state = 4
        elif self.state == 6:
            self.current.author = data
            self.state = 7
