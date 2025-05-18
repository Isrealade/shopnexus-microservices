# 📖 User Service API

Base URL: `http://localhost:5001/api/users`

## Endpoints

| Method | Endpoint      | Description                | Auth Required | Request Body / Params           | Response Example                |
|--------|--------------|----------------------------|---------------|---------------------------------|---------------------------------|
| POST   | `/register`  | Register a new user        | No            | `{ username, email, password }` | `{ "message": "User created" }` |
| POST   | `/login`     | Authenticate user          | No            | `{ email, password }`           | `{ "token": "..." }`            |
| GET    | `/profile`   | Get current user profile   | Yes           | -                               | `{ "id": 1, "email": "...", ...}`|
| PUT    | `/profile`   | Update user profile        | Yes           | `{ email?, password? }`         | `{ "message": "Updated" }`      |
| GET    | `/`          | List all users (admin)     | Yes           | -                               | `[ { "id": 1, ... }, ... ]`     |

## Authentication

- Most endpoints require a JWT token in the `Authorization: Bearer <token>` header.

## Example Request

```bash
curl -H "Authorization: Bearer <token>" http://localhost:5001/api/users/profile
```

---