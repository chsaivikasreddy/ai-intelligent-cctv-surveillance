import cv2
import os
from datetime import datetime

from ultralytics import YOLO

from event_manager import EventManager
from event_database import EventDatabase
from risk_engine import RiskEngine


class SurveillanceEngine:

    def __init__(self):

        # AI model
        self.model = YOLO("yolo11n.pt")

        # Existing modules
        self.event_manager = EventManager()
        self.event_database = EventDatabase()
        self.risk_engine = RiskEngine()

        # Latest intrusion event
        self.last_event = None

        # Evidence folder
        self.evidence_folder = "evidence"

        os.makedirs(
            self.evidence_folder,
            exist_ok=True
        )

        # Restricted zone
        # Keep your current coordinates here
        self.zone_x1 = 400
        self.zone_y1 = 100
        self.zone_x2 = 1000
        self.zone_y2 = 650


    def process_frame(self, frame):

        # Detect and track ONLY people
        results = self.model.track(
            frame,
            classes=[0],
            persist=True,
            verbose=False
        )

        # Draw YOLO detections
        annotated_frame = results[0].plot()


        # Check every detected person
        for box in results[0].boxes:

            if box.id is None:
                continue


            # Bounding box
            x1, y1, x2, y2 = (
                box.xyxy[0].cpu().numpy()
            )


            # Person tracking ID
            person_id = int(box.id[0])


            # Bottom-center of person
            center_x = int((x1 + x2) / 2)

            bottom_y = int(y2)


            # Check restricted zone
            inside_zone = (
                self.zone_x1 <= center_x <= self.zone_x2
                and
                self.zone_y1 <= bottom_y <= self.zone_y2
            )


            # Event manager
            event = self.event_manager.check_person(
                person_id,
                inside_zone
            )


            # =====================================
            # NEW INTRUSION
            # =====================================

            if event:

                current_time = event["time"]


                # -----------------------------
                # Save evidence screenshot
                # -----------------------------

                filename_time = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )


                image_path = os.path.join(
                    self.evidence_folder,
                    f"intrusion_{filename_time}"
                    f"_person_{person_id}.jpg"
                )


                cv2.imwrite(
                    image_path,
                    annotated_frame
                )


                # -----------------------------
                # Store latest event
                # -----------------------------

                self.last_event = {

                    "person_id": person_id,

                    "event": "INTRUSION DETECTED",

                    "zone": "Restricted Zone",

                    "time": current_time,

                    "evidence": image_path

                }


                # -----------------------------
                # Terminal alert
                # -----------------------------

                print(
                    f"🚨 INTRUSION DETECTED | "
                    f"Person ID: #{person_id} | "
                    f"Zone: Restricted Zone | "
                    f"Time: {current_time}"
                )


                print(
                    f"📸 Evidence saved: "
                    f"{image_path}"
                )


            # =====================================
            # SHOW INTRUSION ON VIDEO
            # =====================================

            if inside_zone:

                cv2.putText(
                    annotated_frame,
                    "INTRUSION!",
                    (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )


        # =====================================
        # DRAW RESTRICTED ZONE
        # =====================================

        cv2.rectangle(
            annotated_frame,
            (self.zone_x1, self.zone_y1),
            (self.zone_x2, self.zone_y2),
            (0, 0, 255),
            3
        )


        cv2.putText(
            annotated_frame,
            "RESTRICTED ZONE",
            (self.zone_x1, self.zone_y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )


        return annotated_frame


    def get_last_event(self):

        return self.last_event