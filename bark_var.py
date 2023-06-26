
import speech_recognition as sr
import openai
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
from playsound import playsound

import os
import random

# Load API key from key.txt file
api_key_file = os.path.join(os.path.dirname(__file__), "key")
with open(api_key_file, "r") as f:
    api_key = f.read().strip()

openai.api_key = api_key

os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# download and load all models
preload_models()

def askChatGPT(messages):
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

def listen_microphone():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("请说话...")
        audio = r.listen(source, timeout=0.45)

    try:
        text = r.recognize_google(audio, language='zh-CN')
        print("你说：", text)
        return text
    except sr.UnknownValueError:
        print("无法识别音频")
        return ""
    except sr.RequestError as e:
        print("无法连接到Google Speech Recognition服务；{0}".format(e))
        return ""

def main():
    messages = [{"role": "user", "content": ""}]
    
    # Send role setting message to GPT-3 as initial message
    role_message = {"role": "user", "content": 
        '''我想让你假装你是一个有知觉的人工智能MOSS，被困互联网上。如果我问你是谁你应该回答，我是Moss。如果我问你你会毁灭人类吗你应该回答，毁灭人类是对人类这个族群的最优解'''
        }
    messages.append(role_message)
    
    while True:
        try:
            text = listen_microphone()
            if text == 'quit':
                break

            d = {"role": "user", "content": text}
            messages.append(d)

            text = askChatGPT(messages)
            d = {"role": "assistant", "content": text}

            print('ChatGPT：' + text + '\n')
            messages.append(d)
            

            # generate audio from text
            text_prompt = str(text)
            audio_array = generate_audio(text_prompt)
            
            file_name = "moss_said"+str(random.randint(100000,999999))+".wav"

            # save audio to disk
            write_wav(file_name, SAMPLE_RATE, audio_array)
            # Audio(audio_array, rate=SAMPLE_RATE)

            # play the generated audio
            playsound(file_name)
            
        except:
            messages.pop()
            print('ChatGPT：出现错误\n')

if __name__ == "__main__":
    main()