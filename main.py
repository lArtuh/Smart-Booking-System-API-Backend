from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_router import user_router
from app.routers.properties_router import property_router
from app.routers.bookings_router import booking_router
from app.routers.payments_router import payment_router
from app.routers.reviews_routers import review_router
from app.core.mongo import init_mongo
from app.core.init_db import init_db

app = FastAPI(title="Smart Booking System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(user_router)
app.include_router(booking_router)
app.include_router(property_router)
app.include_router(payment_router)
app.include_router(review_router)


@app.on_event("startup")
async def on_startup():
    await init_db()
    await init_mongo()


@app.get("/")
def root():
    return {"message": "Welcome to Smart Booking System API!"}
