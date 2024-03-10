import pygame
from check import check
from sys import exit  # 不加这行源代码也可以运行，但是Pyinstaller打包不行
from tkinter.messagebox import askyesno
from random import randint

"""读取json配置"""
settings = []
settings = check(settings)

"""初始化pygame和mixer"""
pygame.init()
pygame.mixer.init()

"""新建窗口"""
screen = pygame.display.set_mode()
pygame.display.set_caption(settings['caption'])
icon = pygame.image.load(settings['icon'])
pygame.display.set_icon(icon)

"""加载音效"""
time_sub5_sound = pygame.mixer.Sound(settings['sounds']['time_sub5'])
time_out_sound = pygame.mixer.Sound(settings['sounds']['time_out'])
gameover_sound = pygame.mixer.Sound(settings['sounds']['gameover'])

"""一堆Surface对象"""
#背景
background = pygame.Surface((1920, 1080))
background.fill((195, 195, 195))
#警察
police = pygame.image.load(settings['images']['police'])
police = pygame.transform.rotozoom(police, 0, 0.1)
#普通小偷
thief_ord = pygame.image.load(settings['images']['thief_ord'])
thief_ord = pygame.transform.rotozoom(thief_ord, 0, 0.1)
#无敌状态的小偷
thief_invin = pygame.image.load(settings['images']['thief_invin'])
thief_invin = pygame.transform.rotozoom(thief_invin, 0, 0.1)
#无敌道具
invin_box = pygame.image.load(settings['images']['invin_box'])
invin_box = pygame.transform.rotozoom(invin_box, 0, 0.15)
#金币
coin = pygame.image.load(settings['images']['coin'])
coin = pygame.transform.rotozoom(coin, 0, 0.15)

"""初始化坐标"""
#警察坐标
police_x = settings['initial_pos']['police'][0]
police_y = settings['initial_pos']['police'][1]
#小偷坐标
thief_x = settings['initial_pos']['thief'][0]
thief_y = settings['initial_pos']['thief'][1]
#无敌道具坐标
invin_box_pos = [randint(0, 1200), randint(0, 640)]
#金币坐标
coin_pos = [randint(0, 1200), randint(0, 640)]

"""大量变量（就说看着像不像屎山）"""
speed = settings['speed']
thief_invin_time = 0  # 小偷无敌时间
key_list = [False, False, False, False, False, False, False, False]  # 键盘事件列表（太多了，只能列表了）
gameover = False  # 游戏结束变量
game_tick = 0  # 游戏开始到现在的游戏刻
gameover_time = settings['gameover_time']  # 游戏倒计时
score = 0  # 小偷分数（也就是金币数）
invin_box_catched = False  # 无敌道具是否被拾取
invin_box_show_time = 0  # 无敌道具还有多久可以显示
coin_catched = False  # 金币是否被拾取
coin_show_time = 0  # 金币还有多久可以显示
gameover_sound_playing = False  # 游戏结束音乐是否已经在播放

"""显示字符的函数"""
def display_time():
    """显示离时间耗尽的时长"""
    font = pygame.font.Font(settings['font'], 30)
    text_gameover = font.render('游戏超时倒计时：%i秒'%gameover_time, True, (255, 255, 0))
    screen.blit(text_gameover, (0, 0))


def display_score():
    """显示小偷获得的金币数"""
    font = pygame.font.Font(settings['font'], 30)
    text_score = font.render('小偷分数：%i分'%score, True, (255, 255, 0))
    screen.blit(text_score, (400, 0))
    text_rule = font.render('小偷得到%i分，就会胜利！'%settings['win_score'], True, (255, 255, 0))
    screen.blit(text_rule, (900, 0))


def display_exit():
    """显示退出游戏提示"""
    font = pygame.font.Font(settings['font'], 20)
    if gameover:
        color = (255, 0, 0)  # 游戏结束时字体是红色的
    else:
        color = (255, 255, 255)  # 游戏进行时字体是白色的，防止过于吸引玩家注意力
    text_score = font.render('按"Esc"键退出游戏', True, color)
    screen.blit(text_score, (0, 687))

"""游戏主循环"""
game_clock = pygame.time.Clock()
while True:
    """事件遍历for循环（别看了，全是按键）"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                """退出游戏（没错，是Esc，没用Alt+F4）"""
                if not gameover:  # 如果游戏没结束，就弹提示
                    if not askyesno('退出游戏', '游戏还未结束，确定要退出游戏吗？'):
                        continue
                pygame.quit()
                exit()
            elif event.key == pygame.K_F2:  # 我有一个问题，为啥K_w一类的没用？
                key_list[0] = True
            elif event.key == pygame.K_2:
                key_list[1] = True
            elif event.key == pygame.K_1:
                key_list[2] = True
            elif event.key == pygame.K_3:
                key_list[3] = True
            elif event.key == pygame.K_UP:
                key_list[4] = True
            elif event.key == pygame.K_DOWN:
                key_list[5] = True
            elif event.key == pygame.K_LEFT:
                key_list[6] = True
            elif event.key == pygame.K_RIGHT:
                key_list[7] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F2:
                key_list[0] = False
            elif event.key == pygame.K_2:
                key_list[1] = False
            elif event.key == pygame.K_1:
                key_list[2] = False
            elif event.key == pygame.K_3:
                key_list[3] = False
            elif event.key == pygame.K_UP:
                key_list[4] = False
            elif event.key == pygame.K_DOWN:
                key_list[5] = False
            elif event.key == pygame.K_LEFT:
                key_list[6] = False
            elif event.key == pygame.K_RIGHT:
                key_list[7] = False
    
    """移动部分，我测了好久才让这小方块子不跑到屏幕外头去"""
    if not gameover:
        if key_list[0] and police_y >= settings['border']['up']:
            police_y -= speed
        if key_list[1] and police_y <= settings['border']['down']:
            police_y += speed
        if key_list[2] and police_x >= settings['border']['left']:
            police_x -= speed
        if key_list[3] and police_x <= settings['border']['right']:
            police_x += speed
        if key_list[4] and thief_y >= settings['border']['up']:
            thief_y -= speed
        if key_list[5] and thief_y <= settings['border']['down']:
            thief_y += speed
        if key_list[6] and thief_x >= settings['border']['left']:
            thief_x -= speed
        if key_list[7] and thief_x <= settings['border']['right']:
            thief_x += speed
    
    """如果小偷还有无敌时间，就使用无敌Surface对象，否则用普通对象"""
    if thief_invin_time >= 1:
        thief = thief_invin
    else:
        thief = thief_ord
    
    """显示道具和金币"""
    if invin_box_show_time == 0:
        invin_box_pos = [randint(0, 1200), randint(0, 640)]
        invin_box_show_time = -1  # 设为-1以防止多次闪

    if coin_show_time == 0:
        coin_pos = [randint(0, 1200), randint(0, 640)]
        coin_show_time = -1  # 设为-1以防止多次闪
    
    """碰撞检测Rect对象创建（我不知道咋检测Surface对象碰撞，只能用Rect了）"""
    police_rect = pygame.Rect(police_x, police_y, police.get_width(), police.get_height())
    thief_rect = pygame.Rect(thief_x, thief_y, thief.get_width(), thief.get_height())
    # 在show_time<=0的时候，将Rect对象移到对应的位置，否则移到(100000,100000)的位置（这个位置不可能到达）
    if coin_show_time <= 0:
        coin_rect = pygame.Rect(coin_pos[0], coin_pos[1], coin.get_width(), coin.get_height())
    else:
        coin_rect.move_ip(100000, 100000)
    if invin_box_show_time <= 0:
        invin_box_rect = pygame.Rect(invin_box_pos[0], invin_box_pos[1], invin_box.get_width(), invin_box.get_height())
    else:
        invin_box_rect.move_ip(100000, 100000)
    
    """Surface对象显示"""
    screen.blit(background, (0, 0))
    screen.blit(thief, (thief_x, thief_y))
    screen.blit(police, (police_x, police_y))
    if coin_show_time <= 0:
        screen.blit(coin, tuple(coin_pos))
    if invin_box_show_time <= 0:
        screen.blit(invin_box, tuple(invin_box_pos))
    
    """文字对象显示"""
    display_time()
    display_score()
    display_exit()

    """检测Rect对象之间的碰撞"""
    # 无敌道具
    if police_rect.colliderect(invin_box_rect):
        invin_box_catched = True
    if thief_rect.colliderect(invin_box_rect):
        invin_box_catched = True
        thief_invin_time = settings['invin_time']
    # 金币
    if police_rect.colliderect(coin_rect):
        coin_catched = True
    if thief_rect.colliderect(coin_rect):
        coin_catched = True
        score += settings['bonus']
    # 抓住小偷
    if police_rect.colliderect(thief_rect):
        if thief_invin_time <= 0:  # 如果小偷不是无敌的，就算抓住小偷
            font = pygame.font.Font(settings['font'], 200)
            text_gameover = font.render('警察获胜!', True, (255, 0, 0))
            screen.blit(text_gameover, (200, 250))
            gameover = True
            if not gameover_sound_playing:
                gameover_sound.play()
                gameover_sound_playing = True
    
    """非玩家对象的显示计时"""
    if invin_box_catched:  # 无敌道具
        invin_box_show_time = settings['show_time']['invin_box']
        invin_box_catched = False

    if coin_catched:  # 金币
        coin_show_time = settings['show_time']['coin']
        coin_catched = False
    
    """小偷获胜检测"""
    if score >= settings['win_score']:
        font = pygame.font.Font(settings['font'], 200)
        text_gameover = font.render('小偷获胜!', True, (255, 0, 0))
        screen.blit(text_gameover, (200, 250))
        gameover = True
        if not gameover_sound_playing:
            gameover_sound.play()
            gameover_sound_playing = True

    """游戏计时部分"""
    game_tick += 1
    if gameover_time == 0:  # 如果没时间了，就算平局
        font = pygame.font.Font(settings['font'], 200)
        text_gameover = font.render('平局结束!', True, (255, 0, 0))
        screen.blit(text_gameover, (200, 250))
        gameover = True
        if not gameover_sound_playing:
            gameover_sound.play()
            gameover_sound_playing = True
    
    if game_tick % settings['game_tick'] == 0 and not (gameover):  # tick换算
        gameover_time -= 1
        if gameover_time == 0:
            time_out_sound.play()
        elif gameover_time <= 5:
            time_sub5_sound.play()
        thief_invin_time -= 1
        invin_box_show_time -= 1
        coin_show_time -= 1
    
    game_clock.tick(settings['game_tick'])  # 设置tick
    pygame.display.update()  # 更新屏幕
