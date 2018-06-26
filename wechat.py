import itchat
from itchat.content import TEXT
from itchat import send
import json

servername = '@7f362f1fda17f0b73c062594c7669668af1496745029671d664bea03cf6d3546'


@itchat.msg_register(TEXT)
def text_reply(msg):
    print(msg['FromUserName'])
    print(msg['ToUserName'])
    try:
        if msg['FromUserName'] == servername:
            print("sever")
            send(json.dumps({'a':2}), servername)
        if u'用户' in msg['Text'] or u'密码' in msg['Text']:
            message = msg['Text'].split()
            # message format:'wechat account + username + password'
            MessageToServer = {
                'MessageType': 1,  # Authetication
                'FromUserName': msg['FromUserName'],
                'User': message[1],
                'Password': message[3]
            }
            send(json.dumps(MessageToServer), servername)
        elif u'任务' in msg['Text'] or u'日程' in msg['Text']:
            MessageToServer = {
                'MessageType': 2,  # Requirement of Schedule list to Server
                'FromUserName': msg['FromUserName']
            }
            send(json.dumps(MessageToServer), servername)

        elif msg['FromUserName'] == servername:
            message = json.loads(msg['Text'])

            if message['MessageType'] == 1:
                # the result of authetication
                # format: {'MessageType' : 1, 'ToUserName' : ToUserName, 'AutheticationResult' : Ture or False}
                if message['AuthenticationResult'] == True:
                    send('绑定成功', message['ToUserName'])
                else:
                    send('绑定失败，用户名或密码错误', message['ToUserName'])
            elif message['MessageType'] == 2:
                # General message to client or Required Schedulelist
                # format: {'MessageType' : 2, 'ToUserName' : ToUserName, 'Message' : Message}
                send(message['Message'], message['ToUserName'])

        else:
            # UserGuide
            send('若要绑定用户，请以 用户+空格+你的用户名+空格+密码+空格+你的密码 的形式回复，例如:"用户 user 密码 123456"', msg['FromUserName'])
    except:
        print("Exception happen")
        pass

itchat.auto_login(hotReload=True)
a=itchat.get_friends()
itchat.run()

b=a