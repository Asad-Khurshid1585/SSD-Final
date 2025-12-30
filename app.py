from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.id} {self.first_name}>"

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    age = request.form['age']
    city = request.form['city']
    new_user = User(first_name=first_name, last_name=last_name, email=email, age=age, city=city)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.age = request.form['age']
        user.city = request.form['city']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
