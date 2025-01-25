# Number Plate Recognition API

This project is a **FastAPI-based application** for recognizing and managing vehicle number plates. It utilizes **YOLO** for object detection and integrates with a database to store, validate, and manage number plate information.

---

## Features

- **Detect** number plates in uploaded images.
- **Validate** if a number plate exists in the database.
- Perform **CRUD operations** (Create, Read, Update, Delete) on vehicle number plate records.

---

## Prerequisites

Ensure the following are installed on your system:

- **Python**: Version `3.11.3`
---

## Environment Setup

1. **Download and extract the `.env` file**:  
   [Click here to download](https://drive.google.com/file/d/1Ga7DGgQz8QwqDq5aPoNpdyt7ZT5sfat7/view?usp=sharing)
   
2. **Place the `.env` file** in the project folder:
   - File name: `numberPlateDetectionEnv`

---

## Setting Up a Virtual Environment and run the project

1. **Install virtualenv** (if not already installed):  
```bash
pip install virtualenv
```
2. **activate  virtualenv**
```bash
numberPlateDetectionEnv\Scripts\activate
```
3. **Run the project:**
```bash
    python main.py

