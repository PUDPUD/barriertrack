import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
import json



#variable env bestand
dotenv_path = Path('agent_vars.env')
load_dotenv(dotenv_path=dotenv_path)


#Omzetten van de .env variablen
log_file = os.getenv("LOG_BESTAND")
url = os.getenv("DOEL_SERVER_URL")
loop_tijd = float(os.getenv("LOOP_TIJD"))
print(f"Logging barriertrack_agent gestart en verstuurd de data naar {url}")


#  Versturen van de POST reqquest naar de API
def verstuur_data(data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    
    gebruiker = data["user"]
    vol_event = data["full_event"]
    van_ip = data["source_ip"]
    gebeurtenis = data["event_type"]
    print(f"\nLogging is verstuurd naar {url}: \n \n LET OP: {event_type} \n gebruiker = {gebruiker} \n van ip : {van_ip}, \n volledige event: {vol_event} " )
    if response.status_code != 200:
        print("Fout bij het versturen van data:", response.text)

def opslaan_log_vandaag(data):
    with open("verstuurde_logging.txt", "a") as f:
        f.write(json.dumps(data) + "\n")

# probleem is dat ubuntu verkeerde log format heeft namelijk: Mar  9 00:00:00 
# en onze API kan alleen maar YYYY-MM-DD HH:MM:SS format aan
def format_datetime(log_tijd, log_maand_dag):
    maand_namen = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    # Als maand dag 1 karakter is, voeg dan een 0 toe. Database verwacht 2 karakters
    if len(log_maand_dag[1]) == 1:
        log_maand_dag[1] = "0" + log_maand_dag[1]

    
    jaar = datetime.now().year
    formatted_date = f"{jaar}-{maand_namen[log_maand_dag[0]]}-{log_maand_dag[1]} {log_tijd}"
    return formatted_date



with open(log_file, "r") as f:
    #https://pynative.com/python-file-seek/
    #begin aan het einden van het bestand
    f.seek(0, 2)

    #Inspiratie voor het loopen: https://stackoverflow.com/questions/74198615/why-while-loop-does-not-run-in-txt-file-reading-in-python
    #loop door het helebestand elke 0.1 seconden
    while True:
        line = f.readline()
        if not line:
            print("Running...", end="\r", flush=True)
            time.sleep(loop_tijd)  # Wacht kort als er geen nieuwe regel is
            continue


        if "sshd" in line: 
                #Het extraheren van de de event_type onafhankelijke data, zoals servernaam, tijd en het in het goede format zetten van de timestamp
                parts = line.split()
                log_maand_dag = parts[0:2]
                log_tijd = parts[2]
                formatted_datetime = format_datetime(log_tijd, log_maand_dag)
                server_name = parts[3]
                ip_address = "Onbekend"
                event_type = "Onbekend"
                user = "Onbekend"

                if "Accepted password" in line:
                    user = line.split("for")[1].split()[0]
                    ip_address = line.split("from")[1].split()[0]
                    event_type = "Accepted password"
                elif "Disconnected"  in line and "[preauth]" not in line:
                    user = line.split("from")[1].split()[0]
                    ip_address = line.split("from")[1].split()[0]
                    event_type = "Disconnected"
                elif "Failed password" in line and "invalid user" in line:
                    event_type = "Failed password for invalid user" 
                    user = line.split("invalid user")[1].split()[0]
                    ip_address = line.split("from")[1].split()[0]
                elif "Failed password" in line and "message" not in line:
                    event_type = "Failed password"
                    user = line.split("for")[1].split()[0]
                    ip_address = line.split("from")[1].split()[0]
                    
                full_event = line.strip()


                data = {
                    "timestamp": formatted_datetime,
                    "user": user,
                    "hostname": server_name,
                    "event_type": event_type,
                    "full_event": full_event,
                    "source_ip": ip_address
                    }
                if event_type == "Onbekend":
                    continue
                else:
                    verstuur_data(data)
                    opslaan_log_vandaag(data)
        else:
            continue



