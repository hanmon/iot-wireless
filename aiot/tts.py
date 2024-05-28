#import openai related packages and varables
from openai import OpenAI
import wave
import pyaudio
import os,time
import configparser 
config = configparser.ConfigParser()
config.read('../openai.conf')
openai_key = config.get('openai_key', 'key')
client = OpenAI(api_key=openai_key)
is_space_key_pressed=False
# 设置录音参数
FORMAT = pyaudio.paInt16
CHANNELS = 1  # 声道数
RATE = 44100  # 采样率
CHUNK = 1024  # 缓冲区大小
RECORD_SECONDS = 5  # 录制时长
WAVE_OUTPUT_FILENAME = "in.wav"  # 输出文件名
audio = pyaudio.PyAudio()
import pixels
#for led displaying
pixel = pixels.Pixels()
def led_on():
    # pixel = pixels.Pixels()
    pixel.wakeup()
    time.sleep(3)


def led_off():
    # pixel = pixels.Pixels()
    pixel.off()
    time.sleep(1)

def led_think():
    # pixel = pixels.Pixels()
    pixel.think()
    time.sleep(1)

def led_speak():
    # pixel = pixels.Pixels()
    pixel.speak()
    time.sleep(1)

def play_audio_file(fname):
    os.system("aplay " + fname + " > /dev/null 2>&1")

def ai_speak(msg):
    speech_file_path = "speech.wav"
    print("msg:{}".format(msg))
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=msg
    )
    result=response.stream_to_file(speech_file_path)
    led_speak()
    result=os.system("mpg123 {} > /dev/null 2>&1".format(speech_file_path))
    if result==0:
        print("執行成功")
        #play_audio_file(speech_file_path)
    else:
        print("播放失敗")
    led_off()



def main():
    # os.system("alsactl --file ~/.config/asound.bee restore")
    # src = Source(rate=16000, channels=1, frames_size=1600)
    # ec = EC(channels=src.channels, capture=0, playback=2) 

    # # try:
    # #     model = sys.argv[1]
    # #     sens  = sys.argv[2]
    # #     kws = KWS(model, sensitivity=float(sens))
    # #     #kws = KWS(model='hi_lbj', sensitivity=0.65)

    # # except IndexError:
    # #     #sens  = sys.argv[1]
    # #     sens  = 1
    # #     #sens  = 0.65
    # #     kws = KWS(sensitivity=float(sens))
    # #     print("sens: ", sens)
    # #     #kws = KWS()

    # def on_detected(keyword):
    #     print("Button pressed")
    #     global is_space_key_pressed
    #     is_space_key_pressed=True
    #     print('found {}'.format(keyword))
    #     play_audio_file("resources/ding_half.wav")

    #     try:
    #         subprocess.call("kill -9 `ps aux | grep python3 | grep yt3.py | awk '{print $2}'`", shell=True)
    #     finally:
    #         audioRecorderCallback()
            
    # def mycallback(channel):
    #         print("Button pressed")
    # try:
    #     GPIO.add_event_detect(BTN_PIN, \
    #     GPIO.RISING, \
    #     callback=on_detected, \
    #     bouncetime=200)
    #     while True:
    #         time.sleep(10)
    # finally:
    #     GPIO.cleanup()
#for waking up by sound
    # kws.on_detected = on_detected

    # src.pipeline(ec, kws)

    # src.pipeline_start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            led_off()
            #t = threading.Thread(target=led_off, args=())
            #t.start()
            break

    # src.pipeline_stop()


if __name__ == '__main__':
    main()