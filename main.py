
import speech_recognition as sr
import openai
import pyttsx3
from gtts import gTTS

import os

# Load API key from key.txt file
api_key_file = os.path.join(os.path.dirname(__file__), "key")
with open(api_key_file, "r") as f:
    api_key = f.read().strip()

openai.api_key = api_key

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
        audio = r.listen(source, timeout=0.5)

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
            
            def text_to_speech(text):
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()

            # 调用 text_to_speech 函数
            text_to_speech(text)
            
            # def text_to_speech(text, filename):
            #     tts = gTTS(text=text, lang='zh-cn', slow=False, speed=1.5)
            #     tts.save(filename)
            #     os.system('start ' + filename)

            # # 调用text_to_speech函数
            # filename = "output.mp3"
            # text_to_speech(text, filename)
            
        except:
            messages.pop()
            print('ChatGPT：出现错误\n')

if __name__ == "__main__":
    main()
