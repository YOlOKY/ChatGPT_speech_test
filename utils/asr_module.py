import base64
import requests
# from conf.config import　BaiDu_Asr_Url
# url = BaiDu_Asr_Url
url = 'https://vop.baidu.com/server_api'

def speech2text(speech_data, token, dev_pid=1536):  #'1536：普通话(简单英文),1537:普通话(有标点),1737:英语,1637:粤语,1837:四川话
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = 'GPT3_TX2'
    SPEECH = base64.b64encode(speech_data).decode('utf-8')

    data = {
        'format': FORMAT,
        'rate': RATE,
        'channel': CHANNEL,
        'cuid': CUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }

    headers = {'Content-Type': 'application/json'}

    print('正在识别...')
    r = requests.post(url, json=data, headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result