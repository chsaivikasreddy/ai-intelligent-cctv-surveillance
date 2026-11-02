# AI-Based Intelligent CCTV Surveillance System

An AI-powered video surveillance platform designed to improve security monitoring through automated person detection, object tracking, restricted-zone monitoring and intelligent intrusion alerts using existing CCTV infrastructure.

## Project Overview

Traditional CCTV surveillance requires continuous human monitoring, which can be time-consuming and inefficient.

This project aims to automate surveillance by integrating computer vision, video processing and event management. It analyzes camera streams, detects people, tracks their movements and identifies suspicious activities in monitored areas.

## Key Features

- **Person Detection:** Detects people from CCTV video streams using YOLO-based object detection.
- **Object Tracking:** Assigns unique IDs to detected individuals to track their movement.
- **Restricted Zone Monitoring:** Monitors predefined restricted areas.
- **Intrusion Detection:** Identifies unauthorized entry into monitored zones.
- **Event Management:** Records and manages detected surveillance events.
- **Evidence Capture:** Captures timestamped snapshots for detected events.
- **Web Dashboard:** Provides a browser-based interface for monitoring surveillance activities.
- **Authorization:** Includes an authorization component for access management.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Object Detection | YOLO |
| Computer Vision | OpenCV |
| Backend | Python |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Version Control | Git and GitHub |

## Project Structure

```text
ai-intelligent-cctv-surveillance/
│
├── dashboard/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── authorization.py
├── backend.py
├── camera_stream.py
├── person_detection.py
├── event_database.py
├── event_manager.py
├── risk_engine.py
├── surveillance_engine.py
│
├── .gitignore
└── README.md
```

## System Workflow

1. Capture video from the CCTV camera or video stream.
2. Process video frames using computer vision.
3. Detect people using the YOLO object detection model.
4. Track detected individuals across frames.
5. Monitor predefined restricted zones.
6. Identify potential intrusion events.
7. Generate and manage surveillance alerts.
8. Capture evidence snapshots and display relevant information through the dashboard.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/chsaivikasreddy/ai-intelligent-cctv-surveillance.git
```

### 2. Navigate to the project directory

```bash
cd ai-intelligent-cctv-surveillance
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Configure the YOLO model

Download or provide the compatible YOLO model weights separately and configure the model path as required by the detection code.

The model weights are not included in this repository.

### 6. Run the application

Refer to the application entry point and configuration in the source code to start the backend and camera processing components.

Open the dashboard's `index.html` in a browser if it is configured for standalone access.

## Applications

- Border and perimeter surveillance
- Restricted-area monitoring
- Industrial security monitoring
- Campus and building surveillance
- Automated CCTV monitoring systems

## Future Enhancements

- Real-time notification integration
- Advanced suspicious-activity detection
- Multi-camera monitoring
- Improved tracking and analytics
- Cloud-based event storage
- RFID-based access integration

## Project Information

**Project Category:** Artificial Intelligence and Computer Vision

**Domain:** Intelligent Video Surveillance

**Developer:** Chintha Gunta Veera Sai Vikas Reddy

**GitHub:** https://github.com/chsaivikasreddy

---

*This project is developed for learning and intelligent surveillance automation. Detection results should be reviewed by authorized personnel before taking security-related action.*
