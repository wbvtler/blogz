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


#### Routes ####
@app.route('/')
def to_mainpage():
    return redirect('/blog')

@app.route('/blog')
def blog():
    entries = Entry.query.all()
    return render_template('blog-home.html', title='Home', entries=entries)

@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if request.method == 'POST':
        entry_name = request.form['name']
        entry_text = request.form['text']
        new_entry = Entry(name=entry_name, text=entry_text)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/blog')
    return render_template('newpost.html')

@app.route('/view-post')
def view_post():
    # TODO: 
    # Use get request to select correct post
    return render_template('view-post.html')


if __name__ == '__main__':
    app.run()
