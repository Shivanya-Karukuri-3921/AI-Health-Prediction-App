# AI Health Prediction Application

## Project Overview

This project is a Healthcare AI Prediction Application developed using Python and Streamlit.

The application allows users to:
- Add patient records
- View patient records
- Update patient details
- Delete patient records
- Predict possible health risks using AI logic
- Integrate external AI API services

The system uses SQLite database for persistent storage and Streamlit for the frontend interface.

---

## Features

- CRUD Operations
- SQLite Database Integration
- AI Health Prediction
- External AI API Integration
- Search Functionality
- Dashboard Metrics
- Input Validation
- User-Friendly Interface

---

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Requests API

---

## Health Prediction Logic

The application predicts possible risks based on:
- Glucose Level
- Cholesterol Level
- Haemoglobin Level

Example Predictions:
- High Diabetes Risk
- Heart Disease Risk
- Anemia Risk

---

## External API Used

The project integrates with:
https://api.agify.io

This API is used to demonstrate external REST API integration and JSON data handling.

---

## How to Run the Project

### Install Requirements

pip install -r requirements.txt

### Run Application

streamlit run app.py

---

## Project Structure

AI-Health-Prediction-App/

│

├── app.py

├── patients.db

├── requirements.txt

└── README.md

---

## Future Improvements

- Real Machine Learning Model
- Cloud Deployment
- User Authentication
- Advanced Healthcare Analytics
- PDF Report Generation

---

## Author

Shivanya Karukuri