import json

class RedisQueue():

    def __init__(self, redisClient, q_name):
        self.redis = redisClient
        self.name = q_name

    def push(self, data):
        self.redis.rpush(self.name, data)
    
    def pushJSON(self, data):
        self.push(json.dump(data))

    def pop(self):
        val = self.redis.lpop(self.name)
        if not val:
            return
        return json.loads(val.decode("utf-8"))
