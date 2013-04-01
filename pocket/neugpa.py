import tornado.web
import os
import urllib2
import urllib
import cookielib
import HTMLParser

html_parser = HTMLParser.HTMLParser()
    
def initialCookie():
    #set cookie
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)


def login(userid, password):
    ''' input username and pwd, return the html string after login'''
    xn = {}
    xn['WebUserNO'] = userid
    xn['Password'] = password

    info = urllib.urlencode(xn)
    request = urllib2.Request('http://202.118.31.197/ACTIONLOGON.APPPROCESS', info)
    response = urllib2.urlopen(request)
    request = urllib2.Request('http://202.118.31.197/ACTIONQUERYSTUDENTSCORE.APPPROCESS')
    response = urllib2.urlopen(request)
    html = response.read()
    return html


def selectYear(YearTermNO):
    xn = {}
    xn['YearTermNO'] = str(YearTermNO)
    info = urllib.urlencode(xn)
    request = urllib2.Request('http://202.118.31.197/ACTIONQUERYSTUDENTSCORE.APPPROCESS', info)
    response = urllib2.urlopen(request)
    return response.read()



def parseHTML(html):
    term = []
    first = 0
    cnt = 0
    while True:
        html = html[first+1:]
        first = html.find('row')
        tmp = html[first:]
        second = tmp.find('</tr>')
        if first == -1:
            break
        content = html[first : first + second]
        left = content.find('nbsp') + 5
        right = content[left:].find('<')
        lesson = content[left : left+right]
        lines = content.split('</td>')
        tmp = lines[len(lines)-2]
        left = tmp.find('p>')
        score = tmp[left + 2:]
        cnt = cnt + 1
        term.append((lesson, score))
    return term



class NeugpaHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join('neugpa', 'neugpa.html'))

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        year = self.get_argument('YearTermNO')
        initialCookie()
        login(username,password)
        html = selectYear(year)
        html = html.decode('gbk')
        term = parseHTML(html)
        self.write('<table>')

        for tup in term:
            self.write('<tr><td>%s</td><td>%s</td></tr>' % (tup[0], tup[1]))
        self.write('</table>')
