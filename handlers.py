import tornado.web
import db
from pocket import *


#*********************** global *******************
month = {
    "01": "JAN",
    "02": "FEB",
    "03": "MAR",
    "04": "APR",
    "05": "MAY",
    "06": "JUN",
    "07": "JUL",
    "08": "AUG",
    "09": "SEP",
    "10": "OCT",
    "11": "NOV",
    "12": "DEC"
}


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        entries = db.getRecentPosts()
        self.render("home.html", entries=entries)


class PostHandler(tornado.web.RequestHandler):
    '''show a post'''
    def get(self, link):
        '''Show a post by title.
        '''
        links = link.split('/')
        title = links[1].encode('utf-8')
        try:
            entry = db.getPost(title)
            self.render('post.html', entry=entry)
        except:
            self.render('error.html', info='no such page.')

#    # TODO a preview function, post an entry to post.html, show it
#    def post(self):
#        title = self.get_argument('title').encode('utf-8')
#        catagory = self.get_argument('catagory').encode('utf-8')
#        tag = self.get_argument('tag', '').encode('utf-8')
#        md = self.get_argument('markdown', '').encode('utf-8')
#        html = markdown.markdown(md).encode('utf-8')
#        entry = db.Entry()
#        entry.title = title
#        entry.html = html
#        entry.markdown = md
#        entry.catagory = catagory
#        entry.tag = tag
#        self.render('post.html', entry=entry)


class ArchivesHandler(tornado.web.RequestHandler):
    '''show all posts'''
    def get(self, url):
        now = self.get_argument('page', None)
        if not now:
            now = 0
        entries, total = db.getPosts(now)
        self.render('archives.html',
                    entries=entries,
                    total=total,
                    now=int(now),
                    month=month)


class CatagoryHandler(tornado.web.RequestHandler):
    '''Show all posts in a catagory'''
    def get(self, url):
        name = self.get_argument('name').encode('utf-8')
        if not name:
            name = '1'
        now = self.get_argument('page', None)
        if not now:
            now = 0
        entries, total = db.getPostsByCatagory(name, int(now))
        try:
            catagories = db.getCatagories()
            self.render('catagories.html',
                        entries=entries,
                        now=int(now),
                        total=total,
                        month=month,
                        catagories=catagories)
        except:
            self.write('bad boy')


class AboutHandler(tornado.web.RequestHandler):
    '''about page'''
    def get(self):
        self.render('about.html')


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        '''Login function, the username and password is seted here'''
        if self.get_argument('username').encode('utf-8') == 'ty'\
        and self.get_argument('password').encode('utf-8') == 'bfstheworld':
            self.set_secure_cookie('user', 'ty')
            self.redirect('/admin')
        else:
            self.write('bad boy!')

class AdminBase(tornado.web.RequestHandler):
    '''the base class for all admin page'''
    def get_current_user(self):
        return self.get_secure_cookie('user')


class AdminMainHandler(AdminBase):
    '''show the admin main page, all post and add delete edit function'''
    @tornado.web.authenticated
    def get(self, link):
        operation = self.get_argument('operation', None)
        title = self.get_argument('title', None)
        if operation is None or title is None:
            page = self.get_argument('page', None)
            if page is None:
                page = 0
            page = int(page)
            entries, total = db.getPosts(page)
            self.render('admin.html', entries=entries, total=total, now=page)
        elif operation == 'del':
            try:
                db.deletePost(title.encode('utf-8'))
                self.write('delete ok<br><a href="/admin">return</a>')
            except:
                self.write('some thing wrong with the deletion<br><a href="/admin">return</a>')


class NewPostHandler(AdminBase):
    @tornado.web.authenticated
    def post(self):
        title = self.get_argument('title')
        catagory = self.get_argument('catagory')
        tag = self.get_argument('tag', '')
        md = self.get_argument('markdown', '')
        html = markdown.markdown(md)
        entry = db.Entry()
        entry.title = title.encode('utf-8')
        entry.html = html.encode('utf-8')
        entry.markdown = md.encode('utf-8')
        entry.catagory = catagory.encode('utf-8')
        entry.tag = tag.encode('utf-8')
        db.NewPost(entry)
#        try:
#            db.NewPost(entry)
#            self.write('ok')
#        except:
#            self.render('error.html', info='new post failed')

    @tornado.web.authenticated
    def get(self):
        self.render('newpost.html')


class EditPostHandler(AdminBase):
    @tornado.web.authenticated
    def get(self, link):
        title=self.get_argument('title').encode('utf-8')
        try:
            entry = db.getPost(title)
            self.render('edit.html', entry=entry)
        except:
            self.write('bad boy')

    @tornado.web.authenticated
    def post(self, wht):
        old_title = self.get_argument('old')
        title = self.get_argument('title')
        catagory = self.get_argument('catagory')
        tag = self.get_argument('tag', '')
        md = self.get_argument('markdown', '')
        html = markdown.markdown(md)
        entry = db.Entry()
        entry.title = title.encode('utf-8')
        entry.html = html.encode('utf-8')
        entry.markdown = md.encode('utf-8')
        entry.catagory = catagory.encode('utf-8')
        entry.tag = tag.encode('utf-8')
        try:
            db.updatePost(entry,old_title.encode('utf-8'))
            self.write('ok')
        except:
            self.render('error.html', info='new post failed')


############################ test ############

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        import pylibmc
        client = None
        try:
            client = pylibmc.Client()
        except:
            client = pylibmc.Client(["127.0.0.1"], binary=True)
        key = 'select  '
        value = (1,2,3,4)
        client.set(key, value)
        self.write("yes")


########################### google #################

class GoogleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('googleafa84db2e7d78f11.html')
