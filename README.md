# Barriertrack || Hoofdserver README

Welkom bij de setup-instructies voor de Barriertrack server. Volg deze stappen om de server correct op te zetten.

## Installatie

### Python Dependencies
Je kunt de requirements vinden van python in de requirements.txt file. Run dan pip install requirements.txt om de dependencies te installeren.

``
pip install -r requirements.txt
``

### Variablen
Voordat je begint met de installtie4 contrroleer het ``variables.env`` bestand om er voor te zorgen dat alles correct staat. Dit bestand heeft de belangerijkse configuratievairbale voor de databasen en de API, zoals de inloggevens en API server instellingen

Controleer en pas indien nodig aan:
*Database gebruikersnaam en wachtwoord (POSTGRES_USER, POSTGRES_PASSWORD)
*Database naam (POSTGRES_DB)
*API IP-adres (API_IP)
*API poort (API_PORT)
*API endpoint pad (API_LISTEN_DIR)

# Database
Volg deze stappen om je database en pgAdminop te zetten:

start de database en pgadmin containers op:
``
cd /database
sudo docker-compose up -d 
``

Zorg ervoor dat install_config.sh uitvoerbaar is door het volgende commando uit te voeren:

``
chmod +x install_config.sh
``

Wanneer de containers draaien, voer het install_config.sh script uit 
``
./install_config.sh
``


# De API

###variablen

Zorg dat je de requirements hebt geinstaleerd en de variables.env hebt gecontroleerd

Voer dan het ./install.sh script uit om de API als een service te installeren:
```
install.sh
``
Om de status van de API voer dan uit:
``
systemctl status barriertrack_api
``

Wil je de API handmatig starten doe  dan:
``
python3 api.py 
``



