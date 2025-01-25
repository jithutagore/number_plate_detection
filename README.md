# Number Plate Recognition API

This project is a FastAPI-based application for recognizing and managing vehicle number plates. It uses YOLO for object detection and integrates with a database to store, validate, and manage number plate information.

## Features
- Detect number plates in uploaded images.
- Validate if a number plate exists in the database.
- Add, update, delete, and retrieve vehicle number plate records.

---

## Prerequisites

Ensure you have the following installed:
- **Python**: Version `3.11.3`
- **pip**: Python's package installer
- **Database**: A database (like PostgreSQL or MySQL) to store plate records.
- **Dependencies**: OpenCV, FastAPI, Uvicorn, dotenv, and other Python libraries listed in `requirements.txt`.

