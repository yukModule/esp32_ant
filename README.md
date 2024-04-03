# <center>震动行走机器人🤖</center>

## 🚀参考
- [振动驱动的微型机器人非完整约束补偿的定位方法 (engineering.org.cn)](https://www.engineering.org.cn/ch/article/16557/detail)
- [NN机器人--微型视觉控制振动机器人 - 嘉立创EDA开源硬件平台 (oshwhub.com)](https://oshwhub.com/shukkkk/zhen-dong-ji-qi-ren_copy_copy_copy)
- [【ESP32最全学习笔记（基础篇）——4.ESP32 引脚介绍】「已注销」的博客-CSDN博客](https://blog.csdn.net/m0_46509684/article/details/129105888)
- [kilobot-超赞的集群机器人 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/439647295)
- [GPIO模拟时序控制外设4——红外发射管-CSDN博客](https://blog.csdn.net/qq_41954556/article/details/131414915)

## 💎预览
![预览](/img/正面.png)
![预览](/img/背面.png)

![演示](/video/演示1.mp4)

![原理图](/img/原理图.png)

## 📢介绍
**项目**概述: 
- 应用场景
	1. 教学演示
	2. 群控算法验证
- 依赖与支持
	1. 支持TCP协议通信
	2. 多线程任务处理
	3. PWM调速
	4. NEC协议红外收发


## ❗已知问题
开发中遇到的**问题**:
- [x] 【**已经解决**】pcb设计问题 pwm信号线与wifi天线太近，导致丢包严重
	- 解决方案 
		- 使用 esp-wroom-32u 外置天线 【封装与esp-wroom-32相同】
		- 重画pcb
			- 电驱放边缘
			- 主控下方避开走线
		- 无线设备过多导致干扰严重
		- 改用TCP通信
- [x] 【**已经解决**】两个震动马达振幅不同，难以控制
	- 解决方案
		- 调整震动马达位置
		- 使用两个不同通道的pwm输出
- [x] 【**已经解决**】脚针的角度对移动的控制影响很大，对焊接要求苛刻
	- 解决方案
		- 增厚pcb
		- 反向焊接，探针头朝下

## 👍技术协助
你可以通过以下方式获得**技术帮助**:
- [GitHub](https://github.com/yukModule/)
- [BiliBili](https://space.bilibili.com/22951795)
- [gitee](https://gitee.com/yukmkm/)

## ✍参与作者
- MkM
	- bilibili 无我识l心空妙有

## ⭐主要硬件
- CH340K 【TTL串口通信】
- esp32-wroom-32u 【外置天线】
- IRM-3638T 【红外接收】
- TP4059 【锂电池充放电保护】
- RT9193-33GB 【3.3v稳压】
- 5050ws2812b 【RGB彩灯】
- 小型震动振子马达1034 

### 📵GPIO使用

| **GPIO** | **功能** |
| :--- | :--- |
| pin2 | led |
| pin4 | 左电机 |
| pin17 | 右电机 |
| pin12 | ws2821 RGB |
| pin15 | IRM红外接收 |
| pin26 | 红外发射 |
| pin32 | 电池ADC |

---

## 🚀快速上手
❗必须**先用usb数据线**将机器人与电脑连接后**再打开机器人电源开关**，机器人电源开关在底部

❗当机器人死机无法进入系统时，只需要**关闭再打开机器人电源** 或者按下res开关

### 🌏环境搭建
1. 在Windows操作系统的电脑中**安装Thonny** [1. 开发环境搭建 (itprojects.cn)](https://doc.itprojects.cn/0006.zhishi.esp32/02.doc/index.html#/01.dajianhuanjing)
   [Python+ESP32 快速上手（持续更新中）【 通俗易懂 】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1G34y1E7tE/)
2. 在手机中安装**TCP调试工具**，或使用电脑的TCP调试工具，**端口号为7788**
   服务器**IP地址**为运行机器人后打印出的地址
3. 打开Thonny，连接机器人与电脑，删除esp32中除boot.py文件以外的所有文件
   将**最新代码选中**到esp32中 点击 **上传到/**
   ![下载](/img/下载.png)
   机器人红灯是<font color="#ff0000">充电中</font>，绿灯是<font color="#00b050">充满电</font>，蓝灯是<font color="#00b0f0">已上电</font>
4. 打开esp32的 **config.txt** 修改配置信息

   ❗调试阶段建议 **清除main.py里的程序** 或 **关闭开机运行wifi**

   ❗运行 **main_.py** 必须设置 **main on**

```txt
变量含义：
main <功能: 进入死循环, 防止core1卡死、看门狗重启>
wifi <当且仅当为on时开机启动wifi的TCP服务器>
PASSWORD <WiFi密码>
SSID <WiFi名，确保机器人与上位机共用同一局域网>
bot_name <机器人名>
team <机器人队伍名>
aruco_id <机器人顶部粘贴的Aruco码>

参考设置：
main on
wifi on
PASSWORD 66666666pi
SSID MKM_PRO8
bot_name yuk2
team blue
aruco_id [8]

```

5. 相机标定
   1. https://blog.csdn.net/sunnyrainflower/article/details/131112182

### 🔍程序文件功能概述
- **boot**.py
   - esp32启动时执行的文件，不可删除，不建议在内部运行程序
- **config**.txt
   - 机器人信息配置，可以修改和添加，不可以删除
- **ir_send**.py
   - 红外发送程序，NEC协议红外收发
- **IRM**.py
   - 红外接收程序，NEC协议红外收发
- **main**.py
   - TCP服务器，接收命令处理与任务分配
- **save_load**.py
   - 读取和保存config中的配置
- **WS2812**.py
   - ws2812RGB灯驱动

### ⌨机器人TCP通信指令
- `/connect <wifi名> <wifi密码>` 执行后设置并保存WiFi名和密码，连接该WiFi，开启TCP服务器
- `/say2wifi <信息>` 执行后通过TCP发送该<信息> 到客户端
- `/say2inf <信息>` 执行后通过调用红外发送该<信息>
- `/m <左电机pwm> <右电机pwm> # 控制电机转速` freq=1000 执行后设置当前电机PWM 0~1000
- `/setcolor <r> <g> <b> ` 设置当前ws2812颜色 范围0~255
- `/show ` 执行后通过TCP发送机器人信息到客户端
	- 内容包括：名，睡眠状态，ws2812颜色，队伍名
- `/team <队伍名> ` 设置机器人队伍

### 💻PC端配置与启动
- 相机标定
  - 运行 `拍照.bat` 用不同的视角拍摄棋盘，数量越多越准确
  - 运行 `相机标定.bat` 通过拍照所得的图片生成相机标定文件
- 确保机器人连接的WiFi是本机电脑开启的
- 运行客户端 `客户端.bat`

### ⌨客户端指令
- `/liveip` 查看当前已经建立的连接
- `/rescan` 从新扫描并建立新的连接
- `/send [8] /show` 向 机器人[8]号 发送 /show
- `/line [8] x y ae r` 令 机器人[8]号 沿直线运动到(x,y) 角度容许误差为ae 目标半径为r
- `/arc [9] x0 y0 x1 y1` 令 机器人[8]号 以(x0,y0)为圆心 短弧为轨迹 运动到 (x1,y1)
- `/rot [8] a ae` 令 机器人[8]号 旋转到角度a 容许角度误差为ae
- `/rotp [8] x y ae` 令 机器人[8]号 旋转并指向(x,y) 容许角度误差为ae