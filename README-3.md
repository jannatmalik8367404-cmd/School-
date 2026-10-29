# School Management System

A beginner-friendly Python web app made with Streamlit.

## Features
- Dashboard statistics
- Add and search student records
- Mark attendance
- Save student marks and calculate percentages
- Download student, attendance, and result data as CSV

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   streamlit run app.py
   ```

## Deploy on Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Select **Create app**, choose your repository and branch, and set the main file path to `app.py`.
4. Click **Deploy**.

## Data note
This learning demo stores records in Streamlit session memory. Data can reset when a session restarts. Use a database for persistent, real-world use. Do not enter real sensitive student information.
