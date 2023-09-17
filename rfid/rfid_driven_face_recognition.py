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
    #print(response)
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' + str(position['Left']) + ' ' +
              str(position['Top']) + ' matches with ' + similarity +
              '% confidence')

    imageSource.close()
    imageTarget.close()
    return len(response['FaceMatches']),response

def takePhoto():
    print("拍照中，請微笑 : )")
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
            # source_file = './rekognition/89AFB845.png'
            source_file = './rekognition/'+data+'.png'
            # target_file = './rekognition/'+data+'.png'
            target_file = './rekognition/photo.png'
            print("source_file:"+source_file)
            print("target_file:"+target_file)
            print("人臉辨識中....")
            face_matches,response = compare_faces(source_file, target_file)
            img = cv2.imread(target_file)
            imgHeight, imgWidth, channels = img.shape 
            if face_matches==1:
                print("驗證成功!")
                #send char 's' to arduino
                ser.write(str.encode('succedded'))
                resultStr="Verification Succedded"
                position = response['FaceMatches'][0]['Face']['BoundingBox']
                print(position)
                cv2.putText(img,resultStr,(10, 40), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA)
                # 在圖片上畫一個綠色方框，線條寬度為 2 px
                leftCorner=(int(position['Left']*imgWidth), int(position['Top']*imgHeight))
                rightCorner=(int(position['Left']*imgWidth+position['Width']*imgWidth), int(position['Top']*imgHeight+position['Height']*imgHeight))
                print(leftCorner)
                print(rightCorner)
                cv2.rectangle(img, leftCorner, rightCorner, (0, 255, 0), 2)
                cv2.imshow('photo', img)
                # 按下任意鍵則關閉所有視窗
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("驗證失敗...")
                #send char 'f' to arduino
                ser.write(str.encode('failed'))
                resultStr="Verification Failed"
                cv2.putText(img,resultStr,(10, 40), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA)
                # 在圖片上畫一個綠色方框，線條寬度為 2 px
                cv2.imshow('photo', img)
                # 按下任意鍵則關閉所有視窗
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            # print("Face matches: " + str(face_matches))
            # print('接收到的原始資料：', data_raw)
            # print('接收到的資料：', data)q

except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件
    print('再見！')

# source_file = './rekognition/trump-1.png'
# target_file = './rekognition/trump-2.png'

# face_matches = compare_faces(source_file, target_file)
# print("Face matches: " + str(face_matches))

