import asyncio
import functools


def async_retry(*args, **kwargs):
    retries = kwargs.pop('retries', 1)
    exceptions = kwargs.pop('exceptions', ())
    def deco(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt <= retries:
                        print(f'Retrying {func.__name__} ({attempt}/{retries})...')
                    continue
            raise last_exception
        return wrapper
    return deco



@async_retry(retries=5, exceptions=(ValueError,))
async def unstable_task():
    print("Running task...")
    raise ValueError("Something went wrong")

async def main():
    try:
        await unstable_task()
    except Exception as e:
        print(f"Final failure: {e}")



if __name__ == '__main__':
    asyncio.run(main())