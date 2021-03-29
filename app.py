from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_mail import Mail
import hashlib as has
from flask import session
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'E:\\Flask\\project2\\static\\dump'

app = Flask(__name__)
app.secret_key = 'super-secret-key'

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
    image = db.Column(db.String(50), nullable=True)
    image_caption = db.Column(db.String(255), nullable=True)
    
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
    if "email" in session:
        return render_template('dashboard.html', banner = "Dashboard", year = x.strftime("%Y"))
    else:
        return render_template('login.html')

@app.route("/dashboard", methods = ['GET','POST'])
def dashboard():
    if(request.method == 'POST'):
        email = request.form['email']
        password  = request.form['password']
        session["email"] = email
        sign = sign_in.query.filter_by(email = email).first()
                
        if sign.email == email and sign.password == password:   
            return render_template('dashboard.html',year = x.strftime("%Y"), banner = "Updte Dashboard")
        else:
            return render_template('login.html', status = "Password Failed!!")
             
@app.route("/view-more", methods = ['GET','POST'])
def view_more(): 
    p = posts.query.order_by(posts.sno).all()
    return render_template('others.html', posts = p,banner = "All Posts", year = x.strftime("%Y"))
        
@app.route('/update',methods = ['GET'])  
def update_post(): 
    sno = request.args.get('sno')
    p = posts.query.order_by(posts.sno).filter_by(sno = sno).first()
    return render_template('dashboard_update.html', posts = p, banner = "Update Dashboard", year = x.strftime("%Y"))

@app.route('/delete',methods = ['GET'])  
def delete_post(): 
        
@app.route("/submit1", methods=['GET','POST'])
def submit1():
    if (request.method == 'POST'):
        title = request.form['title']
        tagline  = request.form['tagline']
        content = request.form['content']
        slug = '-'.join(request.form['tagline'].split(" "))
        
        file = request.files['file']
        caption = request.form['file-caption']
        
        file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
        entry = posts(title = title,tagline = tagline, content = content, slug = slug,image = secure_filename(file.filename), image_caption = caption)
        db.session.add(entry)
        db.session.commit()
    return render_template('dashboard.html',status = "Data has saved")

@app.route("/submit2", methods=['GET','POST'])
def submit2():
    if (request.method == 'POST'):
        sno = request.form['sno']
        title = request.form['title']
        tagline  = request.form['tagline']
        content = request.form['content']
        caption = request.form['file-caption']
        
        #find row which will be modify soon
        post = posts.query.filter_by(sno = sno).first()
        post.title = title
        post.tagline = tagline
        post.content = content
        post.image_caption = caption
        db.session.commit()
        
        #return all row from table
        p = posts.query.order_by(posts.sno).all()
    return render_template('others.html', posts = p,banner = "All Posts", year = x.strftime("%Y"))


@app.route("/logout", methods = ['GET','POST'])
def logout():
    session.pop('email', None)
    return render_template('login.html')

@app.route("/post_details/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', post=post,banner = "post-bg.jpg", heading = "Post", heading_footer = "Tech Blog")

app.run()