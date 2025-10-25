# Project Overview

This is a personal finance application named **finanpy**. It is built with Django and styled with Tailwind CSS. The project is structured into several Django apps: `accounts`, `categories`, `profiles`, `transactions`, and `users`.

## Main Technologies

*   **Backend:** Django
*   **Frontend:** Django Templates with Tailwind CSS
*   **Database:** SQLite (for development)

# Building and Running

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Install Tailwind CSS dependencies:**
    ```bash
    python manage.py tailwind install
    ```
3.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

## Running the application

1.  **Start the Tailwind CSS builder:**
    ```bash
    python manage.py tailwind start
    ```
2.  **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

# Development Conventions

*   The project follows a modular architecture with separate Django apps for each major feature.
*   It uses a custom user model for authentication, allowing users to log in with their email address.
*   Class-based views are used for handling requests.
*   The project uses `django-tailwind` for easy integration of Tailwind CSS.
*   Configuration is managed through environment variables using `python-decouple`.
*   The project has a detailed task list in `TASKS.md`, which outlines the development sprints and their respective tasks.
