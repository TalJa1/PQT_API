import os
from typing import Literal
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from database import (
    Base,
    engine,
)  # Removed SessionLocal as it's not directly used here for seeding
from routers import DisasterRoute  # Ensure DisasterRoute is imported
import logging
from contextlib import asynccontextmanager
from sqlalchemy import text  # For executing raw SQL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan event handler
@asynccontextmanager
async def lifespan(
    app_instance: FastAPI,
):  # Renamed 'app' to 'app_instance' to avoid conflict
    logger.info("Application startup: Initializing database...")
    async with engine.begin() as conn:
        # This ensures tables are created if they don't exist.
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured.")

    # Seed data if necessary
    async with engine.connect() as conn_seed:
        try:
            result = await conn_seed.execute(text("SELECT COUNT(id) FROM ThienTai"))
            count = result.scalar_one_or_none()
            if count is None:  # Should ideally not happen if create_all worked
                count = 0
        except Exception as e:
            logger.warning(
                f"Could not check ThienTai table count (error: {e}). Assuming empty for seeding."
            )
            count = 0  # Proceed to seed if table check fails

        if count == 0:
            logger.info("ThienTai table is empty. Seeding data from script.sql...")
            try:
                # Corrected path assuming script.sql is in the same directory as main.py
                # In Docker, WORKDIR is /app, and COPY . . puts files there.
                script_path = os.path.join(os.path.dirname(__file__), "script.sql")
                if not os.path.exists(
                    script_path
                ):  # Fallback for Docker if __file__ is tricky
                    script_path = "script.sql"

                with open(script_path, "r", encoding="utf-8") as f:
                    sql_script = f.read()

                raw_conn = await engine.raw_connection()
                try:
                    await raw_conn.executescript(sql_script)
                    await raw_conn.commit()
                    logger.info("Data seeding from script.sql successful.")
                except Exception as e_script:
                    logger.error(f"Error executing script.sql: {e_script}")
                    await raw_conn.rollback()
                finally:
                    await raw_conn.close()
            except FileNotFoundError:
                logger.error(
                    f"script.sql not found at {script_path}. Cannot seed data."
                )
            except Exception as e_seed:
                logger.error(f"An error occurred during data seeding process: {e_seed}")
        else:
            logger.info(
                f"ThienTai table contains {count} records. Skipping data seeding."
            )

    yield  # Application runs after this point

    logger.info("Application shutdown.")
    # Add any cleanup code here if needed


# Instantiate the FastAPI app ONCE with the lifespan manager
app = FastAPI(
    title="FastAPI with SQLite For PQT app",
    description="This is a very fancy project, with auto docs for the API",
    version="0.1.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Pydantic model for filter parameters (remains unchanged)
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


# Include routers
app.include_router(DisasterRoute.router, prefix="/api/v1", tags=["Disasters"])
