import sqlite3


class EventDatabase:

    def __init__(self, database_name="events.db"):

        self.connection = sqlite3.connect(database_name)

        self.cursor = self.connection.cursor()

        self.create_table()


    def create_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (

                event_id INTEGER PRIMARY KEY AUTOINCREMENT,

                person_id INTEGER,

                rfid_id TEXT,

                person_name TEXT,

                authorization TEXT,

                event_type TEXT,

                zone TEXT,

                date TEXT,

                time TEXT,

                evidence TEXT,

                status TEXT,

                risk_level TEXT,

                risk_score INTEGER,

                risk_reason TEXT

            )
        """)

        self.connection.commit()


    def add_event(
        self,
        person_id,
        rfid_id,
        person_name,
        authorization,
        event_type,
        zone,
        date,
        time,
        evidence,
        risk_level,
        risk_score,
        risk_reason,
        status="Unresolved"
    ):

        self.cursor.execute("""
            INSERT INTO events
            (
                person_id,
                rfid_id,
                person_name,
                authorization,
                event_type,
                zone,
                date,
                time,
                evidence,
                status,
                risk_level,
                risk_score,
                risk_reason
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            person_id,
            rfid_id,
            person_name,
            authorization,
            event_type,
            zone,
            date,
            time,
            evidence,
            status,
            risk_level,
            risk_score,
            risk_reason
        ))

        self.connection.commit()


    def get_events(self):

        self.cursor.execute("""
            SELECT * FROM events
            ORDER BY event_id DESC
        """)

        return self.cursor.fetchall()


    def close(self):

        self.connection.close()