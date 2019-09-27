from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import odoorpc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://quocanh:123@localhost/flask-blog'
db = SQLAlchemy(app)

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=8069)

# Check available databases
print(odoo.db.list())

# Login
odoo.login('flask-blog', 'admin', 'admin')


@app.route("/")
@app.route("/home")
def home():
    posts = odoo.env['post'].search([])
    posts.sort(reverse=True)
    post = odoo.execute('post', 'read', posts)
    return render_template('home.html', post=post)


@app.route("/detail/<int:id>")
def post_detail(id):
    post = odoo.env['post'].browse(id)
    return render_template('detail.html', post=post)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
