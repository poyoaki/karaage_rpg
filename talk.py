import pygame as pg, sys, time, os, random
import data
import util
import karaage_main

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
    util.write_text("(スペースキーか、エンターキーを押してください)")

def talk_main():
    key = pg.key.get_pressed()
    if (key[pg.K_SPACE] or key[pg.K_RETURN]):
        util.write_text("やあ、君は" + " " + "はし" + " " + "かな?")
    elif (key[pg.K_ESCAPE]):
        util.clear_text()
        util.back_to_field()

