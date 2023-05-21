import werobot
from werobot.replies import ArticlesReply,Article
import random
import re, json, time, datetime
import urllib.parse

import openai

conversation_list = []
openai.api_key = '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'

token = 'token'
APPID = 'wx453efae09548d3e2'
APPSECRET = 'f54462607da4ea5fe1fa8c09dbf6f5f7'

robot = werobot.WeRoBot(token=token)
robot.config['APP_ID']= APPID
robot.config['APP_SECRET'] = APPSECRET


def ask_1(conversation_list):
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=conversation_list)
        # response = openai.ChatCompletion.create(model='davinci',messages=conversation_list)
        answer = response.choices[0].message['content']
        conversation_list.append({"role":"assistant","content":answer})
        if '【over】' not in answer:
            conversation_list.append({"role":'user', 'content':'继续'})
            answer += ask_1(conversation_list=conversation_list)
        print(answer)
        return answer
    except Exception as err:
        return err

@robot.text
def text_reply(message):
    # conversation_list.append({"role":'system', 'content':'在你每次开始回答时，开头加上"【start】"'})
    prompt = message.content
    # print(message.)
    if prompt[:2]=='//':
        prompt = prompt[2:]
        print(prompt)
        conversation_list = []
        conversation_list.append({"role":'system', 'content':'在你每次回答结束时，末尾加上"【over】"'})
        conversation_list.append({"role":'user', 'content':prompt})
        try:
            answer = ask_1(conversation_list)
            return answer
        except:
            return "false"
    else:
        return f"无指令：{prompt}"

@robot.subscribe
def sub_reply(message):
    return """
    欢迎来到小俊的秘密基地
    发送消息时，前面加上双斜杠 // 可以调用ai进行回复
    """

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = '80'
robot.run()
