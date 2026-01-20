from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_router import user_router
from app.routers.properties_router import property_router
from app.routers.bookings_router import booking_router
from app.routers.payments_router import payment_router

app = FastAPI(title="Smart Booking System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(booking_router)
app.include_router(property_router)
app.include_router(payment_router)


@app.get("/")
def root():
    return {"message": "Welcome to Smart Booking System API!"}
