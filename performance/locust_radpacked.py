from locust import HttpLocust, TaskSet, task

# 定义用户行为
class UserBehavior(TaskSet):

    @task(1)
    def test_1(self):
        self.client.get("/redPond/redPondGoods")

    @task(1)
    def test_2(self):
        self.client.post("/redPond/redPondRollData",{'page': 1,'rows': 10})

    @task(1)
    def test_3(self):
        self.client.get("/redPond/redPondData")

    @task(1)
    def test_4(self):
        self.client.get("/redPond/redPondSupport")

    @task(1)
    def test_5(self):
        self.client.get("/redPond/redPondMusic")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000