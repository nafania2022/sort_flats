import asyncio
import sys

SCRIPTS = [
    'runners/scheduler_runer_arhive.py',
    'runners/tasks_scheduler_runner.py',
    'runners/tg_posting_scheduler_runner.py'
    
]

async def waiter(sc, p):
    # "Функция которая вернет имя скрипта после ожидания"
    await p.wait()
    return sc, p


async def main():
    waiters  = []
    
    # Запуск
    for sc in SCRIPTS:
        p = await asyncio.create_subprocess_exec(sys.executable, sc)
        print('Started', sc)
        waiters.append(asyncio.create_task(waiter(sc, p)))

    # Ожидание
    while waiters:
        done, waiters = await asyncio.wait(waiters, return_when=asyncio.FIRST_COMPLETED)
        for w in done:
            sc,p = await w
            print('Done', sc)
        
      
if __name__ == "__main__":
    asyncio.run(main())
    