# barriertrack || Hoofdserver Readme

Welkom bij de setup-instructies voor de Barriertrack server. Volg deze stappen om de server correct op te zetten.


### Vereisten
- **Besturingssysteem**: Ubuntu Server (aanbevolen versies: 20.04 of 22.04).
- **Python**: Zorg ervoor dat Python 3 en `pip` zijn geïnstalleerd.
- **Docker**: Noodzakelijk voor het draaien van de database en pgAdmin.
- **Python Dependencies**: Vereist voor zowel de Hoofdserver als de Agent.




### Python Dependencies
De Python dependencies kunnen worden geïnstalleerd via de `requirements.txt` file. Voer het volgende commando uit om ze te installeren:

```bash
pip install -r requirements.txt

```

### Variabelen

Controleer het variables.env bestand voor de juiste configuratie van de database en de API, zoals inloggegevens en serverinstellingen. Pas de volgende variabelen aan indien nodig:


### Database Variabelen
- `POSTGRES_USER`: De gebruikersnaam voor toegang tot de PostgreSQL database.
- `POSTGRES_PASSWORD`: Het wachtwoord voor de PostgreSQL database gebruiker.
- `POSTGRES_DB`: De naam van de PostgreSQL database die gebruikt wordt voor het loggen van gegevens.
- `DATABASE_IP`: Het IP-adres waarop de PostgreSQL database bereikbaar is.

### PgAdmin Variabelen
- `PGADMIN_DEFAULT_EMAIL`: Het standaard e-mailadres om in te loggen op pgAdmin, de webgebaseerde administratie tool voor PostgreSQL.
- `PGADMIN_DEFAULT_PASSWORD`: Het standaard wachtwoord voor het pgAdmin account.

### API Variabelen
- `API_IP`: Het IP-adres waarop de API luistert. `0.0.0.0` betekent dat de API op alle beschikbare netwerkinterfaces luistert.
- `API_PORT`: De poort waarop de API luistert voor inkomende verzoeken.
- `API_LISTEN_DIR`: Het endpoint pad waar de API verzoeken voor logging input ontvangt.

### Dashboard Variabelen
- `DASHBOARD_PORT`: De poort waarop het dashboard luistert voor inkomende verzoeken.
- `DASHBOARD_IP`: Het IP-adres waarop het dashboard luistert. `0.0.0.0` geeft aan dat het dashboard op alle beschikbare netwerkinterfaces luistert.

## Installatie Script

## Installatie

### Docker en Python Dependencies
- **Docker**: Vereist voor het opzetten van de database en pgAdmin. Zie [Docker's officiële documentatie](https://docs.docker.com/get-docker/) voor installatie.
- **Python Dependencies**: Installeer via `requirements.txt` met het commando `pip install -r requirements.txt`.

## Opstarten

### Database en pgAdmin
1. Start de services met Docker-compose: `sudo docker-compose up -d` vanuit de `barriertrack/database` directory.
2. Maak `install_config.sh` uitvoerbaar met `chmod +x install_config.sh` en voer het uit met `./install_config.sh`.

### API
De API verbindt met de database om logdata te ontvangen en te verwerken.
- **Automatisch Starten**: Gebruik `./install.sh` om de API als service te installeren.
- **Handmatig Starten**: Voer `python3 api.py` uit voor een directe start.

### Dashboard
Het dashboard biedt een visuele weergave van de data.
De API verbindt met de database om logdata te ontvangen en te verwerken.
- **Automatisch Starten**: Gebruik `./install.sh` om de API als service te installeren.
- **Starten**: Voer `python3 app.py` uit in de dashboard directory om het dashboard te starten.



