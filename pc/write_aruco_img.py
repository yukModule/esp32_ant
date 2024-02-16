# 生成aruco二维码

import cv2
import numpy as np
# 生成aruco标记
# 加载预定义的字典
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

# 生成标记
markerImage = np.zeros((200, 200), dtype=np.uint8)
for i in range(12):
    markerImage = cv2.aruco.generateImageMarker(dictionary, i, 200, markerImage, 1);
    print(i)
    firename='pc/armark/'+str(i)+'.png'
    cv2.imwrite(firename, markerImage);
