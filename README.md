# Andhra Spices - Food Ordering Web App

## Overview

**Andhra Spices** is a full-stack web application for discovering restaurants, browsing menus, and ordering food online. The app is built using Flask (Python) for the backend, SQLite for the database, and HTML/CSS/JavaScript for the frontend. It features a modern UI, user authentication, cart management, and a responsive design.

---

## Features

- **Restaurant Discovery:** Browse a curated list of popular restaurants with images, cuisine types, and ratings.
- **Menu Browsing:** View detailed menus for each restaurant, including dish images, prices, and ratings.
- **Cart System:** Add or remove menu items to/from your cart, adjust quantities, and view a summary before placing an order.
- **User Authentication:** Signup and login functionality with session management.
- **Order Placement:** Place orders with a success animation and automatic cart clearing.
- **Responsive Design:** Works seamlessly on desktop and mobile devices.
- **Account Dropdown:** View user details and logout from the navigation bar.
- **Footer:** Includes links to products, resources, about, and contact information.

---


## Screenshots

<img width="1440" height="2544" alt="127 0 0 1_5000" src="https://github.com/user-attachments/assets/2b0479b2-08a6-4cab-9582-9bb21835bc39" />

<img width="2880" height="1734" alt="127 0 0 1_5000_cart" src="https://github.com/user-attachments/assets/764601f4-4586-4017-a139-03e0279b3385" />

<img width="2880" height="2131" alt="127 0 0 1_5000_signup" src="https://github.com/user-attachments/assets/a2a553c4-8a83-4ce8-8642-f8b1a203de53" />

<img width="2880" height="1826" alt="127 0 0 1_5000_login" src="https://github.com/user-attachments/assets/d81d5725-faa1-4b18-98f9-2b9b58305380" />

## Folder Structure

```
AndhraSpices/
├── README.md
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── instance/
│       └── db.sqlite3
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── images/
│   │   └── [all images used in the app]
│   └── js/
│       └── scripts.js
└── templates/
    ├── base.html
    ├── cart.html
    ├── index.html
    ├── login.html
    ├── restaurant.html
    └── signup.html
```

---

## How It Works

### 1. Home Page (`index.html`)
- Displays a carousel of banner images.
- Lists all restaurants with images, cuisine, and ratings.
- Clicking a restaurant opens its menu.

### 2. Restaurant Page (`restaurant.html`)
- Shows restaurant details and menu items.
- Users can add menu items to their cart.
- "Add" button toggles to "Added" if the item is in the cart.

### 3. Cart Page (`cart.html`)
- Shows all items in the cart with quantity controls.
- Displays total price including delivery charges.
- "Place Order" button triggers a success animation and clears the cart.

### 4. Authentication (`login.html`, `signup.html`)
- Users can sign up with their details (full name, mobile, address, email, password).
- Login with email and password.
- Session management keeps users logged in.

### 5. Account Dropdown
- Shows user info (name, email, mobile, address) if logged in.
- Logout button available.

### 6. Footer
- Contains links to products, resources, about, and contact info.
- Social media icons.

---

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript, Jinja2 templates
- **Icons:** Font Awesome

---

## Setup Instructions

### 1. Install Dependencies

Navigate to the `backend` folder and install requirements:

```sh
pip install -r requirements.txt
```

### 2. Run the App

From the `backend` folder, start the Flask server:

```sh
python app.py
```

The app will be available at `http://localhost:5000`.

### 3. Database Initialization

On first run, the app will automatically create and populate the SQLite database (`db.sqlite3`) with sample restaurants and menu items.

---

## Customization

- **Add Restaurants/Menu Items:** Edit the `restaurant_data` and `food_items_by_restaurant` dictionaries in [`backend/app.py`](backend/app.py).
- **Change Styles:** Modify [`static/css/styles.css`](static/css/styles.css).
- **Update Images:** Place new images in [`static/images/`](static/images/).
- **Edit Templates:** Update HTML files in [`templates/`](templates/).

---

## File Descriptions

- [`backend/app.py`](backend/app.py): Main Flask application, routes, and logic.
- [`backend/models.py`](backend/models.py): SQLAlchemy models for User, Restaurant, MenuItem.
- [`backend/requirements.txt`](backend/requirements.txt): Python dependencies.
- [`static/css/styles.css`](static/css/styles.css): All CSS styles.
- [`templates/base.html`](templates/base.html): Base template with navbar and footer.
- [`templates/index.html`](templates/index.html): Home page.
- [`templates/restaurant.html`](templates/restaurant.html): Restaurant menu page.
- [`templates/cart.html`](templates/cart.html): Cart and order page.
- [`templates/login.html`](templates/login.html): Login form.
- [`templates/signup.html`](templates/signup.html): Signup form.

---

## Security Notes

- Passwords are stored in plain text for demo purposes. For production, use password hashing.
- The app uses Flask sessions for authentication.

---

## Credits

- Images and icons are for demonstration purposes.
- Inspired by popular food delivery platforms.

---

## License

This project is for educational/demo use. Please check image/icon licenses before commercial use.

---

## Contact

For questions or feedback,
