from molotov import scenario


_API = 'https://activity.godteam.net/redPond/redPondRollData'
API='https://activity.godteam.net/redPond/redPondGoods'
payload={'page': 1,'rows': 10}


@scenario(weight=40)
async def scenario_one(session):
    async with session.post(API,json=payload) as resp:
        res = await resp.json()
        print(res)
        assert res['success'] == True
        assert resp.status == 200


@scenario(weight=60)
async def scenario_two(session):
    async with session.get(_API) as resp:
        r=await resp.json()##读取接口返回值
        print(r)
        assert resp.status == 200