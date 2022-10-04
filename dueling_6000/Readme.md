# Readme

机器人无地图导航使用了深度学习中的 CNN 和强化学习中的 DQN 变种。达到了平滑速度，动态避障和到达目标点的效果。需要注意此项目开展时间为 2019 年 10 月，这里展示了其中一组参数的模型。

Robotic map-less navigation used CNNs in deep learning and DQN variants in reinforcement learning. The effect of smooth speed, dynamic obstacle avoidance and reaching the target point was achieved. Note that this project was launched in October 2019, and the model for one set of parameters is shown here.



## 安装环境

### Ubuntu 安装

Ubuntu 16.04，默认 python2.7。参考教程：

 [**windows10 安装 ubuntu 双系统教程（绝对史上最详细）**](https://www.cnblogs.com/masbay/p/10745170.html?from=singlemessage&isappinstalled=0) 

注意：

1. 一定要明确电脑是 UEFI 还是传统 bios。它们的 U 盘制作启动模式和挂载点种

类都有区别。

2. 可以直接自己手动分区，用“扩展卷”和“压缩卷”来操作。

3. 注意分区大小。如果空间够的话，可留 140G：home 88G,efi 2G, / 40G, swap

10G。

4. 装好后，easybcd 的引导作用不一定有效，这时需要手动选择要进入的系统。

5. 也可以把 Ubuntu 装在移动硬盘上，实现即插即用。

但是要注意，当换一个电脑使用的时候，可能会出现黑屏的 **missing operating** 

**system**。这时要先拔出硬盘，长按关机键，再重新开机了。然后需要同时插入硬

盘和作为安装向导的 u 盘，进入 u 盘里的 Ubuntu 试用版，一定要联网后再把 grub 加上。

否则会报错：

**“Cannot add PPA: 'ppa:yannubuntu/boot-repair'. error:'~yannubuntu' user or te”** 

参考：[Ubuntu 14.04 引导修复（Boot Repair）（双系统修复一）](https://blog.csdn.net/piaocoder/article/details/50589667) 



### Tensorflow 安装

该项目安装的是 CPU 版。参考：

[ubuntu 16.04 安装 Tensorflow (CPU 和 GPU)](https://blog.csdn.net/qust1508060414/article/details/81138629) 

如需安装 GPU 版，参考 [清华大学开源软件镜像站](https://blog.csdn.net/qust1508060414/article/details/81138629) 。



注意：

1. 如果遇到无法获得锁 /var/lib/dpkg/lock - open (11: 资源暂时不可用)的问题，
   说明有进程没有结束： [解决办法](https://blog.csdn.net/qq_38019633/article/details/84024309) 。

2. 如果测试时报错，可以先关闭所有终端，再来测试，往往能够解决。

3. 下载可能会很慢，出现 timeout 之类的提示，多试几次就好。

4. 一定要安装 1.1 或以上版本，否则运行程序时，会有 TypeError: unsupported
    operand type(s) for -: ‘int’ and ‘NoneType’的报错。

  

### ROS 安装

参考： [中国大学 MOOC———《机器人操作系统入门》讲义-安装 ROS](https://sychaichangkun.gitbooks.io/ros-tutorial-icourse163/content/chapter1/1.4.html)



### 包的安装

因为是 python2.7 所以用的是 pip，而不是 pip3。

**sudo pip install matplotlib**

**sudo pip install numpy**

**sudo pip install scipy**

安装 cv2：参考该[教程](https://www.cnblogs.com/wmr95/p/7567999.html)。



### 其他安装问题

运行：**ctrl+alt+t** 打开终端。打开多个终端，分别输入 **roscore** 等代码。**cd** 进入文件路径。



**AttributeError: 'module' object has no attribute 'global_variables_initializer'** 

**解决方法：** 

运行代码中如果出现这个问题，原因是 tensorflow 更新了。将 **tf.global_variables_initializer()**更改为 **tf.initialize_all_variables()** 即可解决问题。





## 使用说明

### 训练

1. 开始训练前，在 dueling_6000 文件夹中新建一个名为 data 的空文件夹。

2. Alt+ctrl+T 打开终端，输入 **roscore**

3. Alt+ctrl+T  打开另一个终端，cd 到 dueling_6000 所存放的路径，输入

**rosrun stage_ros stageros ./dueling_6000/worlds/Obstacles1.world**

4. 在 dueling_6000 文件夹下打开终端，输入

**python FS-DDQN.py**

5. 可以输入如下命令

**tensorboard --logdir=./dueling_6000**

在浏览器中输入得到的网址，查看训练情况。当 loss 与 max_Q 数值相对稳定时，可以认为训练完成，键盘 ctrl+Z 停止，ctrl+C 结束。



### 测试

1. 开始测试前，在 dueling_6000 文件夹中新建一个名为 data_test 的空文件夹。

2. 更换 Obstacles1.world 中的训练地图 Obstacles1.jpg 为测试地图 Obstacles2.jpg 或 

Obstacles3.jpg；且更换 StageWorld.py 中的图片为 Obstacles2.jpg 或 Obstacles3.jpg。

3. 执行训练中的第 1、2 步骤。

4. 在 dueling_6000 文件夹下打开终端，输入

**python FS-DDQN-test.py**

5. 当用蓝色表示的机器人结束十个回合，每回合 20 次的导航后，程序自动停止。该测试会

生成 figure1，figure2……figure10 来表示不同回合的速度情况。

6. 每个回合的平均速度波动以及目标达到率将显示于终端上。

   

### 读取速度图像

#### 对于训练

1. 开始训练前，在 dueling_6000 文件夹下新建一个名为 picture_train

的空文件夹。

2. 在 dueling_6000 文件夹下打开终端，输入

**python readnpy.py**

#### 对于测试

1. 开始训练前，在dueling_6000 文件夹下新建一个名为 picture_test 的

空文件夹。

2. 在相应目录下的 dueling_6000 文件夹下打开终端，输入

**python readnpy_test.py**

得到最后一个回合的 20 次速度图。

