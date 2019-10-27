import redis
import config
import messages
import json

#TODO: make LQ Cache its own service

class SendService():

    def __init__(self, twilio, send):
        self.twilio = twilio
        self.redisClient = redis.StrictRedis(host=config.HOST, port=config.PORT)
        self.sendQueue = send

    def updateLQCache(self, number, message_id):
        return self.redisClient.hset('LQ', number, message_id)

    def readLQCache(self, number):
        message = self.redisClient.hget('LQ', number)
        if message:
            return message.decode("utf-8")

    def clearLQCache(self, number):
        return self.redisClient.hdel('LQ', number)

    def doesMessageExpectReply(self, message_id):
        return 'expectsReply' in messages.MASTER_LIST[message_id]

    def sendSMS(self, message):
        try:
            if 'message_id' in message:
                # print("sending ", messages.MASTER_LIST[message['message_id']]['body'], "to", message['number'])
                self.twilio.messages.create(
                    body=messages.MASTER_LIST[message['message_id']]['body'],
                    from_= config.TWILIO['from_'],
                    to = message['number']
                )
            elif 'message' in message:
                #print("sending ", message['message'], "to", message['number'])
                self.twilio.messages.create(
                    body=message['message'],
                    from_= config.TWILIO['from_'],
                    to = message['number']
                )
        except Exception as e:
            print(e)

    def sendMessage(self, message):
        self.sendSMS(message)
        if 'message_id' in message:
            if self.doesMessageExpectReply(message['message_id']):
                self.updateLQCache(message['number'], message['message_id'])

    def getExpectedReply(self, message_id):
        return messages.MASTER_LIST[message_id]['expectsReply']

    def publishResults(self, message, publishResultSchema):
        if not publishResultSchema:
            return

        if publishResultSchema['data'] == "number" and message['number']:
            return self.redisClient.rpush(publishResultSchema['channel'], json.dumps({
                'number': message['number']
            }))
        elif publishResultSchema['data'] == "body" and message['body']:
            return self.redisClient.rpush(publishResultSchema['channel'], json.dumps({
                'body': message['body']
            }))

    def handleReply(self, message):
        lastMessage = self.readLQCache(message['number'])
        if lastMessage:
            replySchema = self.getExpectedReply(lastMessage)
            if replySchema:
                matchedReply = False
                for option in replySchema['options']:                                        
                    if message['body'] in option['responses']:
                        matchedReply = True               
                        self.clearLQCache(message['number'])         
                        if 'publishResult' in option:
                            self.publishResults(message, option['publishResult'])
                        if 'reply' in option:
                            new_message = {
                                "number": message['number'],
                                "message_id": option['reply']
                            }
                            self.sendMessage(new_message)
                        return

                if not matchedReply and 'default' in replySchema:
                    new_message = {
                        "number": message['number'],
                        "message_id": replySchema['default']
                    }
                    self.sendMessage(new_message)
                    return
        else:
            new_message = {
                "number": message['number'],
                "message_id": "default"
            }
            self.sendSMS(new_message)
