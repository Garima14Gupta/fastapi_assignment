from fastapi import FastAPI
from routers import items, clock_in

# FastAPI instance
app = FastAPI()

# Include API routers
app.include_router(items.router)
app.include_router(clock_in.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI CRUD Assignment!"}
