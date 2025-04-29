from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from routes.routes import App


app = FastAPI()

origins = [
    "https://rolsa-technologies-uk1j.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],

)

app.include_router(
    App,
    prefix="/Auth",
    tags=["auth"]
)
