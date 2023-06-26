from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

import os

os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# download and load all models
preload_models()

# generate audio from text with voice style and pitch adjustment
text_prompt = "你好，我是 Moss,你的智能助理"
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("moss_said.wav", SAMPLE_RATE, audio_array)

# play audio in notebook
Audio(audio_array, rate=SAMPLE_RATE)