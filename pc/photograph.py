# 按j保存一张图片

import cv2
camera=cv2.VideoCapture(0)
 
cv2.namedWindow('imgage', cv2.WINDOW_FREERATIO)
i = -1
flag=camera.isOpened()
camera.set(3,2160)
camera.set(4,3840)
camera.set(6,cv2.VideoWriter.fourcc(*'MJPG'))
print("L:{}".format(camera.get(3)),"H:{}".format(camera.get(4)),
      "FPS:{}".format(camera.get(cv2.CAP_PROP_FPS)))
print(camera.get(cv2.CAP_PROP_FOCUS))
print('英文输入法 按j拍摄')
while flag:
    (grabbed, img) = camera.read()
    cv2.imshow('imgage', img)
    if cv2.waitKey(1) & 0xFF == ord('j'):  
        i += 1
        u = str(i)
        firename=str('pc/images/'+u+'.jpg')
        cv2.imwrite(firename, img)
        print('写入：',firename)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        flag = False
        break