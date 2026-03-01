<p align="center">
  <img src="static/Gazette.svg" alt="CGS IB Gazette" width="300"/>
</p>

<p align="center">
  <strong>CGS IB Gazette</strong><br>
  The student-run digital newspaper project
</p>


## Overview

A full-stack Flask web application powering the CGS IB Gazette — the school's
student newspaper. Features article publishing, an admin dashboard, category
filtering, and a PostgreSQL-backed content management system.

## ✨ Features

### Content Management
- **Multi-Category System** – Organized by Student Life, Student Projects, Volunteering/CAS, Business, and Technology
- **Submission Portal** – Open contribution system for student writers
- **Admin Dashboard** – Content moderation and publishing workflow

### Design
- **Elegant Typography** – EB Garamond headlines + Source Sans Pro body text
- **Responsive Layout** – Optimized for desktop, tablet, and mobile
- **Color Palette** – Warm cream tones (#F9F6F0, #EFEBE0) with editorial accents
- **Tag System** – Visual categorization with color-coded badges


## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask · Gunicorn |
| Database | PostgreSQL · psycopg2 |
| Auth | Flask-HTTPAuth · python-dotenv |
| Frontend | HTML · CSS · JavaScript |
| Schema | schema.sql · init_db.py |

## Project Structure

```
IB-News-site/
├── server.py          # Main Flask application
├── init_db.py         # Database initialisation script
├── schema.sql         # SQL schema
├── requirements.txt
├── static/
│   ├── Gazette.svg    # Logo
│   ├── style.css
│   └── script.js
└── templates/         # Jinja2 HTML templates
```

## License

GNU Affero General Public License v3.0 — see [LICENSE](LICENSE) for details.
Any fork hosted as a network service must also be open source.
