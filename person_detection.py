from event_manager import EventManager
from event_database import EventDatabase
from authorization import Authorization
from ultralytics import YOLO
from risk_engine import RiskEngine
import cv2
from datetime import datetime

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Event manager
event_manager = EventManager()
event_database = EventDatabase()
authorization = Authorization()
risk_engine = RiskEngine()

# Temporary RFID ID for testing
rfid_id = "A001"


while True:

    success, frame = cap.read()

    if not success:
        print("Could not read camera")
        break

    # Detect and track ONLY people
    results = model.track(
        frame,
        classes=[0],
        persist=True,
        verbose=False
    )

    # Draw boxes and tracking IDs
    annotated_frame = results[0].plot()

    # Define restricted zone
    zone_x1 = 300
    zone_y1 = 150
    zone_x2 = 800
    zone_y2 = 500

    # Check each detected person
    for box in results[0].boxes:

        # Get bounding box coordinates
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

        # Get tracking ID
        if box.id is None:
            continue

        person_id = int(box.id[0])

        # Calculate bottom-center point
        center_x = int((x1 + x2) / 2)
        bottom_y = int(y2)

        # Check whether person is inside restricted zone
        inside_zone = (
            zone_x1 <= center_x <= zone_x2
            and zone_y1 <= bottom_y <= zone_y2
        )

        # Send information to EventManager
        event = event_manager.check_person(
            person_id,
            inside_zone
        )

        # New intrusion event
        if event:

            current_time = event["time"]

            # Check whether the person is authorized
            person_info = authorization.check(rfid_id)

            person_name = person_info["name"]
            is_authorized = person_info["authorized"]


            #riskfactor
            risk = risk_engine.calculate_risk(
                is_authorized=is_authorized,
                zone_level="HIGH"
            )

            risk_level = risk["level"]
            risk_score = risk["score"]
            risk_reason = risk["reason"]
            if is_authorized:
                print(
                    f"🟢 AUTHORIZED | "
                    f"{person_name} | "
                    f"Person ID: #{person_id}"
                    )
            else:
                print(
                    f"🚨 UNKNOWN PERSON | "
                    f"Person ID: #{person_id}"
                )
            print(
                    f"⚠️ RISK | "
                    f"Level: {risk_level} | "
                    f"Score: {risk_score} | "
                    f"Reason: {risk_reason}"
                )

            # Create evidence filename
            filename_time = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            image_path = (
                f"evidence/"
                f"intrusion_{filename_time}"
                f"_person_{person_id}.jpg"
            )

            # Save screenshot
            cv2.imwrite(
                image_path,
                annotated_frame
            )
            event_database.add_event(
                person_id=person_id,
                rfid_id=rfid_id,
                person_name=person_name,
                authorization="AUTHORIZED" if is_authorized else "UNKNOWN",
                event_type=event["event"],
                zone=event["zone"],
                date=datetime.now().strftime("%Y-%m-%d"),
                time=current_time,
                evidence=image_path,
                risk_level=risk_level,
                risk_score=risk_score,
                risk_reason=risk_reason
            )

            print(
                f"🚨 INTRUSION ALERT | "
                f"Person ID: #{person_id} | "
                f"Time: {current_time} | "
                f"Evidence: {image_path}"
            )

        # Display warning while person is inside
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

    # Draw restricted zone
    cv2.rectangle(
        annotated_frame,
        (zone_x1, zone_y1),
        (zone_x2, zone_y2),
        (0, 0, 255),
        3
    )

    # Zone label
    cv2.putText(
        annotated_frame,
        "RESTRICTED ZONE",
        (zone_x1, zone_y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    # Display video
    cv2.imshow(
        "Person Tracking",
        annotated_frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()