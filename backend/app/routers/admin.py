from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.pipeline_service import (
    generate_predictions,
    ingest_core_data,
    ingest_enrichment_data,
    ingest_weather,
    run_full_pipeline,
    train_models,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/ingest-core")
def api_ingest_core(db: Session = Depends(get_db)):
    return ingest_core_data(db)


@router.post("/ingest-enrichment")
def api_ingest_enrichment(db: Session = Depends(get_db)):
    return ingest_enrichment_data(db)


@router.post("/ingest-weather")
async def api_ingest_weather(db: Session = Depends(get_db)):
    return await ingest_weather(db)


@router.post("/train-models")
def api_train_models(db: Session = Depends(get_db)):
    try:
        return train_models(db)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/generate-predictions")
def api_generate_predictions(db: Session = Depends(get_db)):
    return generate_predictions(db)


@router.post("/run-full-pipeline")
async def api_run_full_pipeline(db: Session = Depends(get_db)):
    return await run_full_pipeline(db)
