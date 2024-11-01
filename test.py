import asyncio

async def my_task():
    await asyncio.sleep(2)  # Simulate a task taking 2 seconds
    return "Task complete!"

async def main():
    task = asyncio.create_task(my_task())
    
    # Perform other operations here
    print("Doing other operations while task is running...")

    # Await the completion of the created task
    result = await task
    print(result)

# Run the event loop
asyncio.run(main())
