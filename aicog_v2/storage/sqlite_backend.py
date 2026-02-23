import sqlite3
import json
import time
import aiofiles
import aiosqlite
from typing import Dict
from aicog_v2.core.interfaces import AIStorage

class SQLiteStorage(AIStorage):
    def __init__(self, db_path: str = "aicog_monitoring.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    provider TEXT,
                    model TEXT,
                    prompt TEXT,
                    response TEXT,
                    latency REAL,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    total_tokens INTEGER
                )
            """)
            await db.commit()

    async def log_request(
        self, 
        provider: str, 
        model: str, 
        prompt: str, 
        response: str, 
        latency: float, 
        usage: Dict[str, int]
    ):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO requests 
                (timestamp, provider, model, prompt, response, latency, input_tokens, output_tokens, total_tokens)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    time.time(),
                    provider,
                    model,
                    prompt,
                    response,
                    latency,
                    usage.get("input_tokens", 0),
                    usage.get("output_tokens", 0),
                    usage.get("total_tokens", 0)
                )
            )
            await db.commit()
