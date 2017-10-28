#### configure environment ####

from flask import Flask, request, redirect
from flask import render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # pylint: disable=locally-disabled, invalid-name

#create secret key
#app.secret_key = sdfasdfasdf


##### Classes ####
class Entry(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    text = db.Column(db.String(50000))

    def __init__(self, name, text):
        self.name = name
        self.text = text

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String(26))

    def __init__(self, name, text):
        self.username = username
        self.password = password

#### Routes ####
@app.route('/')
def to_mainpage():
    return redirect('/blog')


@app.route("/sign-up", methods=['POST'])
def validate_signin():

    name_error = ''
    init_pass_error = ''
    ver_pass_error = ''
    email_error = ''

    username = request.form['username']
    password = request.form['Password']
    verify = request.form['verify']
    email = request.form['email']

    if len(username) < 3 or len(username) > 12:
        name_error = 'Username must be between 3 and 12 characters long'

    if len(password) < 3 or len(password) > 16:
        init_pass_error = 'Password must be between 8 and 16 characters'

    if verify != password:
        ver_pass_error = 'Passwords do not match'

    if email != '': #if it's blank then it's fine
        if email.count('.') != 1 or email.count('@') != 1:
            email_error = 'Invalid email'

    if name_error == '' and init_pass_error == '' and ver_pass_error == '' and email_error == '':
        return redirect('/success')
    else:
        return render_template('sign-up.html', name_error=name_error, ver_pass_error=ver_pass_error, init_pass_error=init_pass_error, email_error=email_error, username=username)


@app.route('/blog')
def blog():
    entries = Entry.query.all()
    return render_template('blog-home.html', title='Home', entries=entries)


@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if request.method == 'POST':
        blog_name = request.form['name']
        blog_text = request.form['text']
        new_blog = Entry(blog_name, blog_text)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = new_blog.id
        return redirect('/blog')
        #return redirect('/view-post?id=' + entry_id)
    return render_template('newpost.html')


@app.route('/view-post')
def view_post():
    # TODO: 
    # Use get request to select correct post
    entry_id = request.args.get('id')
    entry_veiw = Entry.query.filter_by(id=entry_id).first()
    name = entry_veiw.name
    text = entry_veiw.text
    return render_template('view-post.html', name=name, text=text)


if __name__ == '__main__':
    app.run()
