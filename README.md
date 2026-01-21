# 🚀 Django Starter Kit (Clean, Modern, No Nonsense)

A **modern Django starter kit** built for developers who want:

- real authentication (not demos),
- clean architecture (not magic),
- modern UX without a frontend build step,
- and code they’ll still understand in 6 months.

This project is opinionated — **on purpose**.

---

## ✨ What Is This?

This starter kit gives you a **production-ready Django foundation** with:

- Email-based authentication
- User profiles with avatars
- Profile onboarding flow
- Email verification & email change handling
- HTMX + Alpine.js interactivity
- Tailwind styling (via CDN)
- A real design system
- Clean signal usage (no side effects)

No SPA.
No overengineering.
No “why is this happening?” moments.

---

## 🧱 Tech Stack

### Backend

- **Django 6**
- **django-allauth** – authentication, email verification
- **SQLite** (easy dev, replaceable later)
- **django-cleanup** – auto-delete old uploaded files
- **django-extensions** – developer utilities
- **django-htmx** – first-class HTMX support
- **Jazzmin** – clean admin UI

### Frontend

- **Tailwind CSS (CDN)** – zero build step
- **Alpine.js** – UI state & interactions
- **HTMX** – partial updates, no SPA complexity
- **Bootstrap Icons**

### Forms

- **django-crispy-forms**
- **crispy-tailwind**

---

## 📦 Installed Packages

```txt
Django
django-allauth
django-htmx
django-crispy-forms
crispy-tailwind
django-cleanup
django-extensions
django-jazzmin
python-dotenv
pillow
```

Every dependency is used.
Nothing here is “just in case”.

---

## 👤 Authentication & Accounts

### Email-Based Auth (Allauth)

- Login & signup via email
- Email required
- Email verification supported
- Manual resend verification
- Safe email change flow

### Important Design Choice

> **No emails are sent from signals**

Signals only:

- create profiles
- sync email state

Emails are sent **explicitly from views**, based on user intent.

This avoids hidden side effects and accidental email spam.

---

## 👥 User Profiles

Each user gets:

- A `Profile` model (auto-created)
- Avatar upload
- Display name fallback logic
- Optional bio/info text

### Profile URLs

- **Your profile:** `/profile/`
- **Public profiles:** `/@username`

---

## ✨ Profile Onboarding

New users are redirected to a **profile onboarding flow**:

- Friendly welcome message
- Avatar upload with live preview
- Display name setup
- Same form as “edit profile”, different UX

Onboarding is controlled via routing — not duplicated logic.

---

## 🖼️ Avatar Upload (Done Right)

- Image upload via Django `ImageField`
- Live preview using Alpine.js
- File input hidden
- Custom trigger button
- No JS frameworks
- No hacks

Old avatars are automatically cleaned up thanks to `django-cleanup`.

---

## 📨 Email Management (Robust & Safe)

- Email stored in `User`
- Synced to `EmailAddress` (primary enforced)
- Verification reset on email change
- Manual resend verification endpoint
- Duplicate email prevention

Everything is explicit, predictable, and testable.

---

## ⚡ HTMX + Alpine.js

This project uses:

- **HTMX** for partial updates (email edit form)
- **Alpine.js** for:
  - avatar preview
  - dropdowns
  - transitions
  - UI state

No React.
No Vue.
No build pipeline.

Just HTML that reacts.

---

## 🎨 Design System

A lightweight **CSS variable–based design system**:

- Semantic colors:
  - `primary`
  - `accent`
  - `neutral`
  - `success`
  - `warning`
  - `error`

- Consistent buttons
- Unified form styling
- Reusable utility classes

Tailwind handles layout.
The design system handles meaning.

---

## 🧠 Architecture Principles

This repo follows a few strict rules:

- **Signals = data integrity**
- **Views = side effects**
- **No business logic in templates**
- **No emails in signals**
- **Explicit > clever**

The goal is code that is easy to reason about, not impress.

---

## 🗂️ Project Structure (Simplified)

```txt
a_core/        # Project config
a_home/        # Public home page
a_users/       # Auth, profiles, settings
templates/     # Global layouts & partials
static/        # Static assets
media/         # User uploads
```

Everything lives where you expect it.

---

## 🔑 Environment Variables

Sensitive data lives in `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=you@gmail.com
EMAIL_HOST_PASSWORD=app-password
DEFAULT_FROM_EMAIL=you@gmail.com
```

`.env` is ignored by Git.

---

## 🚀 Getting Started

```bash
git clone https://github.com/EslamKamel89/django-starter.git
cd django-starter

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🎯 Who Is This For?

- Django developers building real products
- SaaS / MVP / internal tools
- People who want modern UX without SPA complexity
- Developers who value clarity over cleverness

---

## 📜 License

MIT — use it, fork it, ship it, improve it.

---

## 🧠 Final Words

This starter kit doesn’t try to do everything.

It tries to do **the important things well**.

If you understand this codebase,
you understand Django.

Happy building 🚀
