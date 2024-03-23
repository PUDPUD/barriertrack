import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path



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
    print(f"\nLogging is verstuurd: \n StatusCode: {response.status_code}\n Logging: {data}")
    if response.status_code != 200:
        print("Fout bij het versturen van data:", response.text)

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
                if "Accepted password" in line:
                    user_index = line.find("for") + 4
                    ip_index = line.find("from") + 5
                    user = line[user_index:line.find("from")].strip()
                    ip_address = line[ip_index:line.find("port")].strip()
                    event_type = "Accepted Password"
                    full_event = line.strip()
                    data = {
                        "timestamp": formatted_datetime,
                        "user": user,
                        "hostname": server_name,
                        "event_type": event_type,
                        "full_event": full_event,
                        "source_ip": ip_address
                    }
                    verstuur_data(data)
                    pass
                if "Failed password" in line:
                    user_index = line.find("for") + 4
                    ip_index = line.find("from") + 5
                    user = line[user_index:line.find("from")].strip()
                    ip_address = line[ip_index:line.find("port")].strip()
                    event_type = "Failed Password"
                    full_event = line.strip()
                    data = {
                        "timestamp": formatted_datetime,
                        "user": user,
                        "hostname": server_name,
                        "event_type": event_type,
                        "full_event": full_event,
                        "source_ip": ip_address
                    }
                    verstuur_data(data)
                    pass
                if "Disconnected" in line:
                    user_index = line.find("for") + 4
                    ip_index = line.find("from") + 5
                    user = line[user_index:line.find("from")].strip()
                    ip_address = line[ip_index:line.find("port")].strip()
                    event_type = "Disconnected"
                    full_event = line.strip()
                    data = {
                        "timestamp": formatted_datetime,
                        "user": user,
                        "hostname": server_name,
                        "event_type": event_type,
                        "full_event": full_event,
                        "source_ip": ip_address
                    }
                    verstuur_data(data)
                    pass
                if "Invalid user" in line:
                    user_index = line.find("for") + 4
                    ip_index = line.find("from") + 5
                    user = line[user_index:line.find("from")].strip()
                    ip_address = line[ip_index:line.find("port")].strip()
                    event_type = "Invalid user"
                    full_event = line.strip()
                    data = {
                        "timestamp": formatted_datetime,
                        "user": user,
                        "hostname": server_name,
                        "event_type": event_type,
                        "full_event": full_event,
                        "source_ip": ip_address
                    }
                    verstuur_data(data)
                    pass

