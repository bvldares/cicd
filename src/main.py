from fastapi import FastAPI
from .api.todos import router as todos_router
from .db.database import create_tables

# Inizializza il database
create_tables()

app = FastAPI(
    title="Todo API",
    description="Una semplice API per gestire todo items",
    version="1.0.0"
)

# Include le route
app.include_router(todos_router)

@app.get("/")
def root():
    return {"message": "Todo API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
