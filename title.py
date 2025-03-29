
import pygame as pg, sys, time, os, random
import util
import data
import battle
import shop
import talk
import karaage_main
dpath = os.path.dirname(__file__)+"/"

#選択肢 選択したときに実行する関数
def start_game():
    print("はじめから 選択 @title")
    util.back_to_field()

def continue_game():
    print("つづきから 選択 @title")
    #Todo セーブ ロード機能 つくる

def open_settings():
    print("設定 選択 @title")
    #Todo 設定画面 つくる

def title_main():
    #タイトル画面での選択肢
    #TODO タイトル画面でクリックしただけでも、進行するように
    choices=(
        #タイトル画面での表示名, y座標の相対位置
        #相対位置…0 → 一番上, 0.5→上下の半分, 1→一番下  にテキストが存在
        ("1 はじめから",0.5),
        ("2 つづきから",0.65),
        ("3 設定",     0.8)
    )
    #フォント
    titlefont=     pg.font.Font(dpath+"font/ipaexg.ttf",200)
    menufont =     pg.font.Font(dpath+"font/ipaexg.ttf", 100)
    menufont_bold =pg.font.Font(dpath+"font/ipaexg.ttf", 100)
    menufont_bold.set_bold(True)
    screen=karaage_main.screen
    screen_x, screen_y = karaage_main.screen_x, karaage_main.screen_y
    #背景画像貼る
    title_img=data.title_img
    w,h=title_img.get_width(),title_img.get_height()
    scale=max(screen_x/w ,screen_y/h)
    title_img_resized = pg.transform.scale(title_img, (w*scale, h*scale))
    screen.blit(title_img_resized, (0,0))
    
    #上に でっかくドーンとタイトル作る
    title_x = screen_x*0.5 - titlefont.size("からあげRPG")[0]//2
    title_y = screen_y*0.1

    title_text = titlefont.render("からあげRPG", True, (115,78,48),(200,230,255))
    screen.blit(title_text, (title_x,title_y))


    #真ん中 ~ 下に 選択肢 つくる
    for choice in choices:
        text, relative_y=choice
        menu_x = screen_x*0.3
        menu_y = screen_y*relative_y

        menu_text_bg = menufont_bold.render(text, True, (0,0,0))
        menu_text  = menufont.render(text, True, (255,255,255))

        screen.blit(menu_text_bg,(menu_x,menu_y))
        screen.blit(menu_text,   (menu_x,  menu_y))
    pg.display.update()
    
    while True:
        if (data.screen_sw == 0):
            break
        elif (data.screen_sw == 4):
            pass
        pg.display.update()
        pg.time.Clock().tick(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if   event.key==pg.K_1:start_game()
                elif event.key==pg.K_2:continue_game()
                elif event.key==pg.K_3:open_settings()
