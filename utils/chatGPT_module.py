import openai
from conf.config import OpenAI_key
from utils.tts_modeule import answer2voice

openai.api_key = OpenAI_key

def gpt_qa(prompt):
    # Get my answer
    response = openai.Completion.create(
        # engine="text-curie-001",  #Curie擅长进行问答和作为通用聊天机器人。例如，如果您正在构建一个客户支持聊天机器人，您可能会选择 Curie 来更快地处理大量请求
        engine="text-davinci-003",  #Davinci更擅长分析复杂的文本，OpenAI称Davinci-text-002/003是GPT-3.5，而它们均为InstrucGPT类型的模型，ChatGPT是基于其中一个微调模型得到
        prompt=prompt,
        temperature=1,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        ans = response["choices"][0]["text"].strip()
    except Exception as e:
        ans = "不知道"
    return ans

def answer_by_gpt(query):
    answer = gpt_qa("请用中文回答：" + query)  # chatGPT
    if "我叫" in answer:
        answer = "我叫小宝"
    print("answer:", answer)
    answer2voice(answer,sleep_time=len(answer)*0.225)