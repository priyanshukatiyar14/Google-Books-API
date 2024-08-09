# Google-Books-API

## Introduction

This guide provides step-by-step instructions to set up the backend for a platform designed for users to share and explore book recommendations. The platform integrates with the Google Books API.

## Prerequisites

Ensure the following tools are installed on your system:

- **Python 3.8+**
- **pip** (Python package manager)
- **virtualenv** (optional but recommended)
- **Git** (to clone the repository)

## Getting Started

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/priyanshukatiyar14/Google-Books-API.git
cd Google-Books-API
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

Create and activate a virtual environment:

On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory and add the following environment variables:

```
DATABASE_URL=your_database_url_here
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_secret_key_here
```

Replace `your_database_url_here`, `your_google_api_key_here`, and `your_secret_key_here` with your actual credentials.

### 5. Apply Migrations

Run the following command to apply the database migrations:

```bash
python manage.py migrate
```

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Access the project in your web browser at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
