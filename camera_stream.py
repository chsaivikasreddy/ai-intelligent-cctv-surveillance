import cv2

from surveillance_engine import SurveillanceEngine


# Create surveillance engine once
engine = SurveillanceEngine()


def generate_frames():

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Could not open laptop camera")
        return

    print("📷 AI surveillance stream started")

    while True:

        success, frame = camera.read()

        if not success:
            print("❌ Could not read camera frame")
            break

        # Process frame using AI surveillance engine
        annotated_frame = engine.process_frame(frame)

        # Convert frame to JPEG
        ret, buffer = cv2.imencode(
            ".jpg",
            annotated_frame
        )

        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        # Send frame to browser
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )

    camera.release()