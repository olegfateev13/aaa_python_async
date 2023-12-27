import asyncio

result = []

async def task_1(i: int):
    result.append(1)
    if i == 0:
        return
    
    if i > 5:
        await task_2(i // 2)
    else:
        await task_2(i - 1)

async def task_2(i: int):
    result.append(2)
    if i == 0:
        return
    
    if i % 2 == 0:
        await task_1(i // 2)
    else:
        await task_2(i - 1)

async def coroutines_execution_order(i: int = 42) -> int:
    # Отследите порядок исполнения корутин при i = 42 и верните число, соответствующее ему.
    #
    # Когда поток управления входит в task_1 добавьте к результату цифру 1, а когда он входит в task_2,
    # добавьте цифру 2.
    #
    # Пример:
    # i = 7
    # return 12212
    global result
    result = []
    await task_1(i)
    return int(''.join(map(str, result)))


if __name__ == "__main__":
    import asyncio
    print(asyncio.run(coroutines_execution_order(7)))

