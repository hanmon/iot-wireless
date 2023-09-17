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

    # client = boto3.client('rekognition')

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
        
    print('Detected labels in ' + photo)    
    for label in response['Labels'][:3]:
        print (label['Name'] + ' : ' + str(label['Confidence']))

    return len(response['Labels'])

def detect_labels(source_file):

    client=boto3.client('rekognition')
    imageSource = open(source_file, 'rb')
    
    response = client.detect_protective_equipment(Image={'Bytes': imageSource.read()}, 
        SummarizationAttributes={'MinConfidence':80, 'RequiredEquipmentTypes':['FACE_COVER', 'HAND_COVER', 'HEAD_COVER']})
        
    ppe_items_count=0
    print('Detected PPE for people in image ' + source_file) 
    print('\nDetected people\n---------------') 
    print(response)  
    for person in response['Persons']:
        
        print('Person ID: ' + str(person['Id']))
        print ('Body Parts\n----------')
        body_parts = person['BodyParts']
        if len(body_parts) == 0:
                print ('No body parts found')
        else:
            for body_part in body_parts:
                print('\t'+ body_part['Name'] + '\n\t\tConfidence: ' + str(body_part['Confidence']))
                print('\n\t\tDetected PPE\n\t\t------------')
                ppe_items = body_part['EquipmentDetections']
                if len(ppe_items) ==0:
                    print ('\t\tNo PPE detected on ' + body_part['Name'])
                else:    
                    for ppe_item in ppe_items:
                        ppe_items_count=ppe_items_count+1
                        print('\t\t' + ppe_item['Type'] + '\n\t\t\tConfidence: ' + str(ppe_item['Confidence'])) 
                        print('\t\tCovers body part: ' + str(ppe_item['CoversBodyPart']['Value']) + '\n\t\t\tConfidence: ' + str(ppe_item['CoversBodyPart']['Confidence']))
                        print('\t\tBounding Box:')
                        print ('\t\t\tTop: ' + str(ppe_item['BoundingBox']['Top']))
                        print ('\t\t\tLeft: ' + str(ppe_item['BoundingBox']['Left']))
                        print ('\t\t\tWidth: ' +  str(ppe_item['BoundingBox']['Width']))
                        print ('\t\t\tHeight: ' +  str(ppe_item['BoundingBox']['Height']))
                        print ('\t\t\tConfidence: ' + str(ppe_item['Confidence']))
            print()
        print()

    # print('Person ID Summary\n----------------')
    # display_summary('With required equipment',response['Summary']['PersonsWithRequiredEquipment'] )
    # display_summary('Without required equipment',response['Summary']['PersonsWithoutRequiredEquipment'] )
    # display_summary('Indeterminate',response['Summary']['PersonsIndeterminate'] )
   
    print() 
    return len(response['Persons']),ppe_items_count

def takePhoto():
    print("拍照中... ") 
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('./rekognition/photo.png', image)
try:
    while True:
        while ser.in_waiting:          # 若收到序列資料…
            data_raw = ser.readline()  # 讀取一行
            data = data_raw.decode()   # 用預設的UTF-8解碼
            data=data.rstrip()  #去除結尾多餘字元
            print(data)
            takePhoto()
            print("辨識人臉及口罩中...")
            photoPath='./rekognition/photo.png'
            personCount,maskCount=detect_labels(photoPath)
            resultStr="People:{},Mask:{}".format(personCount,maskCount)
            print(resultStr)
            ser.write(str.encode(resultStr))
            img = cv2.imread(photoPath)
            cv2.putText(img,resultStr, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(img,"Press Any Key To Continue", (10, 80), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow('photo', img)

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

