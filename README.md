# 🔐 Biometric Authentication System

A desktop-based biometric authentication system developed using **Python**, **OpenCV**, and **CustomTkinter**. The application allows users to register their face using a webcam and authenticate their identity through facial recognition.

---

## Features

- 👤 Face registration using a webcam
- 🔍 Face authentication with OpenCV LBPH Face Recognizer
- 💻 Modern desktop interface built with CustomTkinter
- 📷 Automatic face detection using Haar Cascade Classifier
- 🗂 Local storage of biometric data
- ⚡ Multi-threaded webcam processing for a responsive GUI
- 📢 Real-time authentication status and notifications

---

## Technologies Used

- Python
- OpenCV (opencv-contrib-python)
- CustomTkinter
- NumPy
- Pillow

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/nehaa2003/Biometric-Authentication-System.git
```

### 2. Navigate to the project folder

```bash
cd Biometric-Authentication-System
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

---

## Project Structure

```
Biometric-Authentication-System/
│
├── main.py
├── gui.py
├── biometric_system.py
├── requirements.txt
├── README.md
├── .gitignore
├── dataset/
└── model/
```

---

## How It Works

### Face Registration

1. Enter a username.
2. Click **Register Face**.
3. The webcam captures multiple face samples.
4. Face samples are stored locally.
5. A face recognition model is trained automatically.

### Face Authentication

1. Click **Authenticate Face**.
2. The webcam captures the user's face.
3. The trained model compares the face with registered users.
4. Access is granted if a match is found.

---

## Screenshots

### Main Interface

_Add a screenshot here_

### Face Registration

_Add a screenshot here_

### Authentication

_Add a screenshot here_

---

## Future Improvements

- Liveness detection to prevent photo spoofing
- Fingerprint authentication support
- Multi-factor authentication
- User management dashboard
- SQLite/MySQL database integration
- Authentication history logs
- Face recognition confidence analytics

---

## Disclaimer

This project was developed for educational and portfolio purposes. It demonstrates the fundamentals of biometric authentication and is **not intended for production use**. Additional security measures such as liveness detection and stronger anti-spoofing techniques would be required for real-world deployments.

---

## Author

**Sinehaa Paramasivam**

Bachelor of Computer Science (Cyber Security)

Multimedia University (MMU)