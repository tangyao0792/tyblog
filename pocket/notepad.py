import tornado.web
import db
import random


URL_CODE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
length = len(URL_CODE)


class NotepadHandler(tornado.web.RequestHandler):
    def get(self, url):
        if len(url) <= 1:
        # new random url
            rand_url = ''
            while True:
                rand_url = ''.join(random.choice(URL_CODE) for i in xrange(6))
                if not db.getTextByUrl(rand_url):
                    break
            if not url:
                url = '/'
            self.redirect('/pad' + url + rand_url)
        else:
        # get the url
            if url[1:] == 'show':
            # show recent text
                texts = db.getRecentText()
                html = '<html><head><meta http-equiv="Content-Type"content="text/html; charset=utf-8" /></head><body><table>'
                for t in texts:
                    line = '<tr><td><a href="%s">%s </a></td><td>%s</td></tr>'
                    l = min(len(t[0]), 12)
                    line = line % (t[2], t[0][0: l], t[1])
                    html = html + line
                html = html + '</table></body></html>'
                self.write(html)
                return
            text = db.getTextByUrl(url[1:])
            content = ''
            if text:
                content = text[1]
            self.render('pocket/pad.html', content=content, url=url[1:])

    def post(self, url):
        content = self.get_argument('content')
        content = content.encode('utf-8')
        db.saveText(url[1:], content)
        self.redirect('/pad' + url)
