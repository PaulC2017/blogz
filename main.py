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
    body = db.Column(db.String(255))
    removed = db.Column(db.Boolean)

    def __init__(self, title, body, removed):
        self.title = title
        self.body = body
        self.removed = removed


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        add_body = request.form['body']
        new_body = Blog(add_body)
        db.session.add(new_body)
        db.session.commit()

    post = Blog.query.all()
     
    return render_template('add_new_post.html',title="Blogs R Us!", 
        post=post)


@app.route('/remove-post', methods=['POST'])
def remove_post():

    post_id = int(request.form['post-id'])
    post = Blog.query.get(post_id)
    post.removed = True
    db.session.add(post.removed)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()