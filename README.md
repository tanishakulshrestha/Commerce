# Commerce
An eBay-like online auction web application built using Django, where users can create listings, place bids, manage auctions, and track winners.
🚀 Features

🔐 User Authentication (Register / Login / Logout)

📦 Create auction listings with image, category, and starting bid

💰 Real-time bidding system with bid validation

🏆 Automatically tracks highest bid & winning user

⏳ Auction closing functionality (owner only)

👀 Watchlist for favorite listings

💬 Comment system for listings

🛠 Admin panel for managing users, listings, bids, and comments

📢 User feedback using Django messages framework

🧠 Business Logic Implemented

Users cannot bid on their own listings

Bids must be higher than the current highest bid

Closed auctions reject new bids

Winning bidder is stored when auction is closed

Active listings are dynamically filtered

🛠 Tech Stack

Backend: Django (Python)

Database: SQLite

Frontend: HTML, CSS (Django Templates)
commerce/
│
├── auctions/
│   ├── models.py        # Listing, Bid, Comment models
│   ├── views.py         # Business logic & views
│   ├── urls.py          # App routes
│   ├── templates/
│   └── static/
│
├── commerce/
│   ├── settings.py
│   ├── urls.py
│
└── manage.py
⚙️ How to Run Locally
# Clone the repository
git clone https://github.com/your-username/commerce-auction.git

# Move into project directory
cd commerce

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver

Authentication: Django Auth System

Version Control: Git & GitHub
Then open:
👉 http://127.0.0.1:8000/
