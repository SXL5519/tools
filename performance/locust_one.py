from locust import HttpLocust, TaskSet, task

# 定义用户行为
class UserBehavior(TaskSet):

    # @task(1)
    # def test(self):
    #     self.client.get("/")

    @task(5)
    def test(self):
        self.client.post("/ajgsapp/merchant/getMerchant",{'merchantId': '5d921eee4aa4239f262ebe5e','isNew': 'true'})

    @task()
    def test(self):
        self.client.post("/ajgsapp/index/getMayYouLike", {'page': 1,'size': 8})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000