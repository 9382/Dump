import asyncio

async def test2(a):
	print("T2",a)
	await asyncio.sleep(1)
	print("Done!")
	return a

async def test(a):
	print("Async run",a)
	return await test2(a)

final = asyncio.run(test(5))
print("Final=",final)
