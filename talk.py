import pygame as pg, sys, time, os, random

import data
import util
import karaage_main

def talk_start():
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(0,300, 1920, 400))
    fork_big = pg.transform.scale(data.fork_img, (250, 250))
    karaage_main.screen.blit(fork_big, (1000,300))
    pg.display.update()
    util.write_text("(スペースキーか、エンターキーを押してください。)")

t1=False
yn=False

def talk_main():
    global yn,t1
    key = pg.key.get_pressed()
    if (key[pg.K_SPACE] or key[pg.K_RETURN]) and t1 == False:
        util.write_text("やあ、君は" + " " + "はし" + " " + "かな?")
        util.write_text("(もしそうなら" + " " + "Y" + " " + "を、そうでないなら" + " " + "N" + " " + "を押してください。)")
        t1=True
    elif yn == False:
        if (key[pg.K_y]):
            util.write_text("やっぱり。そうだと思ったんだ。")
            yn=True
        elif (key[pg.K_n]):
            util.write_text("隠しても無駄だよ。僕には分かる。")
            yn=True
    elif (key[pg.K_ESCAPE]):
        util.clear_text()
        util.back_to_field()
        t1=False
        yn=False

#util.write_text("僕はビザンツ帝国から来たフォ・オクさ。")
#util.write_text("君は元から来たようだね。まさか、")
#util.write_text("君もあの「伝説の唐揚げ」について知っているのかい？")
#はしの心の声　　　ごまかそうか？　それとも　認めようか？
#ごまかした場合　　ほう？　とぼけるつもりか。まあいい。
#認めた場合　　　　やっぱり。僕の慧眼に狂いはなかった。
#util.write_text("ただ、「伝説の唐揚げ」は僕のものだ。")
#util.write_text("僕が必ず持ち帰り、帝国で英雄として、名をとどろかせるのだ！")
#util.write_text("僕の邪魔はしないでくれ。そうしてくれれば、僕も何もしない。")
#util.write_text("邪魔なんてしたら、" + "　　　" + "どうなるか分かっているよな。")
#util.write_text("おっと、少し喋りすぎたようだね。それじゃあ、サヨウナラ")