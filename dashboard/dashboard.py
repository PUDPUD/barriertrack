from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://casper:heelsterk1@localhost/logging'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 
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




#rapporten van elk uur PDF
def piechart_elk_uur():
    nu_tijd = datetime.now()
    vorige_uur = nu_tijd - 1
    


@app.route('/rapporten')
def rapporten():
    
    return render_template('rapporten.html')


#Functie voor het generern van piechats van het laatste uur

if __name__ == "__main__":
    app.run(port=2003, host="0.0.0.0", debug=True)
