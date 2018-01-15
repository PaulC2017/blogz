from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    removed = db.Column(db.Boolean)

    def __init__(self, title, body, removed):
        self.title = title
        self.body = body
        self.removed = removed

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect("/Blog") 

@app.route('/Blog', methods=['POST', 'GET'])
def blog():

    # post = Blog.query.all()
    #post = Blog.query.order_by(Blog.id.desc()).all()
    post = Blog.query.filter_by(removed = False).order_by(Blog.id.desc()).all()
    return render_template('blog.html',title="Blogs R Us!", 
        post=post)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        add_body = request.form['body']
        add_title = request.form['title']
        add_removed = False
        new_post = Blog(add_title,add_body, add_removed)
        db.session.add(new_post)
        db.session.commit()

    else: 
        return render_template('add_new_post.html',title="Blogs R Us!")

    # post = Blog.query.all()
    #post = Blog.query.order_by(Blog.id.desc()).all()
    post = Blog.query.filter_by(removed = False).order_by(Blog.id.desc()).all()
    
    return render_template("blog.html",title="Blogs R Us!", post=post)
    



@app.route('/show_post', methods=['POST', 'GET'])
def post():
    post_title = request.args.get("post_title")
    post_body = request.args.get("post_body")
    #post = Blog.query.get(post_id)
    #title = post.title
    #body = post.body"""
   
    return render_template('show_post.html', post_title= post_title, post_body=post_body)
    

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
    return render_template('/remove_post.html', removed_post_title=removed_post_title,removed_post_body=removed_post_body  )


if __name__ == '__main__':
    app.run()