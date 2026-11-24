import asyncio

async def task_one():
    print("Task one started!")
    await asyncio.sleep(2)
    print("Task one completed")

async def task_two():
    print("Task two started")
    await asyncio.sleep(2)
    print("Task two completed")

async def main(): 
    await asyncio.gather(task_one(), task_two())

asyncio.run(main())