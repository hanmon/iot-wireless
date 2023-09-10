import numpy as np
import base64
temp = np.random.randint(10, 32)
humid = np.random.randint(40, 80)
formated_data = f"{temp},{humid}"
print("encode_data:{},length:{}".format(formated_data,len(formated_data)))
#encoded_base64 = base64.b64encode(encoded_data + b'\x00' * (16 - len(encoded_data)))
encoded_base64 = base64.b64encode(formated_data.encode())

print("encode_base64_data:{},length:{}".format(encoded_base64.decode(),len(encoded_base64)))
encoded_base64_str=encoded_base64.decode()
concatedStr="LoraNodeData "+encoded_base64_str+"\r"
print(concatedStr)
#ser.write("LoraNodeData "+encoded_base64.decode()+"\r".encode)