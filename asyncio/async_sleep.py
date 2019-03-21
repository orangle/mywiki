import asyncio  
import time  
from datetime import datetime

async def custom_sleep():  
    print('SLEEP START', datetime.now())
    # time.sleep(1)
    await asyncio.sleep(1)
    print('SLEEP END', datetime.now())

def fib(n):
    if 2 > n:
        return n
    return fib(n-2) + fib(n-1)

async def factorial(name, number):  
    f = 1
    for i in range(2, number+1):
        print('Task {}: Compute factorial({})'.format(name, i), datetime.now())
        await custom_sleep() # 单个任务无法切走时间？切换是多个流程之间切换
        f *= i
        fib(35)
    
    print('Task {}: factorial({}) is {}\n'.format(name, number, f), datetime.now())

start = time.time()  
loop = asyncio.get_event_loop()
tasks = [  
    asyncio.ensure_future(factorial("A", 3)),
    # asyncio.ensure_future(factorial("B", 4)),
]
loop.run_until_complete(asyncio.wait(tasks))  
loop.close()
end = time.time()  
print("Total time: {}".format(end - start))