            #### CONFFIGURE APP ####

from flask import Flask, request, redirect
from flask import render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogs:blogs@localhost:8889/blogs'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # pylint: disable=locally-disabled, invalid-name

#create secret key
app.secret_key = 'sdfasdfasdf'


            #### CLASSES ####

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String(26))
    blogs = db.relationship('Blog', backref='owner', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120))
    text = db.Column(db.Text)

    def __init__(self, name, text, owner_id):
        self.name = name
        self.text = text
        self.owner_id = owner_id


            #### ROUTES ####

@app.before_request
def requre_login():
    blocked_routes = ['newpost']
    if request.endpoint in blocked_routes and 'userId' not in session:
        return redirect('login')

# Working
@app.route('/', methods=['GET', 'POST'])
def index():
    print(session)
    users = User.query.all()
    return render_template('index.html', title='Index', users=users)

# Working
@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():

    name_error = ''
    init_pass_error = ''
    ver_pass_error = ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['Password']
        verify = request.form['verify']

        if len(username) < 3 or len(username) > 16:
            name_error = 'Username must be between 3 and 16 characters long'

        if len(password) < 7 or len(password) > 26:
            init_pass_error = 'Password must be between 7 and 26 characters'

        if verify != password:
            ver_pass_error = 'Passwords do not match'

        if name_error == '' and init_pass_error == '' and ver_pass_error == '':
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['userId'] = new_user.id
            return redirect('/newpost')
        else:
            return render_template('sign-up.html', name_error=name_error, ver_pass_error=ver_pass_error, init_pass_error=init_pass_error, username=username)
    return render_template('sign-up.html')

# Working
@app.route('/login', methods=['POST', 'GET'])
def login():
    print(session)
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # "remember" that the user has logged in
            session['userId'] = user.id
            flash('logged in')
            return redirect('/blog')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            return redirect('/login')

    return render_template('login.html')


# Working
@app.route('/newpost', methods=['GET','POST'])
def newpost():
    print(session)
    if request.method == 'POST':
        blog_name = request.form['name']
        blog_text = request.form['text']
        user_id = session['userId']
        if blog_name == '' or blog_text == '':
            flash('Your blog post must have a title and body', 'error')
            return redirect('/newpost')
        else:
            new_blog = Blog(blog_name, blog_text, user_id)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')
    return render_template('newpost.html')

##### NOT WORKING #####
@app.route('/blog', methods=['GET', 'POST'])
def blog_home():
    print(session)
    ownerId = request.args.get('userId')
    blogs = Blog.query.filter_by(owner_id=ownerId).all()
    if len(blogs) < 1:
        blogs = Blog.query.all()   
        return render_template('blog-home.html', title='Home', blogs=blogs)
    return render_template('indv-user.html', title='Single User', blogs=blogs)

#Working
@app.route('/view-post')
def viewpost():
    print(session)
    blog_id = request.args.get('blogId')
    blog = Blog.query.filter_by(id=blog_id).first()
    return render_template('view-post.html', blog=blog)

# Working
@app.route('/logout')
def logout():
    print(session)
    del session['userId']
    return redirect('blog')


if __name__ == '__main__':
    app.run()