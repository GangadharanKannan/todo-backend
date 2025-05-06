# FastAPI Todo Backend

## Setup (Local)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```
JWT_SECRET=your_secret_key_here
```

4. Run the app:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /signup` - Register new user
- `POST /signin` - Login and receive JWT
- `GET /tasks` - List tasks (auth required)
- `POST /tasks` - Add task (auth required)
- `DELETE /tasks/{id}` - Delete task (auth required)