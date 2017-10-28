#### configure environment ####

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
#app.secret_key = sdfasdfasdf


##### Classes ####
class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String(26))
    blogs = db.relationship('Blog', backref='User', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120))
    text = db.Column(db.Text)

    def __init__(self, name, text):
        self.name = name
        self.text = text


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
            return redirect('/newpost')
        else:
            return render_template('sign-up.html', name_error=name_error, ver_pass_error=ver_pass_error, init_pass_error=init_pass_error, username=username)
    return render_template('sign-up.html')

@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if request.method == 'POST':
        blog_name = request.form['name']
        blog_text = request.form['text']
        new_blog = Blog(blog_name, blog_text)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = new_blog.id
        return redirect('/blog')
        #return redirect('/view-post?id=' + entry_id)
    return render_template('newpost.html')


@app.route('/blog')
def blog_home():
    blogs = Blog.query.all()
    return render_template('blog-home.html', title='Home', blogs=blogs)


if __name__ == '__main__':
    app.run()