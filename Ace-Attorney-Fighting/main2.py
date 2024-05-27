import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#创建游戏窗口
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width , screen_height))
pygame.display.set_caption("逆转，然后格斗")

#限制帧率
clock = pygame.time.Clock()
FPS = 60

menu_image = pygame.image.load("assets/images/mainmenu/menu.png")
button_image = pygame.image.load("assets/images/mainmenu/New Game.png")
button2_image = pygame.image.load("assets/images/mainmenu/Exit Game.png")


start_music = pygame.mixer.Sound("assets/audio/按钮2.mp3")
exit_music = pygame.mixer.Sound("assets/audio/按钮2.mp3")

start_button = pygame.Rect(430, 360, 150, 26)
exit_button = pygame.Rect(430, 410, 150, 26)
#定义颜色
RED=(169,0,8)
YELLOW=(255,255,0)
WHITE=(255,255,255)
BLUE=(0,44,169)

intro_count=3
last_count_update=pygame.time.get_ticks()
score=[0,0]
round_over=False
round_over_cooldown=2000

#定义精灵大小
WARRIOR_SIZE =128
WARRIOR_SCALE=3
WARRIOR_OFFSET=[45,35]
WARRIOR_DATA =[WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]
WIZARD_SIZE=128
WIZARD_SCALE=3
WIZARD_OFFSET=[45,35]
WIZARD_DATA=[WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

#音频

pygame.mixer.music.load("assets/audio/BGM.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0,5000)

attack01_fx =pygame.mixer.Sound("assets/audio/异议.mp3")
attack01_fx.set_volume(0.5)
attack02_fx=pygame.mixer.Sound("assets/audio/异议2.mp3")
attack02_fx.set_volume(0.5)

#加载背景
bg_image=pygame.image.load("assets/images/background/background01.jpg").convert_alpha()
fg_image=pygame.image.load("assets/images/background/background02.png").convert_alpha()
bg_vs=pygame.image.load("assets/images/icons/VS.png").convert_alpha()
#加载血条
hp_left_image=pygame.image.load("assets/images/icons/Hp_left.png").convert_alpha()
hp_right_image=pygame.image.load("assets/images/icons/Hp_right.png").convert_alpha()

#加载精灵表
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior2.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior3.png").convert_alpha()

victory_img = pygame.image.load("assets/images/icons/胜利提示.png").convert_alpha()

def draw_bg():
    scaled_bg= pygame.transform.scale(bg_image,(screen_width,screen_height))
    screen.blit(scaled_bg,(0,0))
    scaled_vs = pygame.transform.rotozoom(bg_vs, 0,0.2)
    screen.blit(scaled_vs, (360, -30))

def draw_fg():
    scaled_fg = pygame.transform.scale(fg_image, (screen_width, screen_height))
    screen.blit(scaled_fg, (0, 0))
#拆分Sprites
WARRIOR_ANIMATION_STEPS = [6,4,7,8,8,7,6,7]
WIZARD_ANIMATION_STEPS=[6,4,7,6,8,7,6,7]

count_font=pygame.font.Font("assets/fonts/turok.ttf",80)
score_font=pygame.font.Font("assets/fonts/turok.ttf",40)

def draw_text(text,font,text_col,x,y):
    img =font.render(text,True,text_col)
    screen.blit(img,(x,y))

#角色血量
def draw_health_bar(player,health,x,y,hp_image):
    ratio = health/100
    #pygame.draw.rect(screen, WHITE, (x-2, y-2, 404, 34))

    #pygame.draw.rect(screen,YELLOW,(x,y,400*ratio,30))
    scaled_hp=pygame.transform.rotozoom(hp_image,0,0.2)
    screen.blit(scaled_hp,(x-45,y-80))
    if player == 1:
        pygame.draw.rect(screen, BLUE, (x+90, y+30, 310*ratio, 38))
    else:
        pygame.draw.rect(screen, RED, (x, y + 30, 310*ratio, 38))


#创建两个战士实例
fighter_01 = Fighter(1,230,350,False,WARRIOR_DATA,warrior_sheet,WARRIOR_ANIMATION_STEPS,attack01_fx)
fighter_02 = Fighter(2,600,350,True,WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,attack02_fx)


#游戏循环
run = True
while run:
    screen.fill((0, 0, 0))

    # 绘制菜单主图片
    screen.blit(menu_image, (0, 0))

    # 绘制按钮
    pygame.draw.rect(screen, (0, 100, 0), start_button)
    pygame.draw.rect(screen, (100, 0, 0), exit_button)

    screen.blit(menu_image, (0, 0))
    # 绘制开始游戏按钮
    button_image = pygame.transform.scale(button_image, (start_button.width, start_button.height))
    button2_image = pygame.transform.scale(button2_image, (exit_button.width, exit_button.height))
    screen.blit(button_image, start_button.topleft)
    # 绘制退出游戏按钮
    screen.blit(button2_image, exit_button.topleft)
    pygame.display.update()
    pygame.draw.rect(screen, (100, 0, 0), start_button)
    pygame.draw.rect(screen, (100, 0, 0), exit_button)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1表示左键点击
                # 获取鼠标点击的位置
                mouse_pos = event.pos
                # 检查是否点击了"开始游戏"按钮
                if start_button.collidepoint(mouse_pos):
                    print("开始游戏")
                    start_music.play()  # 播放开始游戏的音乐
                    pygame.mixer.music.load("assets/audio/杉森雅和 - 尋問 ～アレグロ 2001.mp3")
                    pygame.mixer.music.play(-1, 0.0, 5000)
                    running = True
                    run = False
                # 检查是否点击了"退出游戏"按钮
                elif exit_button.collidepoint(mouse_pos):
                    print("退出游戏")
                    exit_music.play()  # 播放退出游戏的音乐
                    pygame.quit()
                    running = False
                    run=False


    clock.tick(FPS)

running = True
while running:
    clock.tick(FPS)
    #绘制背景
    draw_bg()
    #绘制角色状态
    draw_health_bar(1,fighter_01.health, 20, 20,hp_left_image)
    draw_health_bar(2,fighter_02.health, 580, 20,hp_right_image)

    draw_text("P1:"+str(score[0]),score_font,YELLOW,110,10)
    draw_text("P2:" + str(score[1]), score_font, YELLOW, 580, 10)

    if intro_count <= 0:
        #角色移动
        fighter_01.move(screen_width,screen_height,screen,fighter_02,round_over)
        fighter_02.move(screen_width, screen_height, screen, fighter_01,round_over)
    else:
        draw_text(str(intro_count),count_font,WHITE,screen_width/2,screen_height/3)

        if(pygame.time.get_ticks()-last_count_update)>=1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
        print(intro_count)
    #fighter_02.move(screen_width)
    fighter_01.update()
    fighter_02.update()
    #绘制战士
    fighter_01.draw(screen)
    fighter_02.draw(screen)

    draw_fg()

    if round_over ==False:
        if fighter_01.alive ==False:
            score[1]+=1
            round_over=True
            round_over_time=pygame.time.get_ticks()
        elif fighter_02.alive ==False:
            score[0]+=1
            round_over=True
            round_over_time=pygame.time.get_ticks()
    else:
        scaled_win = pygame.transform.rotozoom(victory_img, 0, 0.2)
        screen.blit(scaled_win, (360, -30))
        if pygame.time.get_ticks() - round_over_time>round_over_cooldown:
            round_over=False
            intro_count=3
            fighter_01 = Fighter(1, 230, 350, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,attack01_fx)
            fighter_02 = Fighter(2, 600, 350, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS,attack02_fx)

            draw_fg()

            if score[1]==1 or score[0]==1:
                pygame.mixer.music.load("assets/audio/杉森雅和 - 成歩堂龍一 ～異議あり! 2001.mp3")
                pygame.mixer.music.play(-1, 0.0, 5000)
            if score[1]==2 or score[0]==2:
                pygame.mixer.music.load("assets/audio/杉森雅和 - 追求 ～追いつめられて.mp3")
                pygame.mixer.music.play(-1, 0.0, 5000)

    for event in pygame.event.get():
     if event.type == pygame.QUIT:
         pygame.quit()
         run = False

    pygame.display.update()

#退出游戏
pygame.quit()