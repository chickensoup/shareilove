from __future__ import with_statement
import time, os, urllib, hashlib, socket, sys
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash, secure_filename
import datetime

reload(sys) 
sys.setdefaultencoding('utf8') 

UPLOAD_FOLDER = 'static/avatar'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# configuration
DATABASE = 'sharei.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

# create our little application :)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)
app.config.from_envvar('SHAREI_SETTINGS', silent=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_user_id(email):
    """Convenience method to look up the id for a email."""
    rv = query_db('select bleaf_id from bleaf where email = ?',
                  [email], one=True)
    return rv[0] if rv else None

def get_user_engaged(bleaf_id):
    rv1 = query_db('select count(*) from raising where raising.bleaf_id = ?',
                  [bleaf_id], one=True)
    rv2 = query_db('select count(*) from applying where applying.bleaf_id = ?',
                  [bleaf_id], one=True)
    rv3 = query_db('select count(*) from donating where donating.bleaf_id = ?',
                  [bleaf_id], one=True)
    return int(rv1[0])+int(rv2[0])+int(rv3[0])

def bleaf_allowed_applying(bleaf_id):
    if get_user_engaged(bleaf_id) > 3:
        return False
    else:
        return True


def get_lleaf_id(lleaf_id):
    rv = query_db('select lleaf_id from lleaf where lleaf_id = ?',
                  [lleaf_id], one=True)
    return rv[0] if rv else None


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest())

@app.before_request
def before_request():
    g.bleaf = None
    if 'bleaf_id' in session:
        g.bleaf = query_db('select * from bleaf where bleaf_id = ?', [session['bleaf_id']], one=True)


@app.route('/')
def home():
    if 'bleaf_id' in session:
        g.bleaf = query_db('select * from bleaf where bleaf_id = ?', [session['bleaf_id']], one=True)
        return render_template('home.html', bleaf=g.bleaf)
    else:
	   return render_template('home.html')

@app.route('/news/<news_id>')
def show_news(news_id):
    if int(news_id) == 1 :
        return render_template('news1.html')
    else:
        return render_template('news2.html')

@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register the big leaf as new user"""
    error = None
    if request.method == 'POST':
        if not request.form['uname']:
            error = '请输入用户名'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = '请输入您的email地址'
        elif not request.form['password']:
            error = '请输入密码'
        elif request.form['password'] != request.form['password2']:
            error = '两次输入密码不一致'
        elif get_user_id(request.form['email']) is not None:
            error = '该邮箱已被注册'
        else:
            db = get_db()
            db.execute('insert into bleaf ( \
                email, avatar, uname, sex, ulevel, password, createtime) \
                values (?, ?, ?, ?, ?, ?, ?)', [request.form['email'], \
                gravatar_url(request.form['email'], 80), request.form['uname'], request.form['sex'], \
                0, generate_password_hash(request.form['password']), datetime.datetime.now()])
            db.commit()
            flash('注册成功！转向登陆页面...')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logins the user in as big leaf"""
    if g.bleaf:
        return redirect(url_for('home'))
    error = None    
    if request.method == 'POST':
        user = query_db('''select * from bleaf where
            email = ?''', [request.form['email']], one=True)
        if user is None:
            error = '不存在这个email的注册信息'
        elif not check_password_hash(user['password'],
                                     request.form['password']):
            error = '密码不正确'
        else:
            flash('正在登陆...')
            session['bleaf_id'] = user['bleaf_id']
            session['logged_in'] = True
            session['bleaf_name'] = user['uname']
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('bleaf_id', None)
    session.pop('bleaf_name', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/littleleaf')
def show_littleleafs():
    littleleafs = query_db('''select * from lleaf''')
    error = None
    if littleleafs is None:
        error = 'No little leaf now'
        return render_template('littleleaf.html', error=error)
    else:
        return render_template('littleleaf.html', error=error, littleleafs = littleleafs)

@app.route('/littleleaf/<lleaf_id>', methods=['GET', 'POST'])
def show_littleleaf(lleaf_id):
    littleleaf = query_db('select * from lleaf where lleaf.lleaf_id = ?', [lleaf_id], one=True)
    error = None

    if littleleaf is None:
            error = 'Invalid little leaf id'
            return render_template('littleleaf.html', error=error)

    blogs = query_db('select blog.blog_id as blog_id, blog.bleaf_id as bleaf_id, blog.lleaf_id as lleaf_id, blog.title as title, \
                blog.blogtext as blogtext, bleaf.avatar as avatar, bleaf.uname as uname , blog.createtime as createtime \
                from blog join bleaf on blog.bleaf_id = bleaf.bleaf_id where blog.lleaf_id = ? order by blog.createtime desc', [lleaf_id])
    donaters = query_db('select donating.bleaf_id, bleaf.avatar, bleaf.uname from donating join bleaf on donating.bleaf_id = bleaf.bleaf_id where donating.lleaf_id = ?', [lleaf_id])
    raiser = query_db('select raising.bleaf_id as bleaf_id, bleaf.avatar as avatar, bleaf.uname as uname from raising join bleaf on raising.bleaf_id = bleaf.bleaf_id where raising.lleaf_id = ?', [lleaf_id], True)
    applyers = query_db('select applying.bleaf_id, bleaf.avatar, bleaf.uname from applying join bleaf on applying.bleaf_id = bleaf.bleaf_id where applying.lleaf_id = ?', [lleaf_id])

    allowed_raiser = False
    allowed_applyer = False
    indonaters = False
    inapplyers = False

    if 'bleaf_id' not in session:
        loggedin = False
    else:
        loggedin = True

        if (query_db('select bleaf_id from raising where bleaf_id = ?', [session['bleaf_id']], True) is None) and bleaf_allowed_applying(session['bleaf_id']):
            allowed_raiser = True

        if (query_db('select bleaf_id from applying where bleaf_id = ?', [session['bleaf_id']], True) is None) and bleaf_allowed_applying(session['bleaf_id']):
            allowed_applyer = True

        if query_db('select bleaf_id from donating where bleaf_id = ? and lleaf_id = ?', [session['bleaf_id'], lleaf_id], True) is not None:
            indonaters = True
        
        if query_db('select bleaf_id from applying where bleaf_id = ? and lleaf_id = ?', [session['bleaf_id'], lleaf_id], True) is not None:
            inapplyers = True

        return render_template('littleleaf_timeline.html', littleleaf=littleleaf, blogs=blogs, donaters=donaters, raiser=raiser, applyers=applyers, indonaters=indonaters, inapplyers=inapplyers, allowed_raiser=allowed_raiser, allowed_applyer=allowed_applyer)

    return render_template('littleleaf_timeline.html', littleleaf=littleleaf, blogs=blogs, donaters=donaters, raiser=raiser, applyers=applyers, indonaters=indonaters, inapplyers=inapplyers, allowed_raiser=allowed_raiser, allowed_applyer=allowed_applyer)

@app.route('/littleleaf/<lleaf_id>/add_blog', methods=['GET', 'POST'])
def add_blog(lleaf_id):
    error = None
    if request.method == 'POST':
        if not request.form['blogtitle']:
            error = '请输入日志标题'
            return redirect( url_for('show_littleleaf', lleaf_id=lleaf_id))
        elif not request.form['blogtext']:
            error = '请输入日志内容'
        else:
            db = get_db()
            db.execute('insert into blog ( \
                title, blogtext, bleaf_id, lleaf_id, createtime) \
                values (?, ?, ?, ?, ?)', [request.form['blogtitle'], \
                request.form['blogtext'], session['bleaf_id'], lleaf_id, datetime.datetime.now()])
            db.commit()
            flash('日志提交成功！')
            return redirect( url_for('show_littleleaf', lleaf_id=lleaf_id))


@app.route('/littleleaf/<lleaf_id>/raise')
def raise_leaf(lleaf_id):
    """Adds the current user as raise of the given user."""
    if not 'logged_in' in session:
        return redirect(url_for('login'))
    whom_id = get_lleaf_id(lleaf_id)
    if whom_id is None:
        abort(404)
    db = get_db()
    error = None

    bcount = get_user_engaged( int(session['bleaf_id']) )
    inraisers = query_db('select bleaf_id from raising where bleaf_id = ?', [session['bleaf_id']], True)
    inapplyers = query_db('select bleaf_id from applying where bleaf_id = ?', [session['bleaf_id']], True)

    if query_db('select bleaf_id from raising where bleaf_id = ?', [session['bleaf_id']], True) is None and bleaf_allowed_applying(session['bleaf_id']):
        db.execute('insert into raising (bleaf_id, lleaf_id, createtime) values (?, ?, ?)', [ int(session['bleaf_id']), int(lleaf_id), datetime.datetime.now() ] )
        db.commit()
        db.execute('update lleaf set status = 2 where lleaf.lleaf_id = ?', [lleaf_id])
        db.commit()
        flash('申请捐助成功！')
    else:
        error  = '您不能申请捐助这枚小叶子'
        flash('您不能申请捐助这枚小叶子')

    return redirect(url_for('show_littleleaf', lleaf_id=lleaf_id))

@app.route('/littleleaf/<lleaf_id>/apply')
def apply_leaf(lleaf_id):
    """Adds the current user as raise of the given user."""
    error = None
    if not 'logged_in' in session:
        return redirect(url_for('login'))
    whom_id = get_lleaf_id(lleaf_id)
    if whom_id is None:
        abort(404)
    db = get_db()

    if query_db('select bleaf_id from applying where bleaf_id = ?', [session['bleaf_id']], True) is None and bleaf_allowed_applying(session['bleaf_id']):
        """raised, can only apply for the liffle leaf"""
        db.execute('insert into applying (bleaf_id, lleaf_id, createtime) values (?, ?, ?)', [ int(session['bleaf_id']), int(lleaf_id), datetime.datetime.now() ] )
        db.commit()
        flash('申请加入捐助成功！')
    else:
        error  = '您不能再申请捐助更多的小叶子了'
        flash('您不能再申请捐助更多的小叶子了')
    
    return redirect(url_for('show_littleleaf', lleaf_id=lleaf_id))

@app.route('/bigleaf')
def show_bigleafs():
    bigleafs = query_db('''select * from bleaf''')
    error = None
    if bigleafs is None:
        error = 'No big leaf now'
        return render_template('bigleaf.html', error=error)
    else:
        return render_template('bigleaf.html', error=error, bigleafs = bigleafs)

@app.route('/bigleaf/<bleaf_id>')
def show_bigleaf(bleaf_id):
    bigleaf = query_db('select * from bleaf where bleaf.bleaf_id = ?', [bleaf_id], one=True)
    if bigleaf is None:
        error = 'Invalid big leaf id'
        return render_template('home.html', error=error)

    blogs = query_db('select * from blog where blog.bleaf_id = ?', [bleaf_id])

    if session['bleaf_id'] == bleaf_id:
        bleaf_self = True
    else:
        bleaf_self = False

    raise_raisebleaf = query_db('select bleaf_id, avatar, uname from bleaf where bleaf_id = ?', [bleaf_id], True)
    raise_lleaf = query_db('select lleaf.lleaf_id as lleaf_id, lleaf.avatar as avatar, lleaf.lnickname from raising join lleaf on raising.lleaf_id = lleaf.lleaf_id where raising.bleaf_id = ?', [bleaf_id], False)
    if raise_lleaf is None:
        raise_applybleafs
    else:
        raise_applybleafs = query_db('select bleaf.bleaf_id, bleaf.uname, bleaf.avatar from applying join bleaf on applying.bleaf_id = bleaf.bleaf_id where applying.lleaf_id = ?', [raise_lleaf.lleaf_id], False)

    apply_lleaf = query_db('select lleaf.lleaf_id, lleaf.avatar, lleaf.uname from applying join lleaf on applying.lleaf_id = lleaf.lleaf_id where raising.bleaf_id = ?', [bleaf_id], True)
    if apply_lleaf is None:
        apply_raisebleaf = None
        apply_applybleafs = None
    else:
        apply_raisebleaf = query_db('select bleaf_id.bleaf_id, bleaf_id.avatar, bleaf_id.uname from bleaf join raising on bleaf.bleaf_id = raising.bleaf_id where raising.leaf_id = ?', [apply_lleaf.lleaf_id], True)
        apply_applybleafs = query_db('select bleaf.bleaf_id, bleaf.uname, bleaf.avatar from applying join bleaf on applying.bleaf_id = bleaf.bleaf_id where applying.lleaf_id = ?', [apply_lleaf.lleaf_id], False)

    return render_template('bigleaf_timeline.html', bigleaf=bigleaf, bleaf_self=bleaf_self, raise_raisebleaf=raise_raisebleaf, raise_llea=raise_lleaf, raise_applybleafs=raise_applybleafs, apply_lleaf=apply_lleaf, apply_raisebleaf=apply_raisebleaf, apply_applybleafs=apply_applybleafs)

@app.route('/blog/<blog_id>')
def show_blog(blog_id):
    blog = query_db('select * from blog where blog.blog_id = ?', [blog_id], one=True)
    if blog is None:
        error = '不存在此日志'
        return render_template('littleleaf.html', error=error)

    return render_template('blog.html', blog=blog)

@app.route('/add_littleleaf', methods=['GET', 'POST'])
def add_littleleaf():
    """Add new little leaf"""
    error = None
    if request.method == 'POST':
        if not request.form['lname']:
            error = '请输入小叶子的名字'
        else:
            db = get_db()
            db.execute('insert into lleaf (lname, lnickname, gender, nationality, age, grade, bday, constellation, school, homeaddress, phone, homeinfo, linfo, \
                        ginfo, gadvice, gname, gschool, gbackground, ginfosource, grr, gweibo, gkaixin, status, createtime) \
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', \
                [request.form['lname'], request.form['lnickname'], request.form['gender'], request.form['nationality'], request.form['age'],\
                request.form['grade'], request.form['bday'], request.form['constellation'], \
                request.form['school'], request.form['homeaddress'], request.form['phone'], request.form['homeinfo'], \
                request.form['linfo'], request.form['ginfo'], request.form['gadvice'], request.form['gname'], \
                request.form['gschool'], request.form['gbackground'], request.form['ginfosource'], request.form['grr'], request.form['gweibo'], request.form['gkaixin'], 1, datetime.datetime.now()])
            db.commit()
            flash('Little leaf added!')
            return redirect(url_for('show_littleleafs'))
    return render_template('add_littleleaf.html', error=error)


if __name__ == '__main__':
    #app.debug = True
    #app.run()
    app.run('0.0.0.0', port=8080)
