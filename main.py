from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from helpers import *
import cgi

 


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
 
app.secret_key = "y337kGcys&zP3B"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10))
    password = db.Column(db.String(20))    
    blogs = db.relationship("Blog", backref="owner")
    
    def __init__(self, user_name, password):
        self.user_name=user_name  
        self.password=password
         
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    removed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, removed, owner):
        self.title = title
        self.body = body
        self.removed = removed
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ["login", "signup", "index", "newpost", "reqs"]
    if request.endpoint not in allowed_routes: # and "email" not in session:  must add later
        # return redirect("/login")
        return redirect("login")




@app.route('/', methods=['POST', 'GET'])
def index():
    return  redirect("/Blog")

@app.route("/Reqs", methods = ["GET", "POST"])
def reqs():
  return render_template("input_req.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():

     if request.method == "POST":
         input_error = False
         un_message = ""
         pw_message = ""
         vp_message = ""
          
     
         user_Name = cgi.escape(request.form["user_name"], quote = True)
         p_Word = cgi.escape(request.form["p_word"], quote = True)
         ver_P_Word = cgi.escape(request.form["ver_password"],quote = True)
     
         if check_user_name(user_Name) == False:
            un_message =  "That is not a valid username"
            input_error = True

         if check_pass_word(p_Word ) == False:
            pw_message =     "That is not a valid password"
            input_error = True
     
         if verify_pass_word(p_Word, ver_P_Word) == False:
            vp_message =   "The passwords do not match"
            input_error = True

         if input_error:
            
            return render_template("signup.html" , un_error = un_message, pw_error = pw_message, vp_error = vp_message, uName = user_Name )
         else:

            existing_user=User.query.filter_by(user_name=user_Name).first()
            
            if not existing_user:
                 new_user=User(user_Name,p_Word)
                 db.session.add(new_user)
                 db.session.commit()
                 session["user_name"] = user_Name
                  
                 return redirect("/newpost" )
            else:
                 flash("User ID already exists", "error")  
     
     return  render_template("signup.html" )


@app.route('/login', methods=['POST', 'GET'])
def login():
    return  render_template("login.html")


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return  redirect("/Blog")






@app.route('/Blog', methods=['POST', 'GET'])
def blog():

    # post = Blog.query.all()
    #post = Blog.query.order_by(Blog.id.desc()).all()
    page_title = "Build-a-Blog"
    post = Blog.query.filter_by(removed = False).order_by(Blog.id.desc()).all()
    return render_template('blog.html',title="Blogs R Us!", 
        post=post, page_title = page_title)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    owner = User.query.filter_by(user_name = session["user_name"]).first()
    if request.method == 'POST':
        add_body = request.form['body']
        add_title = request.form['title']
        user_name = request.form['user_name']
        add_removed = False
        new_post = Blog(add_title,add_body, add_removed)
        db.session.add(new_post)
        db.session.commit()

    else: 
        return render_template('add_new_post.html',title="Blogs R Us!", page_title = "new post")

    # post = Blog.query.all()
    #post = Blog.query.order_by(Blog.id.desc()).all()
    post = Blog.query.filter_by(removed = False).order_by(Blog.id.desc()).all()
    
    return render_template("blog.html",title="Blogs R Us!", post=post, page_title = "new post")
    



@app.route('/show_post', methods=['POST', 'GET'])
def post():
    post_title = request.args.get("post_title")
    post_body = request.args.get("post_body")
    #post = Blog.query.get(post_id)
    #title = post.title
    #body = post.body"""
   
    return render_template('show_post.html', post_title= post_title, post_body=post_body )
    

@app.route('/remove_post', methods=['POST'])
def remove_post(): 

    post_id = int(request.form['post_id'])
    post = Blog.query.get(post_id)
    post.removed = True
    db.session.add(post)
    db.session.commit()

    removed_post = Blog.query.get(post_id)
    removed_post_title = removed_post.title
    removed_post_body = removed_post.body
    return render_template('/remove_post.html', removed_post_title=removed_post_title,removed_post_body=removed_post_body, page_title = "Archived Post" )

@app.route('/archives', methods=['POST', 'GET'])
def archives():

    # post = Blog.query.all()
    #post = Blog.query.order_by(Blog.id.desc()).all()
    archived_post = Blog.query.filter_by(removed = True).order_by(Blog.id.desc()).all()
    return render_template('archived_posts.html',title="Blogs R Us!", 
        archived_post=archived_post, page_title = "Archived Posts")



if __name__ == '__main__':
    app.run()