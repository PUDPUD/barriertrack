## Barriertrack Agent Installatie

De Barriertrack agent is ontworpen om te draaien op externe servers voor het monitoren van logbestanden en het versturen van de gegevens naar de Hoofdserver. Hier volgen de stappen om de agent te installeren en te configureren.

### Vereisten

- **Besturingssysteem**: Ubuntu Server (aanbevolen versies: 20.04 of 22.04).
- **Rechten**: Root toegang of sudo privileges.
- **Python**: Python 3 en `pip` moeten geïnstalleerd zijn.

### Installatieproces

1. **Installeer Python en pip**:
   Zorg ervoor dat Python en pip geïnstalleerd zijn op de server. dit kan met de volgende commando's:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip

Configureer Variabelen:
Kopieer agent_vars.env.example naar agent_vars.env en pas de configuratievariabelen aan volgens je setup. De variabelen zijn:

    DOEL_SERVER_URL: URL van de API op de Hoofdserver.
    LOG_BESTAND: Het volledige pad naar het logbestand dat je wilt monitoren.
    LOOP_TIJD: Interval in seconden waarmee de agent het logbestand op nieuwe gegevens controleert.

    Installeer Vereisten:
Installeer de vereiste Python-pakketten met pip via de requirements.txt:

bash
```
pip3 install -r requirements.txt
```

### Agent
De Agent verbindt met de API om de sshd logging te versturen
- **Automatisch Starten**: Gebruik `./install.sh` om de API als service te installeren.
``` 
chmod +x install.sh
./install.sh
```
bekijk de status van het dahsboard:
```
systemctl status barriertrack_agent
```

- **Handmatig Starten**: Voer `python3 api.py` uit voor een directe start.
bash
```
python3 agent.py
```

