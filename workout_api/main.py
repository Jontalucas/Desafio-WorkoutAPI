from typing import Annotated
from fastapi import Depends, FastAPI
from workout_api.routers import api_router
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage
from workout_api.atletas.models import AtletasModel
from workout_api.contrib.repository.dependencies import DataBaseDependency
from sqlalchemy import select
from sqlalchemy.sql import Executable

app = FastAPI(title="WorkouAPI")
app.include_router(api_router)
