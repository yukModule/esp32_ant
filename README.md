# 震动驱动机器人

## 参考
- [振动驱动的微型机器人非完整约束补偿的定位方法 (engineering.org.cn)](https://www.engineering.org.cn/ch/article/16557/detail)
- [NN机器人--微型视觉控制振动机器人 - 嘉立创EDA开源硬件平台 (oshwhub.com)](https://oshwhub.com/shukkkk/zhen-dong-ji-qi-ren_copy_copy_copy)
- [【ESP32最全学习笔记（基础篇）——4.ESP32 引脚介绍】「已注销」的博客-CSDN博客](https://blog.csdn.net/m0_46509684/article/details/129105888)
- [MicroPython for ESP32 多线程问题及解决方案 - 哔哩哔哩 (bilibili.com)](https://www.bilibili.com/read/cv16282686/)
- [kilobot-超赞的集群机器人 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/439647295)
- [GPIO模拟时序控制外设4——红外发射管-CSDN博客](https://blog.csdn.net/qq_41954556/article/details/131414915)

## 介绍
**项目**概述: 
- 应用场景
	1. 教学演示
	2. 群控算法验证
- 依赖与支持
	1. 支持TCP协议通信
	2. 多线程任务处理
	3. PWM调速
	4. NEC协议红外收发


## 已知问题
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

## 技术协助
你可以在一下获得**技术帮助**:
- [GitHub](https://github.com/yukModule/)
- [BiliBili](https://space.bilibili.com/22951795)

## 参与作者
- MkM
	- bilibili 无我识l心空妙有

## 主要硬件
- CH340K 【TTL串口通信】
- esp32-wroom-32u 【外置天线】
- IRM-3638T 【红外接收】
- TP4059 【锂电池充放电保护】
- RT9193-33GB 【3.3v稳压】
- 5050ws2812b 【RGB彩灯】
- 小型震动振子马达1034 

### 管脚使用

| GPIO | 功能 |
| :--- | :--- |
| pin2 | led |
| pin4 | 左电机 |
| pin17 | 右电机 |
| pin12 | ws2821 RGB |
| pin15 | IRM红外接收 |
| pin26 | 红外发射 |
| pin32 | 电池ADC |

### 物料清单

| No. | Quantity | Comment              | Designator              | Footprint                           | Value | Manufacturer Part    | Manufacturer    | Supplier Part | Supplier |
|-----|----------|----------------------|-------------------------|-------------------------------------|-------|----------------------|-----------------|---------------|----------|
| 1   | 1        | 100nF                | C1                      | C0603                               | 100nF |                      |                 |               |          |
| 2   | 1        | 10uf                 | C6                      | C0603                               |       |                      |                 |               |          |
| 3   | 1        | 1uf                  | C7                      | C0603                               |       |                      |                 |               |          |
| 4   | 2        | 10uf                 | C8,C9                   | C0603                               | 10uf  |                      |                 |               |          |
| 5   | 2        | 1uf                  | C10,C11                 | C0603                               | 1uf   |                      |                 |               |          |
| 6   | 1        | 22uf                 | C12                     | C0603                               | 22uf  |                      |                 |               |          |
| 7   | 1        | 100nf                | C13                     | C0603                               | 100nf |                      |                 |               |          |
| 8   | 1        | ESP32-WROOM-32       | ESP-WROOM-32            | WIFIM-SMD_ESP-WROOM-32              |       | ESP32-WROOM-32       | ESPRESSIF(乐鑫)   | C95209        | LCSC     |
| 9   | 2        | -                    | GND,GND1                | HDR-TH_1P-P2.54-V-M                 |       | -                    | BOOMELE(博穆精密)   | C81276        | LCSC     |
| 10  | 1        | IRM-3638T            | IR1                     | OPTO-TH_IRM-3638T                   |       | IRM-3638T            | EVERLIGHT(亿光)   | C16216        | LCSC     |
| 11  | 4        | 19-213/R6W-BP2Q2B/3T | LED1,LED2,LED-CH,LED-CO | LED0603-R-RD                        |       | 19-213/R6W-BP2Q2B/3T | EVERLIGHT(台湾亿光) | C181863       | LCSC     |
| 12  | 2        | 2.54-1*2P母           | M1,M2                   | HDR-TH_2P-P2.54-V-F                 |       | 2.54-1*2P母           | BOOMELE(博穆精密)   | C49661        | LCSC     |
| 13  | 1        | MICRO 5.9ZB5.0       | MICRO_B2                | MICRO-USB-SMD_MICRO-5.9ZB5.0        |       | MICRO 5.9ZB5.0       | SHOU HAN(首韩)    | C456005       | LCSC     |
| 14  | 1        | MSK-12C01-07         | Power                   | SW-SMD_MSK12CO2-BDM                 |       | MSK-12C01-07         |                 | C9900005167   | LCSC     |
| 15  | 2        | S8050 J3Y            | Q3,Q4                   | SOT-23-3_L2.9-W1.3-P1.90-LS2.4-BR   |       | S8050 J3Y            | CBI(创基)         | C2828466      | LCSC     |
| 16  | 1        | S9013                | Q5                      | SOT-23-3_L2.9-W1.6-P1.90-LS2.8-BR   |       | S9013                | Hottech(合科泰)    | C181163       | LCSC     |
| 17  | 2        | AO3400A              | Q6,Q7                   | SOT-23-3_L2.9-W1.3-P1.90-LS2.4-BR   |       | AO3400A              | HUASHUO(华朔)     | C700953       | LCSC     |
| 18  | 5        | 10K                  | R1,R5,R6,R7,R9          | R0805                               | 10K   |                      |                 |               |          |
| 19  | 2        | 1k                   | R18,R19                 | R0805                               | 1k    | RC0603FR-07330RL     | YAGEO(国巨)       |               | LCSC     |
| 20  | 4        | 1k                   | R27,R29,R30,R31         | R0805                               | 1k    |                      |                 |               |          |
| 21  | 1        | 4.7k                 | R28                     | R0805                               | 4.7k  |                      |                 |               |          |
| 22  | 2        | SMD3X4               | RDL,RS                  | SW-SMD_L4.0-W3.0-LS4.8              |       | SMD3X4               |                 | C9900013942   | LCSC     |
| 23  | 1        | CH340K               | U7                      | ESOP-10_L4.9-W3.9-P1.00-LS6.2-BL-EP |       | CH340K               | WCH(南京沁恒)       | C968586       | LCSC     |
| 24  | 1        | TP4059               | U8                      | SOT-23-6_L2.9-W1.6-P0.95-LS2.8-BR   |       | TP4059               | TOPPOWER(南京拓微)  | C80364        | LCSC     |
| 25  | 1        | RT9193-33GB          | U9                      | SOT-23-5_L3.0-W1.7-P0.95-LS2.8-BL   |       | RT9193-33GB          | RICHTEK(立锜)     | C15651        | LCSC     |
| 26  | 2        | +                    | VCC,VCC1                | HDR-TH_1P-P2.54-V-M                 |       | +                    | BOOMELE(博穆精密)   | C81276        | LCSC     |
| 27  | 1        | 5050WS2812B          | WS2812                  | LED-SMD_5050WS2812B                 |       | 5050WS2812B          |                 | C2874876      | LCSC     |


## 快速上手
❗必须**先用usb数据线**将机器人与电脑连接后**再打开机器人电源开关**，机器人电源开关在底部
❗当机器人死机无法进入系统时，只需要**关闭再打开机器人电源** 或者按下res开关

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
```
main <功能: 进入死循环, 防止core1卡死、看门狗重启>
wifi <当且仅当为on时开机启动wifi的TCP服务器>
PASSWORD <WiFi密码>
SSID <WiFi名，确保机器人与上位机共用同一局域网>
bot_name <机器人名>
team <机器人队伍名>

参考
main on
wifi on
PASSWORD abc123123abc1237
SSID mkm_iqoowifi
bot_name yuk2
team blue

```

### 程序文件功能概述
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
- **sthread**.py
   - 多线程class
- **WS2812**.py
   - ws2812RGB灯驱动

### 机器人TCP通信指令
- `/connect <wifi名> <wifi密码>` 执行后设置并保存WiFi名和密码，连接该WiFi，开启TCP服务器
- `/say2wifi <信息>` 执行后通过TCP发送该<信息> 到客户端
- `/say2inf <信息>` 执行后通过调用红外发送该<信息>
- `/move <左电机pwm> <右电机pwm> # 控制电机转速` freq=1000 执行后设置当前电机PWM 0~1000
- `/sleep <sleep/wake> `  停止运动且不在执行/move指令
- `/setcolor <r> <g> <b> ` 设置当前ws2812颜色 范围0~255
- `/name <bot名>`  设置机器人名
- `/show ` 执行后通过TCP发送机器人信息到客户端
	- 内容包括：名，睡眠状态，ws2812颜色，队伍名
- `/team <队伍名> ` 设置机器人队伍
- `/randomcolor`  随机ws2812的颜色一次

### PC端启动
- 运行pc文件下的main.py
- 确保机器人连接的是pc电脑开启的热点
- 运行后自动连接

### PC客户端指令
- `/liveip` 查看当前已经建立的连接
- `/rescan` 从新扫描并建立新的连接
- `192.168.xxx.xxx:/wryyyyy` 向ip为192.168.xxx.xxx的服务器发送**/wryyyyy**