from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Serve static files (landing page)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
