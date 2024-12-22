import pygame as pg, sys, time, os, random

import data,util,karaage_main,time

def talk_start():

    gbloa = util.get_box_left_on_alignment
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(util.talk_bg_left, util.talk_bg_top, util.talk_bg_width, util.talk_bg_height))
    fork_big = pg.transform.scale(data.fork_img, (250, 250))
    fork_width,fork_height = fork_big.get_size()
    karaage_main.screen.blit(fork_big, (gbloa(util.screen_x,fork_width),gbloa(util.screen_y,fork_height)))

    """
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(0,300, 1920, 400))
    fork_big = pg.transform.scale(data.fork_img, (250, 250))
    karaage_main.screen.blit(fork_big, (1000,300))
    """
    pg.display.update()

    util.write_text("(スペースキーか、エンターキーを押して、会話を進めましょう。)")

burststop=False
t1=False
yn=False
t2=False
t3=False
t4=False
h1=False
admis=False
t5=False
t6=False
t7=False
t8=False
t9=False
tesc=False

#フォークとの会話

def talk_main():
    global burststop,yn,t1,t2,t3,t4,h1,admis,t5,t6,t7,t8,t9,tesc
    key = pg.key.get_pressed()
    if burststop == True:
        burststop=False
        return
    if (key[pg.K_SPACE] or key[pg.K_RETURN]) and t1 == False:
        util.write_text("やあ、君は" + " " + "はし" + " " + "かな?")
        util.write_text("(もしそうなら" + " " + "Y" + " " + "を、そうでないなら" + " " + "N" + " " + "を押してください)")
        t1=True
    elif t1 == True and yn == False:
        if (key[pg.K_y]):
            util.write_text("やっぱり。そうだと思ったんだ。")
            yn=True
        elif (key[pg.K_n]):
            util.write_text("隠しても無駄だよ。僕には分かる。")
            yn=True
    elif yn == True and t2 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("僕はビザンツ帝国から来たフォ・オクさ。")
            t2=True
            burststop=True
    elif t2 == True and t3 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("君は元から来たようだね。まさか、")
            t3=True
            burststop=True
    elif t3 == True and t4 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("君もあの「伝説の唐揚げ」について知っているのかい？")
            t4=True
            burststop=True
    elif t4 == True and h1 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("　　" + "ごまかそうか？" + "　" + "認めようか？")
            util.write_text("　" + "(ごまかすなら" + " " + "G" + " " + "を、認めるなら" + " " + "M" + " " + "を押してください)")
            h1=True
    elif h1 == True and admis == False:
        if (key[pg.K_g]):
            util.write_text("ほう？" + "　" + "とぼけるつもりか。まあいい。")
            admis=True
        elif (key[pg.K_m]):
            util.write_text("やっぱり。僕の慧眼に狂いはない。")
            admis=True
    elif admis == True and t5 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("ただ、「伝説の唐揚げ」は僕のものだ。")
            t5=True
            burststop=True
    elif t5 == True and t6 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("僕が必ず持ち帰り、帝国で英雄として、名をとどろかせるのだ！")
            t6=True
            burststop=True
    elif t6 == True and t7 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("邪魔はしないでくれ。そうしてくれれば、僕も何もしない。")
            t7=True
            burststop=True
    elif t7 == True and t8 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("　　　" + "邪魔なんかしたら、")
            t8=True
            burststop=True
    elif t8 == True and t9 == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("どうなるか分かってるよな。")
            t9=True
            burststop=True
    elif t9 == True and tesc == False:
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.write_text("おっと、少し喋りすぎたようだね。それじゃあ、サヨウナラ")
            util.write_text("(Escキーを押して会話を終了させて、町に行ってみましょう)")
            tesc=True

    elif (key[pg.K_ESCAPE]):
        util.clear_text()
        util.back_to_field()
        burststop=False
        t1=False
        yn=False
        t2=False
        t3=False
        t4=False
        h1=False
        admis=False
        t5=False
        t6=False
        t7=False
        t8=False
        t9=False
        tesc=False

        data.fd_map[10][12] = 0
