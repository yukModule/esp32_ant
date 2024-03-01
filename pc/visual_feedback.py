import contextlib
from threading import Thread
import numpy as np
import time
import cv2
import cv2.aruco as aruco
import math
import yaml

bot_posture_dic = {} # {'[8]':bot_posture([8]), }
Point = []

class bot_posture:
    '''滑动均值滤波 保存位姿'''
    def __init__(self,id):
        self.aruco_id = id
        self.angle_list = []
        self.x_list = []
        self.y_list = []
        self.x = 0
        self.y = 0
        self.angle = 0
    
    def ava_filter(self, x, filt_length):  # sourcery skip: avoid-builtin-shadow
        '''
        x: 待处理列表
        filt_length: 滑动窗口大小
        '''
        N = len(x)
        res = []
        for i in range(N):
            if i <= filt_length // 2 or i >= N - (filt_length // 2):
                temp = x[i]
            else:
                sum = 0
                for j in range(filt_length):
                    sum += x[i - filt_length // 2 + j]
                temp = sum * 1.0 / filt_length
            res.append(temp)
        return res

    def denoise(self):
        if len(self.angle_list) >= 10:
            for _ in range(4):
                res = self.ava_filter(self.angle_list, 6)
                self.angle_list = res
            self.angle = sum(res) / len(res)
            self.angle_list.pop(0)
    
    def denoise_x(self):
        if len(self.x_list) >= 10:
            for _ in range(4):
                res = self.ava_filter(self.x_list, 6)
                self.x_list = res
            self.x = sum(res) / len(res)
            self.x_list.pop(0)
    
    def denoise_y(self):
        if len(self.y_list) >= 10:
            for _ in range(4):
                res = self.ava_filter(self.y_list, 6)
                self.y_list = res
            self.y = sum(res) / len(res)
            self.y_list.pop(0)

# 加载相机标定
file_path = ("pc/标定文件.yaml")
with open(file_path, "r") as file:
    parameter = yaml.load(file.read(), Loader=yaml.Loader)
    mtx = parameter['camera_matrix']
    dist = parameter['dist_coeff']
    camera_u = parameter['camera_u']
    camera_v = parameter['camera_v']
    mtx = np.array(mtx)
    dist = np.array(dist)

#打开笔记本摄像头
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_SIMPLEX #font for displaying text (below)

def getpoint():
    '''通过机器视觉 获取aruco码的位姿'''
    global cap, font, dist, newcameramtx, mtx, bot_posture_dic, angle_list, frame
    start = time.time()
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    parameters =  aruco.DetectorParameters()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

    if ids is not None:
     
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        # 估计每个标记的姿态并返回值rvet和tvec
        (rvec-tvec).any()
        for i in range(rvec.shape[0]):
            # cv2.drawFrameAxes(frame, mtx, dist, rvec[i, :, :], tvec[i, :, :], 0.03) #绘制轴
            aruco.drawDetectedMarkers(frame, corners) #在标记周围画一个正方形

            # 角度估计
            R=np.zeros((3,3),dtype=np.float64)
            with contextlib.suppress(Exception):
                cv2.Rodrigues(rvec[i, :, :],R)
            sy=math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
            singular=sy< 1e-6

            ## 滚动
            z = math.atan2(R[1, 0], R[0, 0]) if not singular else 0
            rz = -1 * z * 180.0 / math.pi + 90
            if rz>180:
                rz = rz - 360
            x = tvec[i, :, :][0][0] * 100
            y = -1 * tvec[i, :, :][0][1] * 100

            if str(ids[i]) not in bot_posture_dic:
                bot_posture_dic[str(ids[i])] = bot_posture(str(ids[i]))
                bot_posture_dic[str(ids[i])].angle_list = [rz]
                bot_posture_dic[str(ids[i])].x_list = [x]
                bot_posture_dic[str(ids[i])].y_list = [y]

            else:
                bot_posture_dic[str(ids[i])].angle_list.append(rz)
                bot_posture_dic[str(ids[i])].x_list.append(x)
                bot_posture_dic[str(ids[i])].y_list.append(y)

            

            bot_posture_dic[str(ids[i])].denoise_x()
            bot_posture_dic[str(ids[i])].denoise_y()
            bot_posture_dic[str(ids[i])].denoise()

            
        #显示ID，rvec,tvec, 旋转向量和平移向量
        cv2.putText(
            frame,
            f"Id: {str(ids)}",
            (10, 40),
            font,
            0.5,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "x: {:.2f}".format(x),
            (10, 60),
            font,
            0.5,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "y: {:.2f}".format(y),
            (10, 80),
            font,
            0.5,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "angle: {:.2f}".format(rz),
            (10, 100),
            font,
            0.5,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

    else:
        cv2.putText(frame, "No Ids", (10,64), font, 1, (0,255,0),2,cv2.LINE_AA)

    cv2.imshow("frame",frame)

    key = cv2.waitKey(1)

    if key == 27:         # 按esc键退出
        print('esc break...')
        cap.release()
        cv2.destroyAllWindows()
        return
    return

def get_bot_posture():
    global bot_posture_dic # ={'[8]':class}
    return bot_posture_dic

def task_open_vf():
    '''多线程开启视觉反馈'''
    def open_vf():
        while True:
            getpoint()
    task = Thread(target=open_vf)
    task.start()

def show_err(err, x, y):
    '''在屏幕上显示角度误差与当前位置'''
    global frame, font
    cv2.putText(
        frame,
        "angle error: {:.2f}".format(err),
        (10, 120),
        font,
        0.5,
        (255, 0, 0),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "bot: ({:.2f}, {:.2f})".format(x, y),
        (10, 140),
        font,
        0.5,
        (255, 0, 0),
        1,
        cv2.LINE_AA,
    )
