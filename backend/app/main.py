from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.config import FRONTEND_ORIGINS
from app.db import Base, engine, get_db
from app.routers.alerts import router as alerts_router
from app.routers.admin import router as admin_router
from app.routers.dashboard import router as dashboard_router
from app.routers.districts import router as districts_router
from app.routers.monitoring import router as monitoring_router
from app.services.pipeline_service import load_artifacts
from app.services.query_service import health_payload


def ensure_runtime_schema() -> None:
    inspector = inspect(engine)
    required_columns = {
        "predictions": {"predicted_date", "final_score", "confidence_score"},
        "alerts": {"predicted_date", "confidence_score", "owner_role"},
    }

    tables_to_reset: list[str] = []
    for table_name, expected_columns in required_columns.items():
        if not inspector.has_table(table_name):
            continue
        existing_columns = {
            column["name"] for column in inspector.get_columns(table_name)
        }
        if not expected_columns.issubset(existing_columns):
            tables_to_reset.append(table_name)

    if not tables_to_reset:
        return

    # Legacy SQLite files may still carry the older alert/prediction schema.
    for table_name in ["alerts", "predictions"]:
        if table_name in tables_to_reset:
            Base.metadata.tables[table_name].drop(bind=engine, checkfirst=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_runtime_schema()
    Base.metadata.create_all(bind=engine)
    load_artifacts()
    yield


app = FastAPI(
    title="AI-Based Early Warning System",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS if FRONTEND_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["health"])
def api_health(db: Session = Depends(get_db)):
    return health_payload(db)


@app.get("/", tags=["health"])
def root():
    return {
        "message": "AI-Based Early Warning System backend is running",
        "health": "/api/health",
    }


app.include_router(admin_router)
app.include_router(alerts_router)
app.include_router(dashboard_router)
app.include_router(districts_router)
app.include_router(monitoring_router)
