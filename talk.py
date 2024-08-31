import pygame as pg, sys, time, os, random

import data
import util
import karaage_main

def talk_start():
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(0,300, 1920, 400))
    fork_big = pg.transform.scale(data.fork_img, (250, 250))
    karaage_main.screen.blit(fork_big, (1000,300))
    pg.display.update()
    util.write_text("(スペースキーか、エンターキーを押してください)")

def talk_main():
    key = pg.key.get_pressed()
    if (key[pg.K_SPACE] or key[pg.K_RETURN]):
        util.write_text("やあ、君は" + " " + "はし" + " " + "かな?")
    elif (key[pg.K_ESCAPE]):
        util.clear_text()
        util.back_to_field()

