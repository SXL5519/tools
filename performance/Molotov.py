from molotov import scenario


API_1 = 'https://activity.godteam.net/redPond/redPondRollData'
API_2='https://activity.godteam.net/redPond/redPondGoods'
payload={'page': 1,'rows': 10}
API_3='https://activity.godteam.net/redPond/redPondData'
API_4='https://activity.godteam.net/redPond/redPondSupport'
API_5='https://activity.godteam.net/redPond/redPondMusic'


a='http://192.168.1.118:8070/merchant/merReward/saveMerchantRewardApply'
aa={'goodsJson':[{'id':'5d9d3c420b06ca7b955a0f66','num':1},{'id':'5d922ebe8dfe9f4f0d5070ae','num':3}]}


@scenario(weight=1)
async def scenario_one(session):
    async with session.post(API_2,json=payload) as resp:
        res = await resp.json()
        print(res)
        assert res['success'] == True
        assert resp.status == 200


@scenario(weight=1)
async def scenario_two(session):
    async with session.get(API_1) as resp:
        r=await resp.json()##读取接口返回值
        print(resp.status)
        assert resp.status == 200

@scenario(weight=1)
async def scenario_two(session):
    async with session.get(API_3) as resp:
        r=await resp.json()##读取接口返回值
        print(resp.status)
        assert resp.status == 200

@scenario(weight=1)
async def scenario_two(session):
    async with session.get(API_4) as resp:
        r=await resp.json()##读取接口返回值
        print(resp.status)
        assert resp.status == 200

@scenario(weight=1)
async def scenario_two(session):
    async with session.get(API_5) as resp:
        r=await resp.json()##读取接口返回值
        print(resp.status)
        assert resp.status == 200