import asyncio
from random import randint


async def my_coroutine(i):
    await asyncio.sleep(randint(0, 3))  # Simulate varying task durations
    return i


async def stream():
    tasks = [my_coroutine(i) for i in range(10)]

    for completed_task in asyncio.as_completed(tasks):
        result = await completed_task
        yield f"Task completed with result: {result}"


async def main():
    async for v in stream():
        print(v)


if __name__ == "__main__":
    asyncio.run(main())
