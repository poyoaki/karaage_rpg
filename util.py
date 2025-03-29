import pygame as pg, sys, time, os, random

import data, karaage_main
dpath = os.path.dirname(__file__)+"/"
"""
テキストの描画
clear_txt: 文字表示枠の初期化
write_txt：1行単位で文字を描画可能
文字サイズは42x42
6行 27文字 が表示エリア
"""
txt_buf = ["", "", "", "", "", ""]
txt_line = 0

"""
is_desktop_FullHD: デスクトップの画面が1920x1080表示に対応しているか(bool)

txt_letter_size  : テキストボックス内の文字の大きさ(int)
txt_padding_y    : テキストボックスの内側と文字の、縦の余白(float)
txt_box_left     : テキストボックスの内側の、左上の角のx座標(float)
txt_box_top      : テキストボックスの内側の、左上の角のy座標(float)
txt_box_width    : テキストボックスの内側の、幅  (x方向の大きさ)(float)
txt_box_height   : テキストボックスの内側の、高さ(y方向の大きさ)(float)

status_letter_size  : ステータスメッセージ内の文字の大きさ(int)
status_padding_y    : ステータスメッセージの内側と文字の、縦の余白(float)
status_box_left     : ステータスメッセージの内側の、左上の角のx座標(float)
status_box_top      : ステータスメッセージの内側の、左上の角のy座標(float)
status_box_width    : ステータスメッセージの内側の、幅  (x方向の大きさ)(float)
status_box_height   : ステータスメッセージの内側の、高さ(y方向の大きさ)(float)

talk_bg_left        :キャラ登場時の、背景の黒幕の左上の角のx座標(float)
talk_bg_top         :キャラ登場時の、背景の黒幕の左上の角のy座標(float)
talk_bg_width       :キャラ登場時の、背景の黒幕の幅  (x方向の大きさ)(float)
talk_bg_height      :キャラ登場時の、背景の黒幕の高さ(y方向の大きさ)(float)
"""
is_desktop_FullHD=karaage_main.is_desktop_FullHD
if is_desktop_FullHD:
    txt_letter_size=42
    txt_padding_y=20
    txt_box_left, txt_box_top, txt_box_width, txt_box_height=0, 730, 1560, 300

    status_letter_size=42
    status_padding_y=20
    status_box_left, status_box_top, status_box_width, status_box_height=1210, 310, 700, 380

    talk_bg_left, talk_bg_top, talk_bg_width, talk_bg_height=0, 300, 1920, 400
    screen_x, screen_y=1920,1080

else:
    txt_letter_size=28
    txt_padding_y=10
    txt_box_left, txt_box_top, txt_box_width, txt_box_height=0, 500, 1040, 200

    status_letter_size=28
    status_padding_y=10
    status_box_left, status_box_top, status_box_width, status_box_height=800, 150, 400, 300

    talk_bg_left, talk_bg_top, talk_bg_width, talk_bg_height=0, 240, 1280, 300

    screen_x, screen_y=1280,720

# 画面の大きさ、テキストボックスの幅を指定すると、
# テキストボックスを中央ぞろえにしたときの、テキストボックスの左端の座標が分かる。
def get_box_left_on_alignment(screen_x,txt_box_width,alignment="center"):
    if   alignment=="center":
        return (screen_x-txt_box_width)/2
    elif alignment=="right":
        return screen_x-((screen_x-txt_box_width)/2)
    elif alignment=="left":
        return 0

# テキスト欄を書く
def clear_text_box(x_offset, y_offset):
    global screen
    if (abs(x_offset) > 10):
        x_offset = 0
    if (abs(y_offset) > 10):
        y_offset = 0
    pg.draw.rect(karaage_main.screen, (0,0,0),       pg.Rect(txt_box_left,                                                txt_box_top,           screen_x,        320))
    pg.draw.rect(karaage_main.screen, (255,255,255), pg.Rect(get_box_left_on_alignment(screen_x,txt_box_width)-8+x_offset,txt_box_top-8+y_offset,txt_box_width+16,txt_box_height+16))
    pg.draw.rect(karaage_main.screen, (0,0,0),       pg.Rect(get_box_left_on_alignment(screen_x,txt_box_width)+x_offset,  txt_box_top+y_offset,  txt_box_width,   txt_box_height))
    print(get_box_left_on_alignment(screen_x,txt_box_width))
    pg.display.update()

# テキスト欄をクリア
def clear_text():
    global txt_line, txt_buf
    txt_line = 0
    txt_buf = ["", "", "", "", "", ""]
    clear_text_box(0,0)

# 1行をテキスト欄に書く
def write_text(txt):
    global txt_line, txt_buf
    font = pg.font.Font(dpath+"font/ipaexg.ttf", txt_letter_size)
    if (txt_line <= 5):
        txt_buf[txt_line] = txt
        txt_line += 1
    else:
        for i in range(0, 5):
            txt_buf[i] = txt_buf[i+1]
        txt_buf[5] = txt
    clear_text_box(0,0)
    for i in range(0, 6):
        if len(txt_buf[i]) > 0:
            text = font.render(txt_buf[i], True, pg.Color("white"))
            karaage_main.screen.blit(text, (get_box_left_on_alignment(screen_x,txt_box_width)+10, txt_box_top+txt_padding_y+txt_letter_size*i+4*i))
            pg.display.update()

# テキスト欄の再描画（微妙な位置ずらしつき）
def update_write(x_offset, y_offset):
    global txt_line, txt_buf
    font = pg.font.Font(dpath+"font/ipaexg.ttf", txt_letter_size)
    clear_text_box(x_offset, y_offset)
    for i in range(0, 6):
        if len(txt_buf[i]) > 0:
            text = font.render(txt_buf[i], True, pg.Color("white"))
            karaage_main.screen.blit(text, (190+x_offset, 750+txt_letter_size*i+4*i+y_offset))
            pg.display.update()

# ステータス欄を書く(枠のみ、中身消去)
def clear_status_box():
    pg.draw.rect(karaage_main.screen, (255,255,255), pg.Rect(status_box_left-10,status_box_top-10, status_box_width+20, status_box_height+20))
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(status_box_left,   status_box_top,    status_box_width,    status_box_height))
    pg.display.update()

# ステータスのline行に書く(16x9文字まで)
def write_status(txt, line):
    if (line > 8):
        print("write_status line err %d" % (line))
        return
    font = pg.font.Font(dpath+"font/ipaexg.ttf", status_letter_size)
    text = font.render(txt, True, pg.Color("white"))
    karaage_main.screen.blit(text, (status_box_left+5, status_box_top+status_padding_y+status_letter_size*line))
    pg.display.update()


# 戦闘用画面の敵キャラなどを書く
def disp_battle_chr(monster_num, position, hosei):
    if (monster_num > data.monster_num):
        print("定義されていない敵を表示しようとしている")
        return
    # positionは未実装（複数の敵キャラを画面に出すときにつかう）
    #print("disp_battle_chr(%d)" %(monster_num))
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(0,get_box_left_on_alignment(screen_y,400), screen_x, 400))
    karaage_main.screen.blit(data.monster_db[monster_num]['img'], (900+hosei,300))
    pg.display.update()

def back_to_field():
    data.screen_sw = 0

def switch_to_battle():
    data.screen_sw = 1

def switch_to_shop():
    data.screen_sw = 3

def switch_to_talk():
    data.screen_sw = 5

def disp_status():
    pass

def battle_start_effect():
    karaage_main.screen.fill((0,0,0))

def map_switch_effect():
    karaage_main.screen.fill((0,0,0))
    for i in range(10):
        pg.time.Clock().tick(10)
        pg.display.update()
