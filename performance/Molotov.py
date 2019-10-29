from molotov import scenario


_API = 'https://activity.godteam.net/redPond/redPondRollData'
API='https://activity.godteam.net/redPond/redPondGoods'
payload={'page': 1,'rows': 10}

a='http://192.168.1.118:8070/merchant/merReward/saveMerchantRewardApply'
aa={'goodsJson':[{'id':'5d9d3c420b06ca7b955a0f66','num':1},{'id':'5d922ebe8dfe9f4f0d5070ae','num':3}]}


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
        print(resp.status)
        assert resp.status == 200