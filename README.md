# 🌾 Agri-Inputs Marketplace (Django Templates Version)

A full-stack **Python/Django-based Agri-Inputs Marketplace** enabling **direct transactions between farmers and suppliers**. This version is built using **Django Templates** for rendering the frontend, without React. It includes product listings, a cart and checkout system via **Stripe**, user authentication, and product rating and review functionality.

---

## 🚀 Key Features

- 👨‍🌾 Farmer-supplier product marketplace
- 🛍 Product catalog with categories: Seeds, Fertilizers, Pesticides, Equipment
- 🧺 Cart & Stripe-powered checkout
- 🔐 JWT-based authentication for secure login/registration
- ⭐ User ratings, reviews, and product recommendations
- 🛠 Admin dashboard for managing users, products, orders

---

## 🧰 Tech Stack

### Backend
- **Framework**: Django + Django REST Framework (optional)
- **Database**: PostgreSQL (preferred) or SQLite (for development)
- **Auth**: JWT (via `djangorestframework-simplejwt`)
- **Payments**: Stripe API

### Frontend
- **Templating**: Django Templates
- **Styling**: Tailwind CSS or Bootstrap

---

## 📁 Project Structure

```bash
agri_inputs_marketplace/
├── agri_marketplace/       # Main Django project
│   ├── settings.py
│   └── urls.py
├── products/               # App for product listings
├── users/                  # App for authentication and profiles
├── orders/                 # Cart and checkout system
├── reviews/                # Ratings and reviews
├── templates/              # HTML templates (shared across apps)
│   └── base.html           # Base layout with navbar/footer
├── static/                 # CSS, JS, images
├── manage.py
└── README.md
⚙️ Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/agri-inputs-marketplace.git
cd agri-inputs-marketplace
2. Create and Activate Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Up .env File
Create a .env file in the project root with the following:

ini
Copy
Edit
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
5. Apply Migrations
bash
Copy
Edit
python manage.py migrate
6. Create Superuser
bash
Copy
Edit
python manage.py createsuperuser
7. Run the Development Server
bash
Copy
Edit
python manage.py runserver
💳 Stripe Payment Setup
Sign up at Stripe and get your API keys.

Add them to .env.

Integrate with Stripe Checkout or Elements in your Django views and templates.

🔐 Authentication
Handled using JWT via djangorestframework-simplejwt.

Users can register/login via Django views.

Token-based protection for secure order processing APIs (optional).

🧾 Admin Panel
Access the Django Admin at /admin/:

Manage users

Add/edit/delete products

View orders and payments

Moderate reviews

🧪 Testing
Run unit tests using Django’s built-in test framework:

bash
Copy
Edit
python manage.py test
🧠 Future Enhancements
Smart recommendations based on purchase and review history

Supplier-side product management dashboard

Order delivery status tracking

Search and filtering with autocomplete

🪪 License
This project is licensed under the MIT License.

🤝 Contributing
Contributions, feature requests, and bug reports are welcome. Feel free to fork the repo and submit pull requests.

📬 Contact
Your Name
Email: inekeonubifelix@gmail.com
GitHub: @yinekeche
