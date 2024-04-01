# barriertrack || Hoofdserver Readme

Welkom bij de Barriertrack hoofdserver handleiding. Met deze oplossing kan je  auth.log logging van al je Ubuntu servers centraal worden gebracht voor analyse, visualisatie en archivering.
Deze readme is voor de hoofdserver, met de database, API en Dashbaord.

Voor de installatie en configuratie readme van de agent, die op elke individuele server draait, ga naar de agent directory.


Vereistem

Eisen van 

    Besturingssysteem: Ubuntu Server, 20.04 of 22.04
    Python: Python 3 en pip

    Docker: voor de database en pgAdmin
    Docker-Compose: voor het beheren van de containers
    Python requirements: De belangerijke bibliotheken die door de Python code worden gebruikt.

    ik leg later uit hoe je Docker, Docker-Compose en de Python requirements installeert.


# Installatie proces


## Stap 1 Configureren van de variablen

Voor een goede werkend hoofdserver moet je eerst de variablen en aanpassen indien nodig.


#### Database Variabelen
- `POSTGRES_USER`: De gebruikersnaam voor toegang tot de PostgreSQL database.
- `POSTGRES_PASSWORD`: Het wachtwoord voor de PostgreSQL database gebruiker.
- `POSTGRES_DB`: De naam van de PostgreSQL database die gebruikt wordt voor het loggen van gegevens.
- `DATABASE_IP`: Het IP-adres waarop de PostgreSQL database bereikbaar is.

#### PgAdmin Variabelen
- `PGADMIN_DEFAULT_EMAIL`: Het standaard e-mailadres om in te loggen op pgAdmin, de webgebaseerde administratie tool voor PostgreSQL.
- `PGADMIN_DEFAULT_PASSWORD`: Het standaard wachtwoord voor het pgAdmin account.

#### API Variabelen
- `API_IP`: Het IP-adres waarop de API luistert. `0.0.0.0` betekent dat de API op alle beschikbare netwerkinterfaces luistert.
- `API_PORT`: De poort waarop de API luistert voor inkomende verzoeken.
- `API_LISTEN_DIR`: Het endpoint pad waar de API verzoeken voor logging input ontvangt.

#### Dashboard Variabelen
- `DASHBOARD_PORT`: De poort waarop het dashboard luistert voor inkomende verzoeken.
- `DASHBOARD_IP`: Het IP-adres waarop het dashboard luistert. `0.0.0.0` geeft aan dat het dashboard op alle beschikbare netwerkinterfaces luistert.



## Stap 2 Installatie docker en docker compose

### Docker en Python Dependencies
- **Docker**: nodig voor het opzetten van de database en pgAdmin. Zie [Docker Ubuntu](https://docs.docker.com/engine/install/ubuntu/) 
- **Docker Compose**: nodig voor het configureren & beheren van de containers[Docker compose Ubuntu](https://docs.docker.com/compose/install/linux/#install-using-the-repository/) 
- **Python Dependencies**: Installeer via `requirements.txt` met het commando `pip install -r requirements.txt`.

Voer de volgende commandos uit:

bash
```
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

### Stap 3 Python dependencies

Installeer de benodigde Python libarys via een requirements.txt bestand. 

```
pip install -r requirements.txt
```


### Database en pgAdmin
1. Start de services met Docker-compose: `sudo docker-compose up -d` vanuit de `barriertrack/database` directory.
2. Maak `install_config.sh` uitvoerbaar met `chmod +x install_config.sh` en voer het uit met `./install_config.sh`.

Hierna is de gebruiker aangemaakt en PGadmin beschikbaar op: http://jouw_ip:8888


### API
De API verbindt met de database om logdata te ontvangen en te verwerken.
- **Automatisch Starten**: Gebruik `./install.sh` om de API als service te installeren.
``` 
chmod +x install_barriertrack_api.sh
./install_barriertrack_api.sh
```
bekijk de status van het dahsboard:
```
systemctl status barriertrack_dashboard
```

- **Handmatig Starten**: Voer `python3 api.py` uit voor een directe start.
bash
```
python3 api.py
```


### Dashboard
Het dashboard biedt een visuele weergave van de data.
- **Automatisch Starten**: Om barriertrack_dashboard als een service te starten voer het volgende uit:
``` 
chmod +x install_barriertrack_dashboard.sh
./install_barriertrack_dashboard.sh
```
bekijk de status van het dahsboard:
```
systemctl status barriertrack_dashboard
```

- **Handmatig Starten**: Voer `dashboard api.py` uit voor een directe start.
bash
```
python3 dashboard.py
```


# Api en Data Verwerking

Met barriertrack wordt de logging van auth.log centraal mogelijk gemaakt. Hier is hoe het proces werkt:

## Data flow

1. Data Extractie:
De agent analyseert /var/log/auth.log, herkent diverse gebeurtenissen zoals:
- Accepted password
- Disconnected
- Failed password for invalid user
- Failed password
2. Data Formattering en Verzending: De agent zet deze gegevens om naar JSON-formaat en verstuurt ze via een POST-verzoek naar de API.
3. Data Verwerking: Bij ontvangst construeert de API een SQL-query met de aangeleverde gegevens, slaat deze op in de database en zorgt voor dagelijkse archivering

De uiteindelijke data verzonden naar de API is:

- Timestamp: De exacte tijd van de loggebeurtenis.
- Hostname: De hostname van de agent.
- User: Actie uitgevoerd door de gebruiker.
- Source IP: Het IP-adres van de inlogpoging.
- Event Type: Type van het event.
- Full Event: De volledige logregel, onverkort en niet geaggregeerd.

## Dashboard Visualisatie
Het dashboard gebruikt MatplotLib om een cirkeldiagram te genereren op basis van vier variablen:

- Begin tijd
- Eind Tijd
- Event Type
- Hostname van de agent

Ook heeft het dashboard de mogelijkheid om de meest recente loggegevens op te halen met een door de gebruiker gespecificeerd aantal (X).  
Deze logs zijn direct op het dashboard beschikbaar en kunnen of worden geexporteerd naar PDF.








