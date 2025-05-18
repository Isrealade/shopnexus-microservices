# 📖 Frontend API Usage

The frontend (Next.js) does not expose its own REST API, but acts as a client to the backend services.

## How the Frontend Communicates

- **User Service API:** `http://localhost:5001/api/users`
- **Product Service API:** `http://localhost:5002/api/products`

### Example Usage

```js
// Fetch user profile from User Service
const res = await fetch('http://localhost:5001/api/users/profile', {
  credentials: 'include',
  headers: { Authorization: `Bearer <token>` }
});
const profile = await res.json();
```

### API Integration Points

- All authentication, user, and product actions are proxied to the backend services.
- See `/pages/` for examples of API usage in React components and API routes.

---