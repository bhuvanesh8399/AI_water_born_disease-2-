import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.db import SessionLocal
from app.services.pipeline_service import run_full_pipeline


async def main():
    db = SessionLocal()
    try:
        result = await run_full_pipeline(db)
        print(result)
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
