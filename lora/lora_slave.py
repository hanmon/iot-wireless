#Lora SLAVE範例
import threading
import serial, time, re , base64
import numpy as np

# 設定串列通訊參數
port = 'COM21'  # 這裡需要根據你的設備更改串列埠
baud_rate = 38400
#ser = serial.Serial(port, baud_rate, timeout=5)
ser = serial.Serial(port, baud_rate)
#ser = serial.Serial(port,baud_rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=2)
SLAVE_ADDR = '27002e'
MASTER_ADDR = '440033'
LORA_MODE = "SLAVE"
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
        temp = np.random.randint(10, 32)
        humid = np.random.randint(40, 80)
        formated_data = f"{temp},{humid}"
        print("encode_data:{},length:{}".format(formated_data,len(formated_data)))
        #encoded_base64 = base64.b64encode(encoded_data + b'\x00' * (16 - len(encoded_data)))
        encoded_base64_str = base64.b64encode(formated_data.encode()).decode()
        print("encode_base64_data:{},length:{}".format(encoded_base64_str,len(encoded_base64_str)))
        ser.write(("LoraNodeData "+encoded_base64_str+"\r").encode())
        time.sleep(3)  # 每隔5秒發送一次資料
        if stop_event.is_set():
            print('Lora SLAVE傳送執行緒已停止')
            break

send_thread = threading.Thread(target=send_data_periodically)

try:
    #
    ser.write("UartEchoOn\r".encode())
    print(ser.readline())
    print(ser.readline())

    lora_init(LORA_MODE)
    # cmd_str="LoraJoinNode "+ str(SLAVE_ADDR) +"\r"
    # ser.write(cmd_str.encode())
    # ser.write('LoraJoinNode '+ str(SLAVE_ADDR) +'\r'.encode())
    rx_bytes=ser.readline()
    print(rx_bytes)
    count=0
    while "Join the AcsipLoraNet SUCCESSED!".encode() not in rx_bytes:
        rx_bytes=ser.readline()
        print(rx_bytes)
        count+=1
    print("SLAVE加入Lora網路成功")
    send_thread.start()
    print("每5秒送一次資料給MASTER")
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
                print("LoraGateWayAddr:{},DataLength:{},Data:{}".format(kv_pairs["LoraGateWayAddr"],kv_pairs["DataLength"],kv_pairs["Data"]))
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

    
