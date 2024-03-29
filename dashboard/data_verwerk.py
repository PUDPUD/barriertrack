import psycopg2

def db_connectie():
    try:
        # Vul de juiste database inloggegevens in
        conn = psycopg2.connect(
            host="95.179.185.228",
            database="logging",
            user="postgres",
            password="postgres",
        )
        return conn
    except Exception as e:
        print(f"Fout bij connectie met database: {e}")
        return None

def get_data():
    conn = db_connectie()
    cursor = conn.cursor()
    query = """
        SELECT timestamp, "user", hostname, event_type, full_event, source_ip
        FROM public.auth_log
        WHERE timestamp >= (CURRENT_DATE - INTERVAL '1 day');
    """
    cursor.execute(query)
    resultaten = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultaten
import matplotlib.pyplot as plt

def maak_piechart(data):
    event_types = [log[3] for log in data]
    aantal_events = [event_types.count(event_type) for event_type in set(event_types)]
    labels = set(event_types)

    plt.pie(aantal_events, labels=labels, autopct='%1.1f%%')
    plt.title('Verdeling van event types (laatste dag)')
    plt.show()

from jinja2 import Template

def maak_datatable(data):
    template = Template("""
    <table>
        <thead>
            <tr>
                <th>Tijdstip</th>
                <th>Gebruiker</th>
                <th>Hostname</th>
                <th>Event type</th>
                <th>Volledige event</th>
                <th>Bron IP</th>
            </tr>
        </thead>
        <tbody>
            {% for log in data %}
            <tr>
                <td>{{ log[0] }}</td>
                <td>{{ log[1] }}</td>
                <td>{{ log[2] }}</td>
                <td>{{ log[3] }}</td>
                <td>{{ log[4] }}</td>
                <td>{{ log[5] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    """)
    return template.render(data=data)

@app.route('/rapporten')
def rapporten():
    data = get_data()
    piechart = maak_piechart(data)
    datatable = maak_datatable(data)
    return render_template('rapporten.html', piechart=piechart, datatable=datatable)


