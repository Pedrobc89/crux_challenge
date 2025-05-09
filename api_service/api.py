"""
API endpoints
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from random import randint, sample, choice
import csv
import math
import asyncio

app = FastAPI(debug=True)

CSV_LINES = 10000
CSV_FILE_PATH = "./TabularData.csv"
SAMPLE_SIZE = 250
MAX_LATENCY = 30


@app.get("/random-int")
async def get_random_integer():
    await latency()
    return randint(0, CSV_LINES)


@app.get("/table")
async def get_tabular_data():
    await latency()
    try:
        return JSONResponse(content=sample_csv_rows())
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/time-series")
async def get_time_series():
    """ """
    await latency()
    f = choice(
        [
            generate_time_series_x,
            generate_time_series_y,
            generate_time_series_z,
        ]
    )
    return f()


async def latency() -> None:
    """
    Randomly simulates latency between 0 and 30 seconds.
    """
    await asyncio.sleep(randint(0, MAX_LATENCY))


def sample_csv_rows(
    filepath: str = CSV_FILE_PATH, sample_size: int = SAMPLE_SIZE
) -> list[dict[str, str]]:
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = list(csv.DictReader(csvfile))

        if sample_size > len(reader):
            raise ValueError("Sample size exceeds number of rows in the CSV.")

        sampled_rows = sample(reader, sample_size)
        return sampled_rows


def generate_time_series_x(
    step: float = 0.1, duration: float = 300.0
) -> list[dict[str, float]]:
    """
    Generates time series data using the function X(t) = 2 * sin(pi * t / 30)

    Args:
        step (float): Time interval between samples in seconds.
        duration (float): Total duration of the time series in seconds.

    Returns:
        List[Tuple[float, float]]: List of (t, X(t)) tuples.
    """
    num_points = int(duration / step)
    data = []

    for i in range(num_points + 1):
        t = round(i * step, 3)  # rounding for clean float values
        x = 2 * math.sin(math.pi * t / 30)
        data.append({"t": t, "value": x})

    return data


def generate_time_series_y(
    step: float = 0.1, duration: float = 300.0
) -> list[tuple[float, float]]:
    """
    Generates time series data using the function Y(t) = 5 * (1 - exp(-t / 60))

    Args:
        step (float): Time interval between samples in seconds.
        duration (float): Total duration of the time series in seconds.

    Returns:
        List[Tuple[float, float]]: List of (t, Y(t)) tuples.
    """
    num_points = int(duration / step)
    data = []

    for i in range(num_points + 1):
        t = round(i * step, 3)
        y = 5 * (1 - math.exp(-t / 60))
        data.append({"t": t, "value": y})

    return data


def generate_time_series_z(
    step: float = 0.1, duration: float = 300.0
) -> list[tuple[float, float]]:
    """
    Generates time series data using the function Z(t) = X(t) * Y(t),
    where:
      X(t) = 2 * sin(pi * t / 30)
      Y(t) = 5 * (1 - exp(-t / 60))

    Args:
        step (float): Time interval between samples in seconds.
        duration (float): Total duration of the time series in seconds.

    Returns:
        List[Tuple[float, float]]: List of (t, Z(t)) tuples.
    """
    x_series = generate_time_series_x(step, duration)
    y_series = generate_time_series_y(step, duration)

    data = []
    for x, y in zip(x_series, y_series):
        assert x["t"] == y["t"], "Timestamps do not match!"
        z = x["value"] * y["value"]
        data.append({"t": x["t"], "value": z})

    return data
