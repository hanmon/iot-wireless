import requests

# PNG图片的URL
png_url = "https://timgm.eprice.com.tw/tw/mobile/img/2022-05/07/5725783/eprice_1_9162a1b878183a5c4350ebb61d64cd07.png"

# 发起HTTP请求并获取图像数据
response = requests.get(png_url)

# 检查请求是否成功
if response.status_code == 200:
    # 打开一个本地文件用于保存图像
    with open("./rekognition/photo.png", "wb") as file:
        file.write(response.content)

    print("PNG图像已下载并保存为photo.png")
else:
    print("无法下载PNG图像。HTTP错误码:", response.status_code)
