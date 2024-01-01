from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mymodel.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    users = User.query.all()
    return render_template('tmp.html', users=users)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user is None:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        users = User.query.all()
        return render_template('tmp.html', users=users)
    else:
        return 'User with email already exists!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
