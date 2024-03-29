import psycopg2
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from pathlib import Path

#variablen:
# directory van app bepalen:
APP_ROOT = os.path.dirname(os.path.abspath(__file__))  

#variablenfile inladen
dotenv_path = Path('../variables.env')
load_dotenv(dotenv_path=dotenv_path)

database_ip = os.getenv("DATABASE_IP")
database_DB = os.getenv("POSTGRES_DB")
database_user = os.getenv("POSTGRES_USER")
database_password = os.getenv("POSTGRES_PASSWORD")

print(database_ip, database_DB, database_user, database_password)



def logging_ophalen_groep(begin_tijd, eind_tijd, event_type, hostname):

    print(f"event_type: {event_type}, hostname: {hostname}, begin_tijd: {begin_tijd}, eind_tijd: {eind_tijd}")
    #sql query met variabeln van functie
    query = """
    SELECT "user", COUNT(*) AS failed_attempts
    FROM public.auth_log
    WHERE event_type = %s
    AND hostname =%s
    AND timestamp BETWEEN %s AND %s
    GROUP BY "user"
    ORDER BY failed_attempts DESC;
    """
    try:
        #maak de verbinding met de database
        conn = psycopg2.connect(
            host=database_ip,
            database=database_DB,
            user=database_user,
            password=database_password
        )
        cur = conn.cursor()
        print(f"Verbonden met de database {database_DB}")
        print(f"event_type: {event_type} hostname: {hostname} begin_tijd: {begin_tijd} eind_tijd: {eind_tijd}")
        print(f"query: {query}")
        #voer de query uit
        cur.execute(query, (event_type, hostname, begin_tijd, eind_tijd))

        #haal de resultaten op]
        resultaten = cur.fetchall()

        return resultaten
        print("Gebruikersnaam | Aantal mislukte inlogpogingen")
        for row in resultaten:
            print(f"{row[0]} | {row[1]}")
    except Exception as e:
        print(f"Er is iets mis gegaan {e}")
    finally: 
        if conn:
            conn.close()

def haal_laatste_x_records_op(x):
    sql_query = """ 
    SELECT timestamp, "user", source_ip, hostname, event_type, full_event
    FROM public.auth_log
    ORDER BY timestamp DESC
    LIMIT %s;

    """
    try:
        conn = psycopg2.connect(
            host=database_ip,
            database=database_DB,
            user=database_user,
            password=database_password
        )
        cur = conn.cursor()
        cur.execute(sql_query, (x,))
        resultaten = cur.fetchall()
        print(resultaten)
        return resultaten
    except Exception as e:
        print(f"Er is iets mis gegaan {e}")
    finally:
        if conn:
            conn.close()


# Voorbeeldgebruik van de functie
begin_tijd = '2023-03-25 12:00:00'
eind_tijd = '2024-03-29 19:00:00'
event_type = 'Failed password for invalid user'
hostname = ''

def maak_piechart(data):
    pad_naar_img = os.path.join(APP_ROOT, 'static/img/chart.png')
    gebruikersnamen = [rij[0] for rij in data]  # Extract gebruikersnamen
    mislukte_inlogpogingen = [rij[1] for rij in data]  # Extract pogingen

    plt.figure(figsize=(10, 7))
    plt.pie(mislukte_inlogpogingen, labels=gebruikersnamen, autopct='%1.1f%%', startangle=140)
    plt.title('Aantal Mislukte Inlogpogingen per Gebruiker')
    plt.axis('equal')  # Zorgt ervoor dat de pie chart een cirkel is1
    plt.savefig(pad_naar_img)
    plt.close()

app = Flask(__name__)


@app.route('/piechart_maken', methods=['GET', 'POST'])
def piechart():

    if request.method == 'POST':
        begin_tijd = request.form['begin_tijd']
        eind_tijd = request.form['eind_tijd']
        event_type = request.form['event_type']
        hostname = request.form['hostname']
        
        # Je logging_ophalen_groep functie wordt hier aangeroepen
        data = logging_ophalen_groep(begin_tijd, eind_tijd, event_type, hostname)
        print(data)
        # Maak piechart en sla op in static directory
        maak_piechart(data)  # Pas deze functie aan om een bestandspad parameter te accepteren
        
        return redirect(url_for('resultaten'))
    return render_template('piechart_maken.html')

@app.route('/resultaten')
def resultaten():
    # De piechart wordt getoond door de afbeelding in de static directory te gebruiken
    return render_template('resultaten.html', image_path=url_for('static', filename='chart.png'))

@app.route('/data_overzicht', methods=['GET', 'POST'])
def data_overzicht():

    aantal_rows = request.args.get('aantal_rows', default=10, type=int)
    data = haal_laatste_x_records_op(aantal_rows)
    return render_template('data_overzicht.html', data=data)

@app.route('/')
def start_page():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=5761, debug=True)