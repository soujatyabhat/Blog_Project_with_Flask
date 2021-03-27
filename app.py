from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_mail import Mail

app = Flask(__name__)


#Create connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/blog'



db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "candila.ppf105@gmail.com",
    MAIL_PASSWORD = "@soujatya123**"
)

mail = Mail(app)

class contacts(db.Model):
    u_sno = db.Column(db.Integer, primary_key=True)
    u_email = db.Column(db.String(255), nullable=True)
    u_name = db.Column(db.String(300), nullable=True)
    u_number = db.Column(db.Integer, nullable=True)
    u_message = db.Column(db.String(1000), nullable=True)
    
class posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    tagline = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    #img_file = db.Column(db.String(12), nullable=True)
    
class sign_in(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    
x = datetime.datetime.now()

    
@app.route('/', methods=["GET", "POST"])
def index():
    p = posts.query.order_by(posts.sno).all()[0:3]
    return render_template('index.html',heading = "CodingThunder", heading_footer = "A tech blog", banner = "contact-bg.jpg",year = x.strftime("%Y"),posts = p)

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
        mail.send_message('New message from ' + str(name),
                          sender = email,
                          recipients = ["candila.ppf105@gmail.com"],
                          body = message + "\n" + str(number)
                          )
    return render_template('render.html', link = "/contact")

@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
        if(request.method == 'POST'):
            email = request.form['email']
            password  = request.form['password']
            sign = sign_in.query.filter_by(email = email).first()
            
            if sign.email == email and sign.password == password:
                return render_template('dashboard.html',status = "Connected!!")
            else:
                return render_template('dashboard.html',status = "Disconnected!!")

@app.route("/post_details/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', post=post,banner = "post-bg.jpg", heading = post.title, heading_footer = post.tagline)

app.run()