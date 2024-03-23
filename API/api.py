# Importeer benodigde modules
from flask import Flask, request, jsonify
import json
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

#Variablen:
#https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
dotenv_path = Path('../variables.env')
load_dotenv(dotenv_path=dotenv_path)
api_ip = os.getenv("API_IP")
api_port = int(os.getenv("API_PORT"))
api_listen_dir = str(os.getenv("API_LISTEN_DIR"))
working_directory = os.getcwd()
vandaag = datetime.now().strftime("%Y-%m-%d")

## ansci kleur codes: https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007?permalink_comment_id=4488193
paars = "\033[0;35m"
stop_kleur = "\033[0m"
bold  = "\033[1m"
rood = "\033[0;31m"
blauw = "\033[0;34m"
geel = "\033[0;33m"


# initialiseren van de Flask app
app = Flask(__name__)

#https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
#database inlog met .env file
database_inlog = {
    "host": "localhost",
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

#archief map aanmaken
if "archief" not in os.listdir(working_directory):
    os.mkdir("archief")
    print("archief folder aangemaakt")


# functie voor het opslaan van de ontvangen API data in TXT en json format
def opslaan(json_data):
    bestand_json = f"archief/{vandaag}.json"
    bestand_txt = f"archief/{vandaag}.txt"

    with open(bestand_json, "w") as f:
        json.dump(json_data, f)
    with open(bestand_txt, "a") as f:
        f.write(json.dumps(json_data) + "\n")

#https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
#https://medium.com/@shahrukhshl0/building-a-flask-crud-application-with-psycopg2-58de201e3c14
# Api voor het ontvangen van de logging
@app.route(api_listen_dir, methods=["POST"])
def ontvang_logging():
    try:
        conn = psycopg2.connect(**database_inlog)
        cursor = conn.cursor()
        ontvangen_api_data = request.get_json()

        # Parseer de timestamp met de juiste formaat en huidig jaar
        #timestamp_str = ontvangen_api_data["timestamp"] + " " + str(datetime.now().year)  # Voeg huidig jaar toe
        #timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S %Y')
        timestamp = ontvangen_api_data["timestamp"]

        # extraheer de json data 
        user = ontvangen_api_data.get("user", "Onbekend")
        hostname = ontvangen_api_data.get("hostname", "Onbekend")
        source_ip = ontvangen_api_data.get("source_ip", "Onbekend")
        event_type = ontvangen_api_data.get("event_type", "Onbekend")
        full_event = ontvangen_api_data.get("full_event", "Onbekend")

        print(f"{rood}{bold} Ontvangen data: {stop_kleur} \n {rood}Van server:{stop_kleur} {blauw} {hostname} {stop_kleur} \n {geel}{ontvangen_api_data} {stop_kleur}")
        cursor.execute("""
            INSERT INTO public.auth_log (timestamp, "user", hostname, event_type, full_event, source_ip)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (timestamp, user, hostname, event_type, full_event, source_ip))
        conn.commit()
        opslaan(ontvangen_api_data)
        return jsonify(ontvangen_api_data), 200

    except Exception as e:
        print(f" De api is gecrasht: \n \n {e}")
    finally:
        if conn:
            conn.close()

# Start de API flask app
if __name__ == "__main__":

    print(f" \n \n {paars}{bold} luisteren op http://{api_ip}:{api_port}{api_listen_dir} \n \n {stop_kleur}")
    app.run(host=api_ip, port=api_port)



