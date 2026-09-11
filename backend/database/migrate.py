from __future__ import annotations

import logging
from pathlib import Path

import psycopg

from backend.config import get_settings
from backend.logging.config import configure_logging

logger = logging.getLogger(__name__)
MIGRATIONS_DIRECTORY = Path(__file__).with_name("migrations")


def migrate() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    with psycopg.connect(settings.database_url) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        applied = {
            row[0]
            for row in connection.execute(
                "SELECT version FROM schema_migrations"
            ).fetchall()
        }

        for migration_path in sorted(MIGRATIONS_DIRECTORY.glob("*.sql")):
            if migration_path.name in applied:
                continue
            logger.info("Applying migration %s", migration_path.name)
            connection.execute(migration_path.read_text(encoding="utf-8"))
            connection.execute(
                "INSERT INTO schema_migrations (version) VALUES (%s)",
                (migration_path.name,),
            )

    logger.info("Database migrations are current")


if __name__ == "__main__":
    migrate()
