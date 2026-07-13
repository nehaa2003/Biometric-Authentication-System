import json
import os
from pathlib import Path

import cv2
import numpy as np


BASE_DIRECTORY = Path(__file__).resolve().parent
DATASET_DIRECTORY = BASE_DIRECTORY / "dataset"
MODEL_DIRECTORY = BASE_DIRECTORY / "model"

MODEL_FILE = MODEL_DIRECTORY / "face_model.yml"
USERS_FILE = MODEL_DIRECTORY / "users.json"

DATASET_DIRECTORY.mkdir(exist_ok=True)
MODEL_DIRECTORY.mkdir(exist_ok=True)


def load_users() -> dict[str, str]:
    if not USERS_FILE.exists():
        return {}

    try:
        with USERS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users: dict[str, str]) -> None:
    with USERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def get_next_user_id(users: dict[str, str]) -> int:
    if not users:
        return 1

    return max(int(user_id) for user_id in users) + 1


def capture_face_samples(
    username: str,
    number_of_samples: int = 30
) -> tuple[bool, str]:
    username = username.strip()

    if not username:
        return False, "Please enter a username."

    users = load_users()

    if username.lower() in {
        stored_name.lower() for stored_name in users.values()
    }:
        return False, "This username is already registered."

    user_id = get_next_user_id(users)

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        return False, "The webcam could not be opened."

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    captured_samples = 0

    try:
        while captured_samples < number_of_samples:
            success, frame = camera.read()

            if not success:
                return False, "The webcam frame could not be read."

            grayscale_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = face_detector.detectMultiScale(
                grayscale_frame,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(100, 100)
            )

            for x, y, width, height in faces:
                captured_samples += 1

                face_image = grayscale_frame[
                    y:y + height,
                    x:x + width
                ]

                face_image = cv2.resize(
                    face_image,
                    (200, 200)
                )

                image_path = (
                    DATASET_DIRECTORY
                    / f"user.{user_id}.{captured_samples}.jpg"
                )

                cv2.imwrite(str(image_path), face_image)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Samples: {captured_samples}/{number_of_samples}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            cv2.putText(
                frame,
                "Look at the camera. Press Q to cancel.",
                (20, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.imshow("Face Registration", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                return False, "Registration was cancelled."

    finally:
        camera.release()
        cv2.destroyAllWindows()

    users[str(user_id)] = username
    save_users(users)

    trained, training_message = train_model()

    if not trained:
        return False, training_message

    return True, f"{username} was registered successfully."


def train_model() -> tuple[bool, str]:
    face_images = []
    face_labels = []

    image_files = list(DATASET_DIRECTORY.glob("user.*.*.jpg"))

    if not image_files:
        return False, "No registered face samples were found."

    for image_file in image_files:
        filename_parts = image_file.stem.split(".")

        if len(filename_parts) != 3:
            continue

        try:
            user_id = int(filename_parts[1])
        except ValueError:
            continue

        grayscale_image = cv2.imread(
            str(image_file),
            cv2.IMREAD_GRAYSCALE
        )

        if grayscale_image is None:
            continue

        face_images.append(grayscale_image)
        face_labels.append(user_id)

    if not face_images:
        return False, "No valid face images were available for training."

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.train(
        face_images,
        np.array(face_labels)
    )

    recognizer.write(str(MODEL_FILE))

    return True, "Face model trained successfully."


def authenticate_face(
    timeout_seconds: int = 15
) -> tuple[bool, str]:
    if not MODEL_FILE.exists():
        return False, "No trained face model was found. Register first."

    users = load_users()

    if not users:
        return False, "No registered users were found."

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(MODEL_FILE))

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        return False, "The webcam could not be opened."

    start_time = cv2.getTickCount()
    recognised_frames = 0
    required_frames = 5
    recognised_name = None

    try:
        while True:
            success, frame = camera.read()

            if not success:
                return False, "The webcam frame could not be read."

            grayscale_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = face_detector.detectMultiScale(
                grayscale_frame,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(100, 100)
            )

            current_match = False

            for x, y, width, height in faces:
                face_image = grayscale_frame[
                    y:y + height,
                    x:x + width
                ]

                face_image = cv2.resize(
                    face_image,
                    (200, 200)
                )

                predicted_id, confidence = recognizer.predict(face_image)

                # With LBPH, a lower confidence value represents
                # a closer match.
                if confidence < 65 and str(predicted_id) in users:
                    recognised_name = users[str(predicted_id)]
                    recognised_frames += 1
                    current_match = True

                    label = (
                        f"{recognised_name} "
                        f"({round(100 - confidence)}% match)"
                    )
                    rectangle_colour = (0, 255, 0)
                else:
                    recognised_frames = 0
                    recognised_name = None
                    label = "Unknown user"
                    rectangle_colour = (0, 0, 255)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    rectangle_colour,
                    2
                )

                cv2.putText(
                    frame,
                    label,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    rectangle_colour,
                    2
                )

            if not current_match and not faces:
                recognised_frames = 0

            cv2.putText(
                frame,
                "Press Q to cancel",
                (20, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.imshow("Biometric Authentication", frame)

            if recognised_frames >= required_frames and recognised_name:
                return True, f"Access granted. Welcome, {recognised_name}."

            elapsed_time = (
                cv2.getTickCount() - start_time
            ) / cv2.getTickFrequency()

            if elapsed_time >= timeout_seconds:
                return False, "Authentication timed out. Access denied."

            if cv2.waitKey(1) & 0xFF == ord("q"):
                return False, "Authentication was cancelled."

    finally:
        camera.release()
        cv2.destroyAllWindows()