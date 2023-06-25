import speech_recognition as sr

print(sr.Microphone.list_microphone_names())

r = sr.Recognizer()

with sr.Microphone(device_index=0) as source:
    print("请说话...")
    audio = r.listen(source, timeout=5)  # 设置timeout参数为5秒

try:
    text = r.recognize_google(audio, language='zh-CN')
    print("你说：", text)
except sr.UnknownValueError:
    print("无法识别音频")
except sr.RequestError as e:
    print("无法连接到Google Speech Recognition服务；{0}".format(e))
