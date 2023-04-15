# 默认输入的服务器地址，测试时候使用，避免登录总是输入地址麻烦
default_server = "127.0.0.1:1"

# 定义服务器端口，一个端口一个房间
PORT = range(1, 3)

DIR_PATH = ""


# 浏览器请求头文件
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', }
headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko)Chrome/62.0.3202.94 Safari/537.36'}


# 语音保存播放开关
VOICE_SWITCH = True



#OpenAI_key = "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"#这里放入你的key，我这里隐藏了
OpenAI_key = "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"
# 百度密钥
BaiDu_App_ID = '114a49dea3fc45edbbb776110e540ae9'
BaiDu_API_Key = 'rbo2tPlijQ3c08zUsgaNZ9f7'
BaiDu_Secret_Key = '1weW6KEfHl8cQqtWwr7CWn1pG5UNImsA'
BaiDu_OpenApi_Url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"

# 百度语音识别
BaiDu_Asr_Url = 'http://vop.baidu.com/server_api'





####唤醒词
#picovoice_key="y2dlDmQSvdu2BlOnq6L5nLsyDwZ+pjUiyhTch2fk5yu+NlVO22t4pA=="
Picovoice_key="EreKPy6N6tT/nenBtl5SUQ6fPPHmrsJg96J9lODQH+Jk7CrluKdJrQ=="
Picovoice_keyword_paths=[r'data/picovoice/shell-ball_en_windows_v2_1_0.ppn']
# Picovoice_keyword_paths=[r'data/picovoice/shell-ball_en_raspberry-pi_v2_1_0.ppn']
# Picovoice_keyword_paths=[r'data/picovoice/hi-bell_en_raspberry-pi_v2_1_0.ppn']


