# Google-Books-API

- Introduction:
  This guide provides step-by-step instructions to set up the backend. This platform is designed for users to share and explore book recommendations, integrating with the Google Books API.

- Prerequisites:
  Ensure the following tools are installed on your system:
  **Python 3.8+**
  **pip** (Python package manager)
  **virtualenv** (optional but recommended)
  **Git** (to clone the repository)

- Getting Started

1. Clone the Repository
   First, clone the repository to your local machine:

git clone https://github.com/priyanshukatiyar14/Google-Books-API.git
cd Google-Books-API

2. Set Up a Virtual Environment (Optional)

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install Dependencies
   Install all required Python packages:

pip install -r requirements.txt

4. Configure Environment Variables
   Create a .env file in the project root directory and add the following environment variables.
   Add DATABASE_URL, GOOGLE_API_KEY, SECRET_KEY

5. Apply Migrations
   Run the following command to apply the database migrations:

python manage.py migrate

6. Run the Development Server
   Start the Django development server:

python manage.py runserver

Access the project at http://127.0.0.1:8000/ in your web browser.
