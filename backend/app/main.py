from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files (landing page)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
