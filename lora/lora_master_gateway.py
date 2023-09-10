#Lora MASTER範例
import threading
import paho.mqtt.client as mqtt
import serial, time, re, base64
import configparser,json
from tqdm import tqdm

config = configparser.ConfigParser()
config.read('../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
dht11Id    = config.get('device-key', 'dht11Id')

host = "iot.cht.com.tw"
topic = '/v1/device/' + deviceId + '/rawdata'
print(topic)
user, password = projectKey, projectKey

client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(host, 1883, 60)
# 設定串列通訊參數
#port = 'COM20'  # 這裡需要根據你的設備更改串列埠
port = '/dev/ttyUSB0'
baud_rate = 38400
#ser = serial.Serial(port, baud_rate, timeout=5)
ser = serial.Serial(port, baud_rate)
#ser = serial.Serial(port,baud_rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=2)
SLAVE_ADDR = '27002e'

'''
初始化lora模組
SLAVE
1) LoraMode SLAVE
2) LoraSystemMode inNormal
3) LoraStartWork ENABLE
MASTER
1) LoraMode MASTER
2) LoraSystemMode inNormal
3) LoraStartWork ENABLE
4) LoraJoinNode [Slave Address]
'''
def lora_init(mode="MASTER"):
    ser.write("FactoryReset\r".encode())
    for i in range(10):
        print(ser.readline())
        time.sleep(0.1)
    if mode=="MASTER":
        ser.write("LoraMode MASTER\r".encode())
        print(ser.readline())
        print(ser.readline())   
    elif mode=="SLAVE":
        ser.write("LoraMode SLAVE\r".encode())
        print(ser.readline())
        print(ser.readline())
    ser.write("LoraSystemMode inNormal\r".encode())
    print(ser.readline())
    print(ser.readline())
    ser.write("LoraStartWork ENABLE\r".encode())
    print(ser.readline())
    print(ser.readline())

stop_event = threading.Event()


def send_data_periodically():
    while True:
        ser.write("LoraNodeData 27002e DataTest\r".encode())
        time.sleep(3)  # 每隔5秒發送一次資料
        if stop_event.is_set():
            print('Lora MASTER傳送執行緒已停止')
            break

send_thread = threading.Thread(target=send_data_periodically)

try:
    #
    ser.write("UartEchoOn\r".encode())
    print(ser.readline())
    print(ser.readline())

    lora_init("MASTER")
    cmd_str="LoraJoinNode "+ str(SLAVE_ADDR) +"\r"
    ser.write(cmd_str.encode())
    # ser.write('LoraJoinNode '+ str(SLAVE_ADDR) +'\r'.encode())
    rx_bytes=ser.readline()
    print(rx_bytes)
    count=0
    while "EVT=JoinOK".encode() not in rx_bytes:
        rx_bytes=ser.readline()
        print(rx_bytes)
        count+=1
    print("SLAVE "+rx_bytes.decode()[5:10]+"加入Lora網路成功")
    send_thread.start()
    print("每5秒送一次資料給SLAVE")
    while 1:
        #ser.write("LoraNodeData 27002e DataTest\r".encode())
        if ser.in_waiting:
            rx_str=ser.readline().decode()
            pattern = r'(.+?)=(.+)'
            rx_strs=rx_str.split(" ")
            kv_pairs={}
            for kv_pair in rx_strs:
                match_data = re.match(pattern, kv_pair)
                if match_data:
                    key = match_data.group(1)
                    value = match_data.group(2)
                    kv_pairs[key]=value
                    print("Key:", key)
                    print("Value:", value)
            if "Data" in kv_pairs:
                print("Node:{},DataLength:{},Data:{}".format(kv_pairs["Node"],kv_pairs["DataLength"],kv_pairs["Data"]))
                sensor_raw_data=(base64.b64decode(kv_pairs["Data"])).decode()
                sensor_values=sensor_raw_data.split(",")
                temp,humid=sensor_values[0],sensor_values[1]
                print("Temp:{},Humid:{}".format(temp,humid))
                #publish to CHT IoT Platform
                t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))
                payload = [{"id":dht11Id,"value":[temp, humid], "time":t}]
                print(payload)
                client.publish(topic, "%s" % ( json.dumps(payload) ))
                time.sleep(3)
        #print(rx_str)
        #time.sleep(5)

    print('結束！') 
    ser.close()
except Exception as e:
    # 當異常發生時，會執行這裡的程式碼塊
    print("An exception occurred:", e)
    stop_event.set()  # 設置事件，通知執行緒停止
    # 等待執行緒結束
    send_thread.join()
    ser.close()
    print('再見！') 
except KeyboardInterrupt:
    print("Ctrl-C停止")
    stop_event.set()  # 設置事件，通知執行緒停止
    # 等待執行緒結束
    send_thread.join()
    ser.close()    # 清除序列通訊物件
    print('再見！') 

    
