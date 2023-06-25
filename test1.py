import boto3

# 创建 Amazon Polly 客户端
polly_client = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
    region_name='us-west-2').client('polly')

def text_to_speech_with_emotion(text):
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna',
        Engine='neural',
        TextType='ssml'
    )

    # 将合成的音频保存到文件
    with open('output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

# 调用 text_to_speech_with_emotion 函数
text = "<speak>这是一段具有感情的文本。<prosody rate='slow' volume='x-loud'>这部分语音会以慢速和高音量进行合成。</prosody></speak>"
text_to_speech_with_emotion(text)
