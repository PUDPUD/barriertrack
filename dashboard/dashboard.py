from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://casper:heelsterk1@localhost/logging'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definieer je databasemodel
# https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates
class AuthLog(db.Model):
    __tablename__ = 'auth_log'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(), nullable=False)
    hostname = db.Column(db.String(), nullable=False)
    event_type = db.Column(db.String(), nullable=False)
    full_event = db.Column(db.String(), nullable=False)
    source_ip = db.Column(db.String(), nullable=False)

# Functie om de top 5 gebruikersnamen met de meeste inlogpogingen op te halen
def get_top_users():
    user_counts = db.session.query(AuthLog.user, db.func.count(AuthLog.user)).group_by(AuthLog.user).all()
    return [user_count[0] for user_count in user_counts], [user_count[1] for user_count in user_counts]

# Definieer de route voor de homepagina
@app.route('/')
def home():
    return render_template('home.html')

# Definieer de route voor het dashboard
@app.route('/dashboard')
def dashboard():
    logs = AuthLog.query.all()
    top_usernames, login_attempts = get_top_users()
    return render_template('dashboard.html', logs=logs, top_usernames=top_usernames, login_attempts=login_attempts)

if __name__ == "__main__":
    app.run(port=2003, host="0.0.0.0", debug=True)