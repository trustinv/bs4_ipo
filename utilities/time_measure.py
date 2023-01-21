import time


def timeit(func):
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Time taken: {end_time - start_time} seconds")
        return result

    return wrapper
