# Meal Parliament

A collaborative meal-planning web app for households. Members of a household share one meal calendar, build a library of dishes with their ingredients, and book meals into daily slots.

> **Status:** In active development. The backend API is largely complete; the React frontend currently covers authentication and household management.

## Features

- **User accounts:** registration and login with token authentication
- **Households:** create a household or join one with an invite code (auto-generated, or choose your own)
- **Roles:** household creators are admins, joiners are members
- **Meal items:** create dishes and attach ingredients (many-to-many)
- **Meal slots:** book a dish for a household on a given date and meal type (breakfast, lunch, dinner, snack)
- **Booking rule:** a household can book only one meal per meal type per day, enforced at the database level
- **Admin panel:** customized Django admin with search, filters, and inline member lists

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5, Django REST Framework |
| Auth | DRF token authentication |
| Database | SQLite (development) |
| Frontend | React, Vite, React Router, Axios |
| Other | django-cors-headers |

## Data Model

| Model | Purpose |
|---|---|
| `Household` | A group with a name and a unique invite code |
| `HouseholdMember` | Links a user to a household with a role (many-to-many through table) |
| `Ingredient` | A single ingredient, reused across dishes |
| `MealItem` | A dish, linked to many ingredients |
| `MealSlot` | A booking of a meal item for a household, date, and meal type |

## API Endpoints

| Endpoint | Description |
|---|---|
| `POST /api/register/` | Create an account and receive a token |
| `POST /api/login/` | Log in and receive a token |
| `/api/households/` | List and create your households |
| `POST /api/households/join/` | Join a household with an invite code |
| `/api/household-members/` | View members of your households |
| `/api/meal-items/` | Create and browse meal items |
| `/api/ingredients/` | Create and browse ingredients |
| `/api/meal-slots/` | Book and view meal slots for your households |

All endpoints except register and login require the header `Authorization: Token <your-token>`.

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 20+

### Backend

```bash
git clone https://github.com/mustavi25/Meal-Parliament.git
cd Meal-Parliament

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/` and the admin panel at `/admin/`.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```
VITE_API_URL=http://127.0.0.1:8000/api
```

Then start the dev server:

```bash
npm run dev
```

Open `http://localhost:5173`. Both servers must be running at the same time.

## Project Structure

```
Meal-Parliament/
├── accounts/        # Registration, login, API auth
├── households/      # Households and membership
├── meals/           # Meal items, ingredients, meal slots
├── mealparliament/  # Django project settings and URLs
├── templates/       # Server-rendered pages
└── frontend/        # React + Vite app
```

## Roadmap

- [ ] React meal plan page (view and book meal slots per household)
- [ ] Create meal items and ingredients from the React UI
- [ ] Auto-generated shopping list from booked meals
- [ ] Meal suggestions with member voting
- [ ] Production database and deployment

## License

Add a license of your choice (for example, MIT).
