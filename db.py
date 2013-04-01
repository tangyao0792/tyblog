import MySQLdb
import pylibmc
from sae.const import MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, \
    MYSQL_USER, MYSQL_PASS, MYSQL_DB
from base64 import encodestring

# memcache connection
try:
    mc = pylibmc.Client()       # on sae
except:
    mc = pylibmc.Client(["127.0.0.1"], binary=True)

# class for format html template code
class Entry:
    def __init__(self):
        self.title = ''
        self.html = ''
        self.markdown = ''
        self.time = ''
        self.catagory = ''
        self.tag = ''
        self.count = 0


def ConnectDatabase():
    try:
        conn = MySQLdb.connect('localhost', 'root', 'helloworld', 'test')
    except:
        conn = MySQLdb.connect(MYSQL_HOST,MYSQL_USER,MYSQL_PASS,
            MYSQL_DB,port=int(MYSQL_PORT))
    return conn

# global varible
conn = ConnectDatabase()
cursor = conn.cursor()


def sqlMemcache(func):
    '''Decorator for select data from database.'''
    def __wrapper(sql):
        sqlKey = encodestring(sql)
        results = None
        if sql.startswith('select') and sqlKey in mc:
            results = mc[sqlKey]
            #print 'memcache hit'
            #print sqlKey
            #print sql
        else:
            results = func(sql)
            mc.set(sqlKey, results)
        return results
    return __wrapper
        

@sqlMemcache
def executeSql(sql):
    '''Execute the sql sentence, commit to database, return query result.'''
    global conn, cursor
    # ensure the db connection is alive
    try:
        cursor.execute('show tables;')
    except:
        # connection die
        conn = ConnectDatabase()
        cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return cursor.fetchall()


def formatResultToEntry(result):
    entry = Entry()
    entry.title = result[1]
    entry.html = result[2]
    entry.markdown = result[3]
    entry.time = str(result[4])
    entry.catagory = result[5]
    entry.tag = result[6]
    entry.count = result[7]
    return entry
 

def NewPost(entry):
    sql = 'insert into post (title, html, markdown, catagory, tag, count, time)' \
          'values ("%s", "%s", "%s", "%s", "%s", 0, now())' % \
          (
            MySQLdb.escape_string(entry.title),
            MySQLdb.escape_string(entry.html),
            MySQLdb.escape_string(entry.markdown),
            MySQLdb.escape_string(entry.catagory),
            MySQLdb.escape_string(entry.tag)
          )
    executeSql(sql)


def updatePost(entry, title):
    sql = 'update post set title = "%s", html = "%s", markdown = "%s", catagory = "%s", tag = "%s"' \
          'where title = "%s";' % \
          (
            MySQLdb.escape_string(entry.title),
            MySQLdb.escape_string(entry.html),
            MySQLdb.escape_string(entry.markdown),
            MySQLdb.escape_string(entry.catagory),
            MySQLdb.escape_string(entry.tag),
            MySQLdb.escape_string(title)
          )
    executeSql(sql)


def getRecentPosts():
    sql = 'select * from post order by id desc limit 5;'
    results = executeSql(sql)
    entries = []
    for result in results:
        entry = formatResultToEntry(result)
        entries.append(entry)
    return entries


def getPost(title):
    title = MySQLdb.escape_string(title)
    sql = 'select * from post where title = "%s";' % title
    result = executeSql(sql)[0]
    entry = formatResultToEntry(result)
    # update page view counter
    sql = 'update post set count = %s where title = "%s";' \
                   % (str(entry.count + 1), title)
    executeSql(sql)
    return entry


def getPosts(page):
    sql = 'select title, catagory, time from post order by id desc;'
    results = executeSql(sql)
    total = len(results)
    frm = int(page) * 10
    to = min(frm + 10, total)
    results = results[frm: to]
    entries = []
    for result in results:
        entry = Entry()
        entry.title = result[0]
        entry.time = str(result[2])
        entry.catagory = result[1]
        entries.append(entry)
    return entries, (total - 1) / 10  # number of total pages


def getPostsByCatagory(catagory, now):
    catagory = MySQLdb.escape_string(catagory)
    sql = 'select title, catagory, time from post where catagory = "%s" order by id desc;'\
        % catagory
    results = executeSql(sql)
    total = len(results)
    frm = now * 10
    to = min(frm + 10, total)
    results = results[frm: to]
    entries = []
    for result in results:
        entry = Entry()
        entry.title = result[0]
        entry.time = str(result[2])
        entry.catagory = result[1]
        entries.append(entry)
    return entries, (total-1) / 10


def getCatagories():
    catagories = {}
    sql = 'select catagory from post;'
    results = executeSql(sql)
    for result in results:
        if not result[0] in catagories:
            catagories[result[0]] = 0
        catagories[result[0]] = catagories[result[0]] + 1
    return catagories


def deletePost(title):
    '''delete post by title'''
    global conn, cursor
    if isDBConnecting() is False:
        conn = ConnectDatabase()
        cursor = conn.cursor()
    title = MySQLdb.escape_string(title)
    sql = 'delete from post where title = "%s";' % title
    executeSql(sql)

########################## notepad used ############################
def getTextByUrl(url):
    url = MySQLdb.escape_string(url)
    sql = 'select * from text where url = "%s";' % url
    return executeSql(sql)


def saveText(url, content):
    url = MySQLdb.escape_string(url)
    content = MySQLdb.escape_string(content)
    sql = 'select * from text where url = "%s";' % url
    result = executeSql(sql)
    if result is None:
        sql = 'insert into text (content, url) values ("%s", "%s")' % (content, url)
    else:
        sql = 'update text set content = "%s", time = now() where url = "%s";' %(content, url)
    executeSql(sql)


def getRecentText():
    sql = 'select * from text order by time desc limit 50;'
    results = executeSql(sql)
    texts = []
    for t in results:
        arr = []
        arr.append(t[1])    # content
        arr.append(t[2])    # time
        arr.append(t[3])    # url
        texts.append(arr)
    return texts
