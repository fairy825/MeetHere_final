# locust -f locustMixTest.py 
from locust import HttpLocust, TaskSet, task
import Queue

class UserBehavior(TaskSet):
    def on_start(self):
        pass

    def userRegister(self):
        try:
            user_name = self.locust.user_name_queue.get()  
        except Queue.Empty:
            exit()

        body = {"anonymousName": "",
                "email": "example@example.com",
                "faceImage": "",
                "id": 0,
                "name": user_name,
                "nickname": user_name,
                "password": "12345",
                "phoneNumber": "88888888",
                "userToken": ""
                }
        header = {"Content-Type": "application/json"}     
        self.client.post("/regist", json=body,headers=header, verify = False)

    def userLogin(self):
        body = {"anonymousName": "string",
                "email": "string",
                "faceImage": "string",
                "id": 0,
                "name": "string",
                "nickname": "string",
                "password": "string",
                "phoneNumber": "string",
                "userToken": "string"
                }
        header = {"Content-Type": "application/json"}     
        self.client.post("/login", json=body,headers=header, verify = False)

    def forevenues(self):
        self.client.get("/forevenues")

    def home(self):
        self.client.get("/home")

    def forenews(self):
        self.client.get("/forenews")  

    def new(self):
        self.userLogin()        
        self.client.get("/bought")

    def adminLogin(self):
        body = {
                "adminToken": "",
                "id": 0,
                "name": "example",
                "password": "example"
                }
        header = {"Content-Type": "application/json"}     
        self.client.post("/loginAdmin", json=body,headers=header, verify = False)

    def districts(self):
        try:
            district_name = self.locust.district_name_queue.get()  
        except Queue.Empty:
            exit()
        body={
              "id": 0,
              "name": district_name,
              "venues": [
                            {
                                "district": {},
                                "endTime": 0,
                                "firstVenueImage": {
                                "id": 0
                            },
                            "id": 0,
                            "introduction": "test",
                            "location": "",
                            "name": "test",
                            "phoneNumber": "",
                            "price": 10,
                            "reviewCount": 0,
                            "saleCount": 0,
                            "startTime": 0,
                            "totalSeat": 10,
                            "venueImages": [{
                                "id": 0
                            }]
                            }
                        ]
            }
        header = {"Content-Type": "application/json"}     
        self.client.post("/districts", json=body,headers=header, verify = False)

    def venue(self):
        body={
              "district": {
                "id": 23,
                "name": "string",
                "venues": [
                  {}
                ]
              },
              "endTime": 0,
              "firstVenueImage": {
                "id": 0
              },
              "id": 0,
              "introduction": "string",
              "location": "string",
              "name": "string",
              "phoneNumber": "string",
              "price": 0,
              "reviewCount": 0,
              "saleCount": 0,
              "startTime": 0,
              "totalSeat": 0,
              "venueImages": [
                {
                  "id": 0
                }
              ]
            }
        header = {"Content-Type": "application/json"}     
        self.client.post("/venues", json=body,headers=header, verify = False)

    def users(self):
        self.client.get("/users")

    def newsAdd(self):
        body = {
                "content": "test",
                "createDate": "2019-12-23 23:11",
                "id": 0,
                "timeDesc": "test",
                "title": "test"
                }
        header = {"Content-Type": "application/json"}     
        self.client.post("/news", json=body,headers=header, verify = False)

    def booking(self):
        self.client.get("/bookings")

    @task(1)
    def mix1(self):
        self.userLogin()
        self.userRegister()
        self.userLogin()

    @task(1)
    def mix2(self):
        self.userLogin()
        self.forevenues()
        self.home()

    @task(1)
    def mix3(self):
        self.userLogin()
        self.booking()
        self.forevenues()

    @task(1)
    def mix4(self):
        self.userLogin()
        self.home()
        self.new()

    @task(1)
    def mix5(self):
        self.adminLogin()
        self.districts()
        self.venue()

    @task(1)
    def mix6(self):
        self.userLogin()
        self.users()

    @task(1)
    def mix7(self):
        self.userLogin()
        self.new()
        self.newsAdd()
       
    

class WebsiteUser(HttpLocust):
    host = 'http://localhost:8080/meethere'
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000
    user_name_queue = Queue.Queue()  
    district_name_queue = Queue.Queue()  
    for i in range(1,10000):
        user_name = "register"+str(i)
        district_name = "distTestHigh"+str(i)
        user_name_queue.put_nowait(user_name) 
        district_name_queue.put_nowait(district_name) 
