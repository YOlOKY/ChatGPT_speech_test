# chat-gpt3


####一、apt-get/pip安装python依赖包
sudo apt-get update
sudo apt-get install gcc
sudo apt-get install portaudio19-dev

pip install --upgrade pip --user
pip install pyaudio==0.2.13

安装结果：
baidu-aip          4.16.9
chardet            3.0.4
conda              4.5.12
openai             0.26.3
pip                22.3.1
PyAudio            0.2.13
pygame             2.1.2
pypinyin           0.48.0
textdistance       4.5.0



####二、请自行注册百度AI平台账号
1、打开 conf/config.py
2、填入以下对应信息
BaiDu_App_ID = 'xxx'
BaiDu_API_Key = 'xxx'
BaiDu_Secret_Key = 'xxx'