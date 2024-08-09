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

## Endpoints

### `POST /signup/`

#### Description:

This endpoint allows a new user to create an account by providing their details. The password is securely hashed before being saved to the database.

#### Request Body:

- **email** (string, required): The email address of the user.
- **password** (string, required): The user's password.
- **other fields** (optional): Any additional fields required by the `UserSerializer`.

#### Example Request:

```json
{
  "email": "example@example.com",
  "password": "securePassword123",
  "name": "John",
  "username": "Doe"
}
```

#### Responses:

- **201 Created**:
  - **Description**: The user was successfully created.
  - **Body**:
    ```json
    {
      "id": 1,
      "email": "example@example.com",
      "name": "John",
      "username": "Doe",
      "other_fields": "..."
    }
    ```
- **400 Bad Request**:
  - **Description**: The provided data was invalid.
  - **Body**:
    ```json
    {
      "error_field": ["error message"]
    }
    ```

### `POST /signin/`

#### Description:

This endpoint allows a registered user to log in by providing their email and password. Upon successful authentication, the user receives an access token and a refresh token.

#### Request Body:

- **email** (string, required): The user's registered email address.
- **password** (string, required): The user's password.

#### Example Request:

```json
{
  "email": "example@example.com",
  "password": "securePassword123"
}
```

#### Responses:

- **200 OK**:
  - **Description**: The user was successfully authenticated.
  - **Body**:
    ```json
    {
      "access_token": "Bearer ACCESS_TOKEN_STRING",
      "refresh_token": "Bearer REFRESH_TOKEN_STRING",
      "user": {
        "id": "uuid_value",
        "email": "example@example.com",
        "name": "John",
        "username": "Doe",
        "other_fields": "..."
      }
    }
    ```
- **400 Bad Request**:

  - **Description**: The provided email or password was incorrect, or one of them was missing.
  - **Body**:
    ```json
    {
      "error": "email and password are required"
    }
    ```
    or
    ```json
    {
      "error": "Invalid email"
    }
    ```
    or
    ```json
    {
      "error": "Invalid password"
    }
    ```

- **500 Internal Server Error**:
  - **Description**: An unexpected error occurred on the server.
  - **Body**:
    ```json
    {
      "error": "Error message"
    }
    ```

### `POST /books/`

#### Description:

This endpoint allows users to search for books by their title. The search utilizes the Google Books API to retrieve a list of books that match the provided title.

#### Request Body:

- **book_name** (string, required): The title of the book to search for.

#### Example Request:

```json
{
  "book_name": "The Great Gatsby"
}
```

#### Responses:

- **200 OK**:
  - **Description**: A list of books matching the provided title.
  - **Body**:
    ```json
    [
        {
            "title": "The Great Gatsby",
            "author": ["F. Scott Fitzgerald"],
            "description": "A novel about the American dream...",
            "cover_image": "http://books.google.com/thumbnail.jpg",
            "ratings": 4.2
        },
        ...
    ]
    ```
- **400 Bad Request**:

  - **Description**: The `book_name` parameter was not provided.
  - **Body**:
    ```json
    {
      "error": "book_name is required"
    }
    ```

- **502 Bad Gateway**:

  - **Description**: The Google Books API returned an invalid JSON response.
  - **Body**:
    ```json
    {
      "error": "Invalid JSON response"
    }
    ```

- **500 Internal Server Error**:
  - **Description**: An unexpected error occurred while processing the request.
  - **Body**:
    ```json
    {
      "error": "Error message"
    }
    ```

### `POST /books/query/`

#### Description:

This endpoint allows users to search for books using multiple parameters such as keywords, authors, and categories. The search leverages the Google Books API to find books that match any of the provided parameters.

#### Request Body:

- **keywords** (string, optional): Keywords to search in the book title.
- **authors** (string, optional): Author name(s) to search for.
- **categories** (string, optional): Book categories to search in.

#### Example Request:

```json
{
  "keywords": "Python programming",
  "authors": "Guido van Rossum",
  "categories": "Computers"
}
```

#### Responses:

- **200 OK**:
  - **Description**: A list of books matching the search criteria.
  - **Body**:
    ```json
    [
        {
            "title": "Learning Python",
            "author": ["Mark Lutz"],
            "description": "This book offers a comprehensive, in-depth introduction to the core Python language...",
            "cover_image": "http://books.google.com/thumbnail.jpg",
            "ratings": 4.5
        },
        ...
    ]
    ```
- **400 Bad Request**:

  - **Description**: No search parameters were provided in the request body.
  - **Body**:
    ```json
    {
      "error": "At least one search parameter (keywords, authors, or categories) is required"
    }
    ```

- **502 Bad Gateway**:

  - **Description**: The Google Books API returned an invalid JSON response.
  - **Body**:
    ```json
    {
      "error": "Invalid JSON response"
    }
    ```

- **500 Internal Server Error**:
  - **Description**: An unexpected error occurred while processing the request.
  - **Body**:
    ```json
    {
      "error": "Error message"
    }
    ```

### `POST /recommend/`

#### Description:

This endpoint allows users to submit a book recommendation. The recommendation will be associated with the user making the submission.

#### Request Body:

- **title** (string, required): The title of the book.
- **author** (string, required): The author(s) of the book.
- **genre** (string, optional): The genre of the book.
- **rating** (float, optional): The rating of the book.
- **publication_date** (date, optional): The publication date of the book.

#### Example Request:

```json
{
  "title": "1984",
  "author": "George Orwell",
  "genre": "Dystopian",
  "rating": 4.8,
  "publication_date": "1949-06-08"
}
```

#### Responses:

- **201 Created**:
  - **Description**: The book recommendation was successfully created.
  - **Body**:
    ```json
    {
      "id": "uuid",
      "title": "1984",
      "author": "George Orwell",
      "genre": "Dystopian",
      "rating": 4.8,
      "publication_date": "1949-06-08",
      "submitted_by": "user_id"
    }
    ```
- **400 Bad Request**:
  - **Description**: The provided data was invalid.
  - **Body**:
    ```json
    {
      "error_field": ["error message"]
    }
    ```

### `GET /recommend/`

#### Description:

This endpoint allows users to retrieve a list of recommended books, filtered and sorted based on query parameters.

#### Query Parameters:

- **genre** (string, optional): Filter by genre.
- **min_rating** (float, optional): Filter by a minimum rating.
- **max_rating** (float, optional): Filter by a maximum rating.
- **publication_date** (date, optional): Filter by the publication date.
- **sort_by** (string, optional, default="title"): Sort the results by the specified field.

#### Example Request:

```
GET /recommend/?genre=Dystopian&min_rating=4.0&sort_by=rating
```

#### Responses:

- **200 OK**:
  - **Description**: A list of recommended books matching the filters and sort criteria.
  - **Body**:
    ```json
    [
        {
            "id": "uuid",
            "title": "1984",
            "author": "George Orwell",
            "genre": "Dystopian",
            "rating": 4.8,
            "publication_date": "1949-06-08",
            "submitted_by": "user_id",
            "total_likes": 5,
            "comments": 3,
            "comment_list": ["Great book!", "Loved it!", "A must-read."]
        },
        ...
    ]
    ```

### `PUT/PATCH/DELETE /recommend/<uuid:pk>/`

#### Description:

This endpoint allows users to update or delete a specific book recommendation by its UUID.

#### Path Parameter:

- **uuid** (UUID, required): The UUID of the book recommendation.

#### Example Request:

```json
PUT /recommend/123e4567-e89b-12d3-a456-426614174000/
{
    "title": "1984",
    "author": "George Orwell",
    "rating": 4.9
}
```

#### Responses:

- **200 OK** (PUT/PATCH):
  - **Description**: The book recommendation was successfully updated.
  - **Body**:
    ```json
    {
      "id": "uuid",
      "title": "1984",
      "author": "George Orwell",
      "genre": "Dystopian",
      "rating": 4.9,
      "publication_date": "1949-06-08",
      "submitted_by": "user_id"
    }
    ```
- **204 No Content** (DELETE):
  - **Description**: The book recommendation was successfully deleted.

### `POST /interactions/`

#### Description:

This endpoint allows users to submit their interactions with a book recommendation, such as liking a book or leaving a comment.

#### Request Body:

- **book_id** (UUID, required): The UUID of the book being interacted with.
- **liked** (boolean, optional): Whether the user liked the book.
- **comment** (string, optional): A comment on the book.

#### Example Request:

```json
{
  "book_id": "123e4567-e89b-12d3-a456-426614174000",
  "liked": true,
  "comment": "Amazing book!"
}
```

#### Responses:

- **201 Created**:

  - **Description**: The interaction was successfully created.
  - **Body**:
    ```json
    {
      "id": "uuid",
      "book_id": "uuid",
      "liked": true,
      "comment": "Amazing book!",
      "user_id": "user_id"
    }
    ```

- **200 OK**:

  - **Description**: The interaction was updated (e.g., changing the like status or adding a comment).
  - **Body**:
    ```json
    {
      "id": "uuid",
      "book_id": "uuid",
      "liked": false,
      "comment": "Amazing book!",
      "user_id": "user_id"
    }
    ```

- **400 Bad Request**:
  - **Description**: The interaction could not be created or updated due to a missing or invalid `book_id`.
  - **Body**:
    ```json
    {
      "error": "book_id is required"
    }
    ```

### `GET /interactions/`

#### Description:

This endpoint allows users to retrieve their interactions with various book recommendations, such as likes and comments.

#### Responses:

- **200 OK**:
  - **Description**: A list of the user's interactions with book recommendations.
  - **Body**:
    ```json
    [
        {
            "book_id": "uuid",
            "liked": true,
            "comment": "Amazing book!"
        },
        ...
    ]
    ```
