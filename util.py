import pygame as pg, sys, time, os, random

import data, karaage_main
dpath = os.path.dirname(__file__)+"/"
"""
テキストの描画
clear_txt: 文字表示枠の初期化
write_txt：1行単位で文字を描画可能
文字サイズは42x42
5行 27文字 が表示エリア
"""
txt_buf = ["", "", "", "", ""]
txt_line = 0

# テキスト欄を書く
def clear_text_box(x_offset, y_offset):
    global screen
    if (abs(x_offset) > 10):
        x_offset = 0
    if (abs(y_offset) > 10):
        y_offset = 0
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(0,760, 1920, 320))
    pg.draw.rect(karaage_main.screen, (255,255,255), pg.Rect(180-8+x_offset,780-8+y_offset, 1560+16, 300+16))
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(180,780, 1560, 300))
    pg.display.update()

# テキスト欄をクリア
def clear_text():
    global txt_line, txt_buf
    txt_line = 0
    txt_buf = ["", "", "", "", ""]
    clear_text_box(0,0)

# 1行をテキスト欄に書く
def write_text(txt):
    global txt_line, txt_buf
    font = pg.font.Font(dpath+"ipaexg.ttf", 42)
    if (txt_line <= 4):
        txt_buf[txt_line] = txt
        txt_line += 1
    else:
        for i in range(0, 4):
            txt_buf[i] = txt_buf[i+1]
        txt_buf[4] = txt
    clear_text_box(0,0)
    for i in range(0, 5):
        if len(txt_buf[i]) > 0:
            text = font.render(txt_buf[i], True, pg.Color("white"))
            karaage_main.screen.blit(text, (190, 780+42*i+4*i))
            pg.display.update()

# テキスト欄の再描画（微妙な位置ずらしつき）
def update_write(x_offset, y_offset):
    global txt_line, txt_buf
    font = pg.font.Font(dpath+"ipaexg.ttf", 42)
    clear_text_box(x_offset, y_offset)
    for i in range(0, 5):
        if len(txt_buf[i]) > 0:
            text = font.render(txt_buf[i], True, pg.Color("white"))
            karaage_main.screen.blit(text, (190+x_offset, 780+42*i+4*i+y_offset))
            pg.display.update()

# ステータス欄を書く(枠のみ、中身消去)
def clear_status_box():
    pg.draw.rect(karaage_main.screen, (255,255,255), pg.Rect(1200,300, 720, 400))
    pg.draw.rect(karaage_main.screen, (0,0,0),       pg.Rect(1210,310, 700, 380))
    pg.display.update()

# ステータスのline行に書く(16x9文字まで)
def write_status(txt, line):
    if (line > 8):
        print("write_status line err %d" % (line))
        return
    font = pg.font.Font(dpath+"ipaexg.ttf", 42)
    text = font.render(txt, True, pg.Color("white"))
    karaage_main.screen.blit(text, (1215, 320+42*line))
    pg.display.update()


# 戦闘用画面の敵キャラなどを書く
def disp_battle_chr(monster_num, position, hosei):
    if (monster_num > data.monster_num):
        print("定義されていない敵を表示しようとしている")
        return
    # positionは未実装（複数の敵キャラを画面に出すときにつかう）
    #print("disp_battle_chr(%d)" %(monster_num))
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(0,300, 1920, 400))
    karaage_main.screen.blit(data.monster_db[monster_num]['img'], (900+hosei,300))
    pg.display.update()

def back_to_field():
    data.screen_sw = 0

def switch_to_battle():
    data.screen_sw = 1

def switch_to_shop():
    data.screen_sw = 3

def disp_status():
    pass

def battle_start_effect():
    karaage_main.screen.fill((0,0,0))

def map_switch_effect():
    karaage_main.screen.fill((0,0,0))
    for i in range(10):
        pg.time.Clock().tick(10)
        pg.display.update()