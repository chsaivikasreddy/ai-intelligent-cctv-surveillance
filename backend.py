from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from camera_stream import generate_frames, engine

import sqlite3


app = FastAPI(
    title="Intelligent CCTV Surveillance",
    description="AI-based person detection and restricted-zone monitoring",
    version="1.0"
)


# Allow dashboard to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():

    return {
        "message": "CCTV Backend is running"
    }


# -------------------------
# System Status
# -------------------------

@app.get("/status")
def status():

    return {
        "system": "CCTV Surveillance",
        "status": "online"
    }


# -------------------------
# Get Latest Intrusion
# -------------------------

@app.get("/latest-event")
def latest_event():

    event = engine.get_last_event()

    if event is None:

        return {
            "status": "no_event",
            "event": None
        }

    return {
        "status": "event_detected",
        "event": event
    }


# -------------------------
# Get Database Events
# -------------------------

@app.get("/events")
def get_events():

    connection = sqlite3.connect("events.db")

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM events
        ORDER BY event_id DESC
    """)

    events = cursor.fetchall()

    connection.close()

    return [dict(event) for event in events]


# -------------------------
# AI Camera Stream
# -------------------------

@app.get("/video")
def video():

    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )