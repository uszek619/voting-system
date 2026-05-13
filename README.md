# System Głosowania - Młodzieżowe Rady i Organizacje

Kompletny system do zarządzania głosowaniami dla młodzieżowych rad i organizacji.

## Funkcje

✅ Trzy poziomy uprawnień (Superadmin, Admin, User)
✅ Zarządzanie użytkownikami i organizacjami
✅ Tworzenie i zarządzanie głosowaniami
✅ Potwierdzanie frekwencji
✅ Raportowanie wyników
✅ API REST z dokumentacją

## Wymagania

- Python 3.10+
- PostgreSQL 12+
- Node.js 14+ (dla frontend)

## Instalacja

### 1. Klonowanie repozytorium
\`\`\`bash
git clone <repo-url>
cd voting-system
\`\`\`

### 2. Utworzenie wirtualnego środowiska
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
\`\`\`

### 3. Instalacja zależności
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Konfiguracja bazy danych
\`\`\`bash
# Utwórz bazę danych PostgreSQL
createdb voting_system

# Skopiuj .env
cp .env.example .env

# Edytuj .env z Twoimi danymi
\`\`\`

### 5. Migracje bazy danych
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 6. Tworzenie superadmina
\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 7. Uruchomienie serwera
\`\`\`bash
python manage.py runserver
\`\`\`

Serwer powinien być dostępny na: `http://localhost:8000`
Dokumentacja API: `http://localhost:8000/api/docs/`
Admin panel: `http://localhost:8000/admin/`

## API Endpoints

### Autentykacja
- `POST /api/users/auth/login/` - Logowanie (email + hasło)
- `POST /api/users/auth/refresh/` - Odświeżenie tokena

### Użytkownicy
- `GET /api/users/` - Lista użytkowników
- `POST /api/users/` - Tworzenie użytkownika (Admin)
- `GET /api/users/me/` - Moje dane
- `GET /api/users/{id}/` - Szczegóły użytkownika

### Organizacje
- `GET /api/organizations/organizations/` - Lista organizacji (Superadmin)
- `POST /api/organizations/organizations/` - Tworzenie organizacji (Superadmin)

### Kadencje
- `GET /api/organizations/cadences/` - Lista kadencji
- `POST /api/organizations/cadences/` - Tworzenie kadencji (Admin)

### Organy
- `GET /api/organizations/bodies/` - Lista organów
- `POST /api/organizations/bodies/` - Tworzenie organu (Admin)

### Głosowania
- `GET /api/votes/` - Lista głosowań
- `POST /api/votes/` - Tworzenie głosowania (Admin)
- `POST /api/votes/{id}/start/` - Rozpoczęcie głosowania (Admin)
- `POST /api/votes/{id}/end/` - Zamknięcie głosowania (Admin)
- `GET /api/votes/{id}/results/` - Wyniki głosowania
- `POST /api/votes/{id}/cast_vote/` - Oddanie głosu

### Frekwencja
- `GET /api/attendance/` - Moja frekwencja
- `POST /api/attendance/confirm_attendance/` - Potwierdzenie obecności

## Technologia

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Autentykacja**: JWT (SimpleJWT)
- **Dokumentacja**: Swagger (drf-spectacular)

## Struktura Danych

### CustomUser (Użytkownik)
- id (UUID)
- email (unique)
- username
- role (superadmin, admin, user)
- organization (dla adminów)
- is_active
- created_by

### Organization (Organizacja)
- id (UUID)
- name
- description
- is_active

### Cadence (Kadencja)
- id (UUID)
- organization (FK)
- name
- start_date
- end_date

### Body (Organ)
- id (UUID)
- organization (FK)
- name
- body_type (board, committee, revision, other)

### Vote (Głosowanie)
- id (UUID)
- organization (FK)
- title
- vote_type (quorum, regular, amendment)
- status (draft, open, closed, archived)
- participants (M2M with CustomUser)
- start_time, end_time

### VoteOption (Opcja Głosu)
- id (UUID)
- vote (FK)
- text
- order

### UserVote (Oddany Głos)
- id (UUID)
- vote (FK)
- user (FK)
- vote_option (FK)
- timestamp

### Attendance (Frekwencja)
- id (UUID)
- user (FK)
- meeting_date
- is_present
- note

## Testy

\`\`\`bash
python manage.py test
\`\`\`

## Deployment

### Heroku
\`\`\`bash
heroku create
git push heroku main
heroku run python manage.py migrate
heroku config:set DEBUG=False
\`\`\`

## Licencja

MIT

## Wsparcie

W razie problemów, otwórz issue na GitHubie.