BMI Fit

BMI Fit is a Single Page Application (SPA) developed with Python. The system aims to support low-income individuals in calculating their Body Mass Index (BMI) and generating personalized training and diet plans to promote health and well-being.
👨‍💻 Project Participants

    Enzo Nascimento Cabrera - @EnzoCabrera
    Geziel Oliveira Silva - @ImG1029
    Tannus Koussa Neto - @tannuskoussa
    William Menezes Damascena - @william-menezes

🚀 Technologies Used

    Python 3.11
    FastAPI 0.115.12
    OpenAI API (GPT-3.5 Turbo)
    PostgreSQL 15.8
    Docker

🗂️ Project Structure

The project follows the FastAPI architecture pattern and includes the following main modules:

    api/ – Contains the application's routes, organized by feature (e.g., users, BMI, diets). Also includes API configurations and authentication.
    db/ – Responsible for database definitions: ORM models (SQLAlchemy) and database session setup.
    services/ – Holds the business logic, separating it from the route layer. Each file handles a specific feature (e.g., BMI, diets, training).
    utils/ – Stores helper functions and reusable configurations, such as OpenAI prompts or common utilities.

✅ Features
👤 Users

    Sign up – Register new users.
    Login – User authentication.

📏 BMI

    Physical assessment – Form to collect data and calculate BMI.
    Dashboard – Displays the submitted information.

🏋️‍♂️ Training Plans

    Training creation – Available after completing a physical assessment.
    Training update – Allows users to modify existing plans.

🥗 Diet Plans

    Diet creation – Takes dietary restrictions into account.
    Diet update – Allows users to edit or replace existing meal plans.


🚀 Running the Project Locally with Docker

This project was developed using FastAPI, PostgreSQL, and Docker. To run it locally, follow the steps below:
📦 Prerequisites

    Docker and Docker Compose installed

    Ports 8000 and 5432 must be available on your machine

🔧 Database Configuration

ℹ️ The project originally uses Supabase as the database, but that instance is not active in this public repository.
You can either run a local PostgreSQL instance using Docker or connect to your own PostgreSQL database.
🔧 Running PostgreSQL Locally with Docker

You can start a PostgreSQL container with the following command:

-docker run --name postgres-bmi-fit -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=bmifit -p 5432:5432 -d postgres:15

Set your environment variable in the backend with the following DATABASE_URL (example only):

postgresql://postgres:postgres@localhost:5432/bmifit

🗄️ Redis Database

Start a Redis instance locally with:

docker run --name redis-bmi-fit -p 6379:6379 -d redis:alpine

▶️ Running the Backend

    Clone the repository

git clone https://github.com/EnzoCabrera/bmi-calculator-backend.git
cd bmi-calculator-backend

    Set environment variables

Create a .env file inside the backend/ directory with the following content:

user=your_db_user
password=your_db_password
host=your_db_host
port=your_db_port
dbname=your_db_name

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bmifit  # Example only

REDIS_HOST=your_redis_host
REDIS_PASSWORD=your_redis_password
REDIS_PORT=your_redis_port

SECRET_KEY=your_secret_key
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1000

OPENAI_API_KEY=your_openai_key

    Start the backend using Docker Compose

docker compose up --build

The backend will be available at:

http://localhost:8000

The interactive API documentation is available at:

http://localhost:8000/docs

🧬 Running Migrations with Alembic

If you're using a fresh database, run the migrations with Alembic (either inside the container or in your Python environment):

alembic upgrade head


