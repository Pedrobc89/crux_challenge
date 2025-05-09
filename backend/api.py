import asyncio
from random import randint
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator, Dict, Any
import httpx

app = FastAPI()

API_SERVICE_BASE_URL = "http://api_service"  # Docker hostname or service name


async def fetch_from_api(path: str) -> Dict[str, Any]:
    url = f"{API_SERVICE_BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=35.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return {"path": path, "data": response.json()}


async def event_stream() -> AsyncGenerator[str, None]:
    tasks = {
        "number": asyncio.create_task(fetch_from_api("/random-int")),
        "table": asyncio.create_task(fetch_from_api("/table")),
        "time_series": asyncio.create_task(fetch_from_api("/time-series")),
    }

    for task in asyncio.as_completed(tasks.values()):
        try:
            result = await task
            yield json.dumps(result) + "\n"
        except Exception as e:
            print(e)
            yield json.dumps({"error": str(e)}) + "\n"


@app.get("/aggregate-data")
async def aggregate_data() -> StreamingResponse:
    return StreamingResponse(event_stream(), media_type="application/json")
