from aip import AipSpeech
import speech_recognition as sr

class Baidu_sr():
    def __init__(self,APP_ID='21179500',API_KEY = 'ninYN8Qlg1AIgUvcTGpmQ1L8',SECRET_KEY = 'daGMOpmE17obYnskrrYb6e5IzGdx8ghl'):

        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    def __get_text(self,wav_bytes):
        result = self.client.asr(wav_bytes, 'wav', 16000, {'dev_pid': 1537,})
        try:
            text = result['result'][0]
        except Exception as e:
            print(e)
            text = "Error"
        return text

    # For real time voice recording
    def speech_recog(self):

        r = sr.Recognizer()
        mic = sr.Microphone()

        yield 'Info:Please try to speak something...'
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            audio_data = audio.get_wav_data(convert_rate=16000)
            yield "Info:Got you, now I'm trying to recognize that..."
            yield self.__get_text(audio_data)


if __name__=='__main__':
    baidu=Baidu_sr()

    while(1):
        for text in baidu.speech_recog():
            print(text)
