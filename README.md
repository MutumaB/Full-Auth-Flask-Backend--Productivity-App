# Secure Productivity API (Flask Backend Asset)

A modular, production-hardened RESTful Flask API designed to support secure authentication flows, strict tenant boundaries, pagination, and multi-platform database handling.

## 🛠️ Installation & Direct Configuration

1. **Environment Setup:**
   ```bash
   pipenv install
   pipenv shell
   ```

2. **Initialize and Seed Database:**
   ```bash
   python seed.py
   ```

3. **Launch Local Server:**
   ```bash
   python app.py
   ```
   API routes are available at `http://127.0.0`.

## 📑 Core API Contract Routes

All incoming bodies must use `Content-Type: application/json`. Protected actions require authorization structures passed via a `Bearer <token>` inside the `Authorization` header.

*   `POST /signup` — Register a distinct account.
*   `POST /login` — Receive security validation tokens.
*   `GET /check_session` — Verify existing credentials.
*   `GET /tasks?page=1&per_page=10` — View paginated index list belonging exclusively to the authenticated user.
*   `POST /tasks` — Register a child resource object.
*   `GET /tasks/<id>` — View isolated row details.
*   `PATCH /tasks/<id>` — Modify entry state properties.
*   `DELETE /tasks/<id>` — Remove contextual object.

## 🚀 Cloud Deployment Options

### Render (Easiest)
1. Link this repository to a new **Web Service** on Render.
2. Select **Python** as the Runtime environment.
3. Set **Build Command** to `./build.sh` and ensure the script is executable (`chmod +x build.sh`).
4. Set **Start Command** to `pipenv run gunicorn wsgi:app`.
5. Set `JWT_SECRET_KEY` and your production `DATABASE_URL` in the environment variables configuration tab.

### VPS Server (Ubuntu / Nginx)
1. Clone the directory inside your server layer and execute `./build.sh`.
2. Configure Gunicorn to run a system daemon socket configuration.
3. Adjust Nginx configurations to reverse proxy external requests straight into your internal WSGI application layer socket.
