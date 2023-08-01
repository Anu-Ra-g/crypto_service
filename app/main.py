from fastapi import FastAPI
from . import database, models
from .routes import auth, usage
from .routes.callapi import update_cryptDetails
import multiprocessing

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(usage.router)

multiprocessing.Process(target=update_cryptDetails, daemon=True).start()