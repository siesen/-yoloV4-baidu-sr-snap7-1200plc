#sphinx识别率太低，怎么训练和改进模型
import speech_recognition as sr

#path='data/harvard.wav'

r=sr.Recognizer()
mic=sr.Microphone()
#names=sr.Microphone.list_microphone_names()
#for each in names:
#      print(each)
#harvard=sr.AudioFile(path)
with mic as source:
#      r.adjust_for_ambient_noise(source)
      print('say something')
      audio=r.listen(source)

#save the speech
with open("arctic_0001.wav", "wb") as f:
    f.write(audio.get_wav_data())
      
result=r.recognize_sphinx(audio,language='zh-CN')

try:
    print("Sphinx thinks you said --" + result)
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
