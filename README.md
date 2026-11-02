# LifeDrop

A Django web app that connects **blood donors** with people who urgently need their
type, nearby. COMP 8347 – Internet Applications / Distributed Systems · Group 6 ·
University of Windsor · Fall 2026.

## Team & file ownership (2 models each)

Every member owns their own module files, so we can work without clashing.

| Member | Focus | Models file | Views file | Forms file |
|---|---|---|---|---|
| Sujith Chitram | Requests & fixtures | `donors/models/m_sujith.py` | `donors/views/v_sujith.py` | `donors/forms/f_sujith.py` |
| Venkata Charan Sai Doniparthi | Search & image uploads | `donors/models/m_charan.py` | `donors/views/v_charan.py` | `donors/forms/f_charan.py` |
| Sneha Gunturu | Design, footer, pages | `donors/models/m_sneha.py` | `donors/views/v_sneha.py` | `donors/forms/f_sneha.py` |
| Nikhil Goud Nathi | Accounts & auth | `donors/models/m_nikhil.py` | `donors/views/v_nikhil.py` | `donors/forms/f_nikhil.py` |
| Sai Srinivas Uppara | Messaging & user history | `donors/models/m_sai.py` | `donors/views/v_sai.py` | `donors/forms/f_sai.py` |

Templates are split the same way (Sneha owns `base.html` + the static pages,
Nikhil owns the `registration/` auth pages, etc.).

## Run it

```bash
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_data
python manage.py runserver
```

Open http://127.0.0.1:8000/

**Demo accounts** (password `donor1234`): `rahul`, `sara`, `wei`, `amara`.
Admin: `admin` / `admin12345` at `/admin/`.

## Tests

```bash
python manage.py test donors
```

## Progress — this is the ~60% milestone

**Done and working**
- All **10 models** (2 per member) with migrations, admin, and a JSON fixture (`loaddata`)
- **Auth**: register, login, logout, password reset by email
- **Home** (`ListView`) with keyword / blood-type / city **search**
- **Request detail** (`DetailView`) with offer-to-donate and message buttons
- **Post / edit** a request + requisition **photo upload**
- **Donor profile** + donor-card upload (`FileField`) → Verified-donor badge
- **Guest vs member** gating, Bootstrap theme, footer, About / Contact / Team
- 8 passing tests

**Remaining (~40%, split across the team — see the `TODO` notes in the code)**
- Sai Srinivas — inbox page + user-history page (sessions/cookies view)
- Sneha — leave-a-review flow
- Sujith — mark a request as fulfilled
- Charan — saved requests (bookmark in the session)
- Everyone — polish templates and add more tests
