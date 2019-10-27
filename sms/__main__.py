import redis
import time
from twilio.rest import Client
import sendService

import config
from redisQueue import RedisQueue


twilioClient = Client(config.TWILIO['account_sid'], config.TWILIO['auth_token'])

try:
    r = redis.StrictRedis(host=config.HOST, port=config.PORT)

    sendQueue = RedisQueue(r, config.SEND_LIST)
    recievedQueue = RedisQueue(r, config.RECIEVED_LIST)

    SendService = sendService.SendService(twilioClient, sendQueue)

    while True:
        recievedMessage = recievedQueue.pop()
        sendMessage = sendQueue.pop()
        #print(sendMessage)

        if recievedMessage:
            print("recieved:", recievedMessage)
            SendService.handleReply(recievedMessage)

        if sendMessage:
            print("sending", sendMessage)
            SendService.sendMessage(sendMessage)
        
        if not (sendMessage or recievedMessage):
            time.sleep(1)

except Exception as e:
    print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
    print(str(e))