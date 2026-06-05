# Ambulance Management System Using Flask

A simple beginner-friendly Flask project for managing emergency ambulance requests.

## Features

- Patient emergency request form
- Admin dashboard
- Ambulance dispatch system
- Complete request workflow
- Fleet status tracking
- Demo reset option

## How to Run

1. Install Python 3.
2. Open this folder in terminal.
3. Install Flask:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
python app.py
```

5. Open this link in your browser:

```text
http://127.0.0.1:5000
```

## Fixed Error

The dashboard was using `url_for('assign_ambulance')`, but the `assign_ambulance` route was missing from `app.py`. The route has been added, so ambulance dispatch now works properly.
