from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import datetime



app = Flask(__name__)

#Create connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/blog'


db = SQLAlchemy(app)

class contacts(db.Model):
    u_sno = db.Column(db.Integer, primary_key=True)
    u_email = db.Column(db.String(255), nullable=True)
    u_name = db.Column(db.String(300), nullable=True)
    u_number = db.Column(db.Integer, nullable=True)
    u_message = db.Column(db.String(1000), nullable=True)
    
    
x = datetime.datetime.now()
    
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html',heading = "CodingThunder", heading_footer = "A tech blog", banner = "contact-bg.jpg",year = x.strftime("%Y"))

@app.route('/post', methods=["GET", "POST"])
def post():
    return render_template('post.html',heading = "Post", heading_footer = "A tech blog" , banner = "post-bg.jpg",year = x.strftime("%Y"))

@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('about.html',heading = "About", heading_footer = "A tech blog", banner = "about-bg.jpg",year = x.strftime("%Y"))

@app.route('/contact', methods=["GET", "POST"])
def contact():
    return render_template('contact.html',heading = "Contact", heading_footer = "A tech blog" ,banner = "home-bg.jpg",year = x.strftime("%Y"))


@app.route("/submit", methods = ['GET', 'POST'])
def save():
    if(request.method == 'POST'):
        email = request.form['email']
        name  = request.form['name']
        number = request.form['number']
        message = request.form['message']
        entry = contacts(u_email = email, u_name = name, u_number = number, u_message = message)
        db.session.add(entry)
        db.session.commit()
    return render_template('render.html', link = "/contact")

app.run()