#!/usr/bin/env python3
from types import coroutine


async def corout():
    print("running corout")
    return "something returned"

async def corout2():
    print("running corout2")
    await corout()

# cr = corout()
# cr.send(None)

cr2 = corout2()
cr2.send(None)


# @coroutine
# def do_nothing():
#     yield
#     return "something from do nothing"
#
# @coroutine
# def nothing():
#     yield "from nothing"
#     return "something from nothing"
#
# @coroutine
# def count(num):
#     for i in range(num):
#         yield f"count: {i}"
#
# async def do_a_few_things(num=3, name="No_name"):
#     for i in range(num):
#         print(f'\nin the loop "{name}" loop for the {i}th time')
#         from_await = await nothing()
#         print("value returned from await", from_await)
#     return "do a few things result"
#
# #create it
# daft = do_a_few_things(5, "first one")
#
# daft.send(None)
#
# i = 0
# while True:
#     i+=1
#     print(f"{i}th time in the outer while loop")
#     try:
#         res = daft.send(i)
#         print("result of send", res)
#     except StopIteration:
#         print("The awaitable is complete")
#         break

# while True:
#     try:
#         daft.send(None)
#     except StopIteration as si:
#         print("the awaitable is complete")
#         print('passed out', si)
#         break

#run it
# for i in range(5):
#     daft.send(None)