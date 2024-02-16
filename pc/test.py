
import numpy as np
import time
import cv2
import cv2.aruco as aruco
from math import degrees
import yaml


dist=np.array(([[-0.58650416 , 0.59103816, -0.00443272 , 0.00357844 ,-0.27203275]]))
newcameramtx=np.array([[189.076828   ,  0.    ,     361.20126638]
 ,[  0 ,2.01627296e+04 ,4.52759577e+02]
 ,[0, 0, 1]])
mtx=np.array([[398.12724231  , 0.      ,   304.35638757],
 [  0.       ,  345.38259888, 282.49861858],
 [  0.,           0.,           1.        ]])

# file_path = ("标定文件.yaml")
# with open(file_path, "r") as file:
#     parameter = yaml.load(file.read(), Loader=yaml.Loader)
#     mtx = parameter['camera_matrix']
#     dist = parameter['dist_coeff']
#     camera_u = parameter['camera_u']
#     camera_v = parameter['camera_v']
#     mtx = np.array(mtx)
#     dist = np.array(dist)

#打开笔记本摄像头
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_SIMPLEX #font for displaying text (below)

def get_mouse_point(event,x,y,flags,param):  #鼠标点击位置
    global Point
    if event==cv2.EVENT_LBUTTONDOWN:
        print("Point is",x,y)
        Point.append((x,y))
        print(Point)
    if event==cv2.EVENT_RBUTTONDOWN:
        Point = []

def getpoint():
    global cap, font, dist, newcameramtx, mtx

    ar_dic = {}
    start = time.time()
    ret, frame = cap.read()
    # operations on the frame come here
 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)
    parameters =  aruco.DetectorParameters()
 
    #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

#    if ids != None:
    if ids is not None:
 
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        # 估计每个标记的姿态并返回值rvet和tvec ---不同
        (rvec-tvec).any() # get rid of that nasty numpy value array error
        for i in range(rvec.shape[0]):
            cv2.drawFrameAxes(frame, mtx, dist, rvec[i, :, :], tvec[i, :, :], 0.03) #绘制轴
            aruco.drawDetectedMarkers(frame, corners) #在标记周围画一个正方形
            ar_dic[str(ids[i])] = [degrees(rvec[i, :, :][0][0]),tvec[i, :, :][0]]

        #显示ID，rvec,tvec, 旋转向量和平移向量
        cv2.putText(frame, "Id: " + str(ids), (10,40), font, 0.5, (0, 0, 255),1,cv2.LINE_AA)
        cv2.putText(frame, "rvec: " + str(rvec[i, :, :]), (10, 60), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "tvec: " + str(tvec[i, :, :]), (10,80), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        print(ar_dic)
        print('-------')

    else:
        cv2.putText(frame, "No Ids", (10,64), font, 1, (0,255,0),2,cv2.LINE_AA)
 
    
    # 计算帧率并显示
    #cv2.putText(frame, "rate: " + str(1 / (end-start )), (10, 120), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.imshow("frame",frame)
    cv2.setMouseCallback("frame",get_mouse_point)
 
    key = cv2.waitKey(1)
 
    if key == 27:         # 按esc键退出
        print('esc break...')
        cap.release()
        cv2.destroyAllWindows()
        return
    
    return ar_dic

while True:
    print(getpoint())