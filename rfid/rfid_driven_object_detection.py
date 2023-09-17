import matplotlib.pyplot as plt
import boto3
import cv2
import json
import pyfirmata2
import serial # 引用pySerial模組
COM_PORT = 'COM10'    # 指定通訊埠名稱
BAUD_RATES = 9600    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
# bucket = 'chtcourse'  #改成自己建立的bucket name <chtcourse-學員號碼>

# s3 = boto3.client('s3')

# with open('./rekognition/biden-1.png', 'rb') as image:
#     s3.upload_fileobj(image, bucket, 'biden-1.png')
# 可以試試看重複上傳的話會怎麼樣

#Face Comparison
def compare_faces(sourceFile, targetFile):

    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=80,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' + str(position['Left']) + ' ' +
              str(position['Top']) + ' matches with ' + similarity +
              '% confidence')

    imageSource.close()
    imageTarget.close()
    return len(response['FaceMatches'])

def detect_labels_local_file(photo):


    client=boto3.client('rekognition')
   
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    print(response)    
    print('Detected labels in ' + photo)    
    # for label in response['Labels'][:3]:
    #     print (label['Name'] + ' : ' + str(label['Confidence']))

    return response


def takePhoto():
    print("拍照中... )")
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('./rekognition/photo.png', image)
try:
    while True:
        while ser.in_waiting:          # 若收到序列資料…
            data_raw = ser.readline()  # 讀取一行
            data = data_raw.decode()   # 用預設的UTF-8解碼
            data=data.rstrip()
            print(data)
            takePhoto()
            photoPath='./rekognition/photo.png'
            response=detect_labels_local_file(photoPath)
            resultStr0="Labels detected: " + str(len(response['Labels']))
            resultStr1=response['Labels'][0]['Name'] + ' : ' + str(response['Labels'][0]['Confidence'])
            resultStr2=response['Labels'][1]['Name'] + ' : ' + str(response['Labels'][1]['Confidence']) 
            resultStr3=response['Labels'][2]['Name'] + ' : ' + str(response['Labels'][2]['Confidence'])    
            img = cv2.imread(photoPath)
            cv2.putText(img,resultStr0, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(img,resultStr1, (10, 80), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(img,resultStr2, (10,120), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(img,resultStr3,(10, 160), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow('photo', img)
            ser.write(str.encode(response['Labels'][0]['Name']+'\n'))
            # 按下任意鍵則關閉所有視窗
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # # source_file = './rekognition/89AFB845.png'
            # source_file = './rekognition/'+data+'.png'
            # # target_file = './rekognition/'+data+'.png'
            # target_file = './rekognition/photo.png'
            # print("source_file:"+source_file)
            # print("target_file:"+target_file)
            # print("人臉辨識中....")
            # face_matches = compare_faces(source_file, target_file)
            # if face_matches==1:
            #     print("辨識成功!")
            # else:
            #     print("辨識失敗...")
            # # print("Face matches: " + str(face_matches))
            # # print('接收到的原始資料：', data_raw)
            # # print('接收到的資料：', data)

except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件
    print('再見！')

# source_file = './rekognition/trump-1.png'
# target_file = './rekognition/trump-2.png'

# face_matches = compare_faces(source_file, target_file)
# print("Face matches: " + str(face_matches))

