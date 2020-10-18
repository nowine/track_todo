from typing import List, Dict, Any

from fastapi import Depends, FastAPI, HTTPException, logger
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .api.v1.api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/v1")