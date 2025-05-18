# 📖 Product Service API

Base URL: `http://localhost:5002/api/products`

## Endpoints

| Method | Endpoint      | Description                    | Auth Required | Request Body / Params           | Response Example                |
|--------|--------------|--------------------------------|---------------|---------------------------------|---------------------------------|
| GET    | `/`          | List all products              | No            | -                               | `[ { "id": 1, "name": "...", ... }, ... ]` |
| GET    | `/:id`       | Get product by ID              | No            | -                               | `{ "id": 1, "name": "...", ... }` |
| POST   | `/`          | Create new product (admin)     | Yes           | `{ name, price, stock, ... }`   | `{ "id": 2, ... }`              |
| PUT    | `/:id`       | Update product (admin)         | Yes           | `{ name?, price?, stock? }`     | `{ "message": "Updated" }`      |
| DELETE | `/:id`       | Delete product (admin)         | Yes           | -                               | `{ "message": "Deleted" }`      |

## Authentication

- Admin endpoints require a JWT token in the `Authorization: Bearer <token>` header.

## Example Request

```bash
curl http://localhost:5002/api/products/
```

---