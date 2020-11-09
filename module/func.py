from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, LocationSendMessage, TemplateSendMessage,\
        ButtonsTemplate, URITemplateAction, ConfirmTemplate, PostbackTemplateAction


# QnA Maker Host setting
import http.client, json
host ='' #[add your azure web site here]
endpoint_key = '' #[ add yout QnA Maker endpoint_key here]
kb='' #[add your knowledge base key ]
method =  "/qnamaker/knowledgebases/"+kb +"/generateAnswer" 

#LUIS 
import requests

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

scope=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google.json',scope)  #[you have to get a google sheet json to get acces key]

try:
    client = gspread.authorize(creds)
    GSpreadSheet='' #[add your google sheet's name]
    sh=client.open(GSpreadSheet)
    worksheet=sh.sheet1
except Exception as ex:
    print('Error occurred:', ex)



line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def sendLUIS(event, mtext):
    try:
        r= requests.get(''+mtext) #[add you LUIS end point into '']
        result=r.json()
        #print(result)
        if result['prediction']['topIntent']=='assistant_report':
            #print(result['prediction']['entities'])
            text='''
僅能在智慧手機上開啟
https://liff.line.me/add_your_line_liff_website_here
'''
            #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        elif result['prediction']['topIntent']=='assistant_show_troubleshooting':
           # print(result['prediction']['entities']['$instance']['equipment.name'][0]['text'])
            equipment_name=result['prediction']['entities']['$instance']['equipment.name'][0]['text']
            if equipment_name =='電腦':
                if "自動關機" in mtext :
                    #print('自動關機')
                    question="電腦自動關機簡易排除"
                elif "網路" in mtext:
                    #print("network")
                    question="網路問題簡易排除"
                elif "上網" in mtext:
                    #print("network")
                    question="網路問題簡易排除"
                elif "開機" in mtext:
                    print("boot")
                    question="無法開機簡易排除"
            elif equipment_name =='網路':
                question="網路問題簡易排除"
            elif equipment_name =='上網':
                question="網路問題簡易排除"
            elif equipment_name =='示波器':
                question="示波器簡易排除"
            elif equipment_name =='三用電表':
                question="三用電表簡易排除"
            elif equipment_name =='訊號產生器':
                question="訊號產生器簡易排除"

            question={
                    'question':question,
                    }
            content = json.dumps(question)
            headers={
                    'Authorization' : 'EndpointKey'+ endpoint_key,
                    'Content-Type'  : 'application/json',
                    'Content-Length': len(content)
                    }
            conn = http.client.HTTPSConnection(host)
            conn.request("POST", method, content, headers )
            response = conn.getresponse()
            result=json.loads(response.read())
            result1=result['answers'][0]['answer']
            if 'No good match' in result1:
                text='Sorry there is no answer here.'
            else:
                text=result1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無法理解您的意思，請簡短描述問題或選擇回報助理"))


def sendUse(event):
    try:
        text1='''
歡迎使用設備問答助理
可以輸入你的問題，
例如：
“三用電表量不到電壓” 
“電腦無法開機”
輔助程式將會試著幫助你
若點選選單->“問題回報“按鈕，將開啟回報選單
填妥選單系統將回報問題給予實驗室管理．
'''
        message = TextSendMessage(
                text=text1
                )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(evnet.reply_token, TextSendMessage(text='Fail Occured'))

def troubleshooting(event,user_id):
    question={
            'question':"網路問題簡易排除",
            }
    content = json.dumps(question)
    headers={
            'Authorization' : 'EndpointKey'+ endpoint_key,
            'Content-Type'  : 'application/json',
            'Content-Length': len(content)
            }
    conn = http.client.HTTPSConnection(host)
    conn.request("POST", method, content, headers )
    response = conn.getresponse()
    result=json.loads(response.read())
    result1=result['answers'][0]['answer']
    if 'No good match' in result1:
        text1='Sorry there is no answer here.'
    else:
        text1=result1
    message= TextSendMessage(
            text= text1
            )
    line_bot_api.reply_message(event.reply_token, message)

def sendContact(event):
    try:
        message = TemplateSendMessage(
                alt_text= 'Contact us',
                template = ButtonsTemplate(
                    thumbnail_image_url='https://i.imgur.com/tVjKzPH.jpg',
                    title='聯繫設備管理者',
                    text='僅供緊急狀況使用',
                    actions=[
                        URITemplateAction(label='撥打電話', uri='tel:0987654321')
                        ]
                    )
                )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Fail occurred!'))

def manageForm(event, mtext, user_id):
    try:
        flist = mtext[3:].split('/')
        #roomtype=flist[0]
        #amount=flist[1]
        #in_date=flist[2]
        #out_date=flist[3]
        locate = flist[0]
        equipment =flist[1]
        equipment_location=flist[2]
        problem_descript=flist[3]
        if not (ProblemReport.objects.filter(reporter_id=user_id).exists()):
            worksheet.append_row((datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),user_id, locate,equipment,equipment_location, problem_descript))

            text1= "我們收到你的回報了"
            text1+= "\n 地點: "+ locate
            text1+= "\n 問題設備: " + equipment
            text1+= "\n 設備桌次: " + equipment_location
            text1+= "\n 問題簡述: " + problem_descript
            message= TextSendMessage(
                    text = text1
                    )
        else:
            message=TextSendMessage(text="debug")
        line_bot_api.reply_message(event.reply_token, [message,message])
    except Exception as ex:
        print("ex",ex)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="fail occurred at manageForm segment."))
