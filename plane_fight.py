# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 08:50:57 2018

@author: rarestzhou
@作者微信: zjc111369
"""

## 飞机大战

import pygame
import time
from pygame.locals import *
import random

'''
    3. 使用面向对象的方式显示飞机，以及控制其左右移动


    要做的任务：
    1. 实现飞机在你想要的位置显示
    2. 实现按键控制飞机移动
    3. 实现按下空格键的时候，显示一颗子弹
    4. 实现子弹击中飞机使其爆炸的效果(原理:在一定时间内换图片) --> 待实现
'''

class Base(object):
    """定义一个基类"""
    def __init__(self, screen_temp, name):
        self.screen = screen_temp
        self.name = name
        
        
class Plane(Base):
    """定义一个飞机类"""
    def __init__(self, screen_temp, name):
        super().__init__(screen_temp, name)
        self.image = pygame.image.load(self.imagePath)
        # 存储发射出去的子弹对象引用
        self.bullet_list = []
        
        self.isHit = False # 标识飞机是否爆炸
        self.blow_plane_list = [] # 用来存储爆炸的飞机
        self.__create_image() # 调用该方法向列表中添加爆炸飞机图片
        
    def __create_image(self):
        self.blow_plane_list.append(pygame.image.load("./plane/hero_blowup_n1.png"))
        self.blow_plane_list.append(pygame.image.load("./plane/hero_blowup_n2.png"))
        self.blow_plane_list.append(pygame.image.load("./plane/hero_blowup_n3.png"))
        self.blow_plane_list.append(pygame.image.load("./plane/hero_blowup_n4.png"))
        

        
    # 显示玩家飞机及其发射的子弹        
    def display(self):
        # 更新飞机的位置
        self.screen.blit(self.image, (self.x, self.y))
        
#        for bullet in self.bullet_list: # 显示并移动子弹
#            bullet.display()
#            bullet.move()
#            # 判断子弹是否越界
#            # 注：循环删除元素时会存在漏删元素(删不干净)
#            # 解决：使用一个列表保存要删除的元素，再在循环里使用原列表删除新列表中的元素
#            if bullet.judge_out_of_bound(): 
#                self.bullet_list.remove(bullet) 
        
        needDelItemList = []
        
        for del_item in self.bullet_list:
            if del_item.judge_out_of_bound():
                needDelItemList.append(del_item)
                
        for del_item in needDelItemList:
            self.bullet_list.remove(del_item)
            
        #更新及这架飞机发射出的所有子弹的位置
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()

    def fire_bullet(self):
        newBullet = BaseBullet(self.x, self.y, self.screen, self.name)
        self.bullet_list.append(newBullet)

class HeroPlane(Plane):
    """定义一个战斗机类"""
    
    # 重写__init__() 方法
    def __init__(self, screen, name):
        #设置飞机默认的位置
        self.x = 180
        self.y = 600
        self.imagePath = "./plane/hero1.png"
        super().__init__(screen, name)
                                                
    def move_left(self):
        self.x -= 10
        
    def move_right(self):
        self.x += 10

    
class EnemyPlane(Plane):
    """定义一个敌机类"""
    
    def __init__(self, screen, name):
        # 设置敌机的默认位置
        self.x = 0
        self.y = 0
        self.imagePath = "./plane/enemy-1.gif"

        # 调用父类的__init__ 方法
        super().__init__(screen, name)
                
        # 用来存储飞机默认的显示方向
        self.direction = "right" 
        
    def move(self):
        if self.direction == "right": 
            self.x += 5
        elif self.direction == "left":
            self.x -= 5
        
        if self.x > 422 - 50:  # 敌机（右侧）从向左移动到窗口右侧时，则往左继续移动
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"
        
    def fire(self):
        random_number = random.randint(1, 100)
        if random_number == 6 or random_number == 19 or random_number == 65:
            super().fire_bullet()
    

class BaseBullet(Base):
    """定义一个子弹基类"""

    def __init__(self, x, y, screen, planeName):
        super().__init__(screen, planeName)

        if self.name == "hero":
            self.x = x + 40
            self.y = y - 20
            imagePath = "./plane/bullet-3.gif"

        elif self.name == "enemy":
            self.x = x + 30
            self.y = y + 30
            imagePath = "./plane/bullet-1.gif"

        self.image = pygame.image.load(imagePath)

    def move(self):
        if self.name == "hero":
            self.y -= 6
        elif self.name == "enemy":
            self.y += 6

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


    def judge_out_of_bound(self):
        if self.y < 0 or self.y > 746:
            return True
        else:
            return False
     
    
def key_control(hero_temp):
    """获取事件，比如按键等"""
    
    for event in pygame.event.get():

        #判断是否是点击了退出按钮
        if event.type == QUIT:
            print("exit")
            exit()
                
        #判断是否是按下了键
        elif event.type == KEYDOWN:
            #检测按键是否是a或者left
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                hero_temp.move_left()

            #检测按键是否是d或者right
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                hero_temp.move_right()

            #检测按键是否是空格键
            elif event.key == K_SPACE:
                print('space')   
                hero_temp.fire_bullet()
        
'''
    1. 搭建界面，完成主要窗口和背景图(该部分代码为固定用法，后续可直接使用无需自己敲)
'''
def main():
    
    # 1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((422, 750), 0, 32) # 参数 1：窗口的宽和高，参数2和3为固定写法
    
    #2. 加载一个和窗口一样大小的图片，用来充当背景
    background = pygame.image.load("./plane/background.png")
    
    #3. 创建一个飞机对象
    hero = HeroPlane(screen, "hero")
    
    #4. 创建一个敌机对象
    enemy_plane = EnemyPlane(screen, "enemy")
    
    #5. 把背景图片放到窗口中显示
    while True:
        # 设定需要显示的背景图
        screen.blit(background, (0, 0)) # 参数1：背景，参数2：窗口的(0, 0)点坐标
        
        hero.display()
        
        enemy_plane.display()
        enemy_plane.move()  # 调用敌机的move()方法
        enemy_plane.fire()  # 敌机开火
        
        key_control(hero)

        time.sleep(0.01) # 单位：秒

        
        # 更新需要显示的内容
        pygame.display.update()
       
        
'''
    2. 显示玩家飞机，并检测(键盘)事件
'''
        
if __name__ == "__main__":
    main()


    
