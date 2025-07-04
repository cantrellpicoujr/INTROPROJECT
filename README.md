# INTROPROJECT

This project is a full-stack web app with a FastAPI backend and a React frontend. It allows users to view and add cat facts, which are stored in a SQLite database.

---

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm** (or **yarn**)
- **Git** (for version control)

---

## Backend Setup (FastAPI)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cantrellpicoujr/INTROPROJECT.git
   cd INTROPROJECT
   ```

2. **Create a Python virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running with Docker

You can use Docker to run both the backend and frontend in containers.

1. **Build the Docker images:**

   ```bash
   docker-compose build
   ```

2. **Start the containers:**

   ```bash
   docker-compose up
   ```

   - The FastAPI backend will be available at `http://localhost:8000`
   - The React frontend will be available at `http://localhost:5173`

3. **Stop the containers:**
   ```bash
   docker-compose down
   ```

> **Note:** Make sure you have a valid `docker-compose.yml` file in your project root that defines both services.

## Prerequisites for Docker

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your machine

---

## Frontend Setup (React + Vite)

1. **Install frontend dependencies:**

   ```bash
   npm install
   # or
   yarn install
   ```

---

## Development Notes

- **CORS** is enabled in the backend to allow frontend-backend communication during development.
- **API Endpoints:**
  - `GET /catfacts` — List all cat facts
  - `GET /catfacts/random` — Get a random cat fact
  - `POST /catfacts` — Add a new cat fact (form field: `fact`)

---

## Common Commands

- **Activate virtual environment:**  
  `source venv/bin/activate`
- **Deactivate virtual environment:**  
  `deactivate`
- **Install new Python package:**  
  `pip install <package> && pip freeze > requirements.txt`
- **Install new frontend package:**  
  `npm install <package>`

---

## Troubleshooting

- If you see errors about missing dependencies, ensure you have activated your Python virtual environment and installed all requirements.
- If you have issues with large files or Git, check your `.gitignore` and remove large files from Git history if needed.

---

## Contributing

1. Fork the dev repo and create your branch:  
   `git checkout -b feature/your-feature`
2. Commit your changes:  
   `git commit -m "Add your feature"`
3. Push to the branch:  
   `git push origin feature/your-feature`
4. Open a pull request.
