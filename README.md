<div align="center">

<img src="static/Gazette.svg" alt="CGS IB Gazette" width="300"/>

### `THE GAZETTE // STOP THE PRESSES, START THE SERVER`

*a full-stack CMS for the school's student-run newspaper. deadline was yesterday.*

![deadline](https://img.shields.io/badge/deadline-yesterday-1a1a1a?style=flat-square&labelColor=f9f6f0)
![typography](https://img.shields.io/badge/typography-EB_Garamond._we're_serious-1a1a1a?style=flat-square&labelColor=f9f6f0)
![license](https://img.shields.io/badge/AGPLv3-forks_stay_open-8b0000?style=flat-square&labelColor=f9f6f0)
![editors](https://img.shields.io/badge/editors-students._fearless-8b0000?style=flat-square&labelColor=f9f6f0)
![corrections](https://img.shields.io/badge/corrections-printed_promptly-1a1a1a?style=flat-square&labelColor=f9f6f0)

</div>

---

## 🗞️ What is this

The **CGS IB Gazette** — a Flask + PostgreSQL content management system
powering the school's student newspaper. Writers submit through an open
portal, editors moderate from an admin dashboard, readers browse by category,
tag, or search. Editorial design to match: EB Garamond headlines, Source Sans
Pro body, warm cream palette (`#F9F6F0`, `#EFEBE0`). A broadsheet that
happens to be a web app.

```console
editor@gazette:~$ status --edition latest
[✓] 5 categories live. submissions open. admin caffeinated.
[!] one article still "almost done". it has been "almost done" since tuesday.
```

## 📰 The desk

| | section | what it actually does |
|---|---|---|
| 01 | **multi-category system** | Student Life, Student Projects, Volunteering/CAS, Business, Technology |
| 02 | **submission portal** | open contribution pipeline for student writers |
| 03 | **admin dashboard** | moderation and publishing workflow — the editor's desk |
| 04 | **tag system** | color-coded badges, tag pages, visual categorization |
| 05 | **search** | find that article from three editions ago |
| 06 | **responsive layout** | desktop, tablet, phone — the paperboy delivers everywhere |

## 🚀 Run it

```bash
git clone https://github.com/nitrimandylis/IB-News-site.git
cd IB-News-site
pip install -r requirements.txt

python init_db.py        # builds the schema from schema.sql
python server.py         # the presses start rolling
```

Needs a PostgreSQL instance and the usual `.env` secrets
(python-dotenv reads them, Flask-HTTPAuth guards the admin desk).

## 🔩 Under the hood

| layer | tech | job |
|---|---|---|
| backend | Flask + Gunicorn | routes, auth, the whole newsroom |
| database | PostgreSQL + psycopg2 | articles, tags, the archive |
| schema | `schema.sql` + `init_db.py` | the printing plates |
| auth | Flask-HTTPAuth | keeps randoms off the editor's desk |
| frontend | Jinja2 + CSS + JS | the broadsheet itself |
| templating extras | `templatetags/tag_helpers.py` | the tag badge machinery |

| file | job |
|---|---|
| `server.py` | main Flask application |
| `templates/` | index, article, submit, admin, search, tag pages |
| `static/Gazette.svg` | the masthead above |
| `static/style.css` | EB Garamond, cream tones, editorial accents |

---

<div align="center">

**[Nick Trimandylis](https://github.com/nitrimandylis)**

`ALL THE NEWS THAT FITS THE SCHEMA`

GNU AGPL v3 — see [LICENSE](LICENSE). Any fork hosted as a network service
must also be open source. The Gazette protects its sources *and* its source.

</div>
