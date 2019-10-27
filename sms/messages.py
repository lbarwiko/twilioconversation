# class Message():
#     body = ""
# class expectsReply():
# class responseList():

MASTER_LIST = {
    "default":{
        "body": "We weren't expecting a reply from you! Sign up on whatnow.co to join the community!"
    },
    "GreetPatient": {
        "body": "Thanks for signing up! Is it ok if we give someone your phone number? Reply Y/N",
        "expectsReply": {
            "options":[
                {
                    "responses": ['y', 'Y', 'YES', 'yes', 'Yes'],
                    "reply": "getPatientOK",
                    "publishResult":{
                        "channel": "confirmPatient",
                        "data": "number"
                    }
                },
                {
                    "responses": ['n', 'N', 'NO', 'no', 'No'],
                    "reply": "signUpLater"
                }
            ],
            "default": "tryAgainYesNo"
        } 
    },
    "GreetVolunteer": {
        "body": "We appreciate you! Do you understand your resposibilities and feel comfortable with this role? (You can review them at whatnow.co/greet-volunteer) Reply Y/N",
        "expectsReply": {
            "options":[
                {
                    "responses": ['y', 'Y', 'YES', 'yes', 'Yes'],
                    "reply": "confirmVolunteer",
                    "publishResult":{
                        "channel": "confirmVolunteer",
                        "data": "number"
                    }
                },
                {
                    "responses": ['n', 'N', 'NO', 'no', 'No'],
                    "reply": "askQuestions"
                }
            ],
            "default": "tryAgainYesNo"
        } 
    },
    "askQuestions": {
        "body": "Feel free to send an email to luke@whatnow.co with any questions you might have!"
    },
    "confirmVolunteer":{
        "body": "Great, you have been added to the match list. We'll get back to you when we have someone who wants to talk to you!"
    },
    "tryAgainYesNo":{
        "body": "Please reply with either a Y or N"
    },
    "getPatientOK": {
        "body": "Thanks for signing up! You've been added to a waiting list, and we're going to look for a match for you. As soon as we find someone who is available to talk, we will have them send you a text! The only information the volunteer will be given is your number, you may give them your name if YOU want to.",
    },
    "signUpLater":{
        "body": "That's alright! You can always sign up again later :)"
    },
    "thanksForMatching":{
        "body": "Thank you for offering your time. We are about to send you the contact information of someone looking to be supported through their injury."
    },
    "confirmPendingMatch":{
        "body": "Are you still available? We have someone who is looking for support and we wanted to know if you were willing to talk to them! Reply Y/N",
        "expectsReply": {
            "options":[
                {
                    "responses": ['y', 'Y', 'YES', 'yes', 'Yes'],
                    "reply": "thanksForMatching",
                    "publishResult":{
                        "channel": "createMatch",
                        "data": "number"
                    }
                },
                {
                    "responses": ['n', 'N', 'NO', 'no', 'No'],
                    "reply": "takeABreak"
                }
            ],
            "default": "tryAgainYesNo"
        } 
    },
    "takeABreak":{
        "body": "That's no problem! Is it alright if we check if you're availble again sometime later? Reply Y/N",
        "expectsReply": {
            "options":[
                {
                    "responses": ['y', 'Y', 'YES', 'yes', 'Yes'],
                    "reply": "addBackToVolunteerQueue",
                    "publishResult":{
                        "channel": "confirmVolunteer",
                        "data": "number"
                    }
                },
                {
                    "responses": ['n', 'N', 'NO', 'no', 'No'],
                    "reply": "removeVolunteer",
                    "publishResult":{
                        "channel": "removeVolunteer",
                        "data": "number"
                    }
                }
            ],
            "default": "tryAgainYesNo"
        } 
    },
    "addBackToVolunteerQueue":{
        "body": "Great! We really appreciate you!"
    },
    "removeVolunteer":{
        "body": "That's no problem! You can always sign up again sometime later."
    },
    "pendingMatchExpires":{
        "body": "We're going to find another person for this person waiting! Do you want to be considered to be matched with someone in the future again? Reply Y/N",
        "expectsReply": {
            "options":[
                {
                    "responses": ['y', 'Y', 'YES', 'yes', 'Yes'],
                    "reply": "addBackToVolunteerQueue",
                    "publishResult":{
                        "channel": "confirmVolunteer",
                        "data": "number"
                    }
                },
                {
                    "responses": ['n', 'N', 'NO', 'no', 'No'],
                    "reply": "removeVolunteer",
                    "publishResult":{
                        "channel": "removeVolunteer",
                        "data": "number"
                    }
                }
            ],
            "default": "tryAgainYesNo"
        } 
    }
}