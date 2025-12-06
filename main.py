from fastapi import FastAPI
from app.routers import (
    user_router,
    bookings_router,
    properties_router,
    payments_router
)


app = FastAPI(title="Smart Booking System")


app.include_router(user_router)
app.include_router(bookings_router)
app.include_router(properties_router)
app.include_router(payments_router)


@app.get("/")
def root():
    return {"message": "Welcome to Smart Booking System API!"}
