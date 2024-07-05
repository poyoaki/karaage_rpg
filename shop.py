import pygame as pg, sys, time, os, random

import data
import util
import karaage_main

shop_txt = "[1]かう [2]うる [3]ごねる [4]ぬすむ [0]みせをでる"

#0:店に入った 1:店を出る 2:買物中 3:売るものを選択中
shop_mode = 0

# 入った店の番号 保存用
shop = 0

buy_max = 0
buy_list = []

# 店のキャラなどを書く
def disp_shop_chr(shop_num):
    if (shop_num > len(data.shop_db)):
        print("try to disp undefined shop")
        return
        
    pg.draw.rect(karaage_main.screen, (0,0,0), pg.Rect(0,300, 1920, 400))
    karaage_main.screen.blit(data.shop_db[shop_num]['img'], (800,300))
    pg.display.update()


def shop_start(shop_no):
    global shop_mode, shop
    print("shop_start( %s )" %(shop_no))
    shop = shop_no
    shop_mode = 0
    util.battle_start_effect()
    util.write_text(data.shop_db[shop]['welcome_msg'])
    disp_shop_chr(shop)
    util.write_text(shop_txt)
    util.clear_status_box()

def shop_buy():
    global shop_mode, buy_max, buy_list
    db = data.shop_db[shop]['shouhin_db']
    
    buy_list.clear()
    #print("item len %d" %(len(db)))
    for i in range(len(db)):
        for j in range(len(data.item_db)):
            if (db[i] == data.item_db[j]['num']):
                buy_list.append(data.item_db[j])

    for i in range(len(buy_list)):
        #print("item %d" %(i))
        #print("name %s" %(buy_list[i]['name']))
        #print("price %d" %(buy_list[i]['price']))
        txt = '%d %s %d円' % (i+1, buy_list[i]['name'], buy_list[i]['price'])
        util.write_status(txt, i)
    buy_max = i
    util.write_status("0 やっぱやめ", i+1)
    shop_mode = 2
    util.write_text("どれを かうかい？([0]-[%d])" %(buy_max+1))
                
def shop_exit():
    global shop_mode
    util.write_text("また おこしください")
    shop_mode = 1

# 店のメインルーチン
def shop_main():
    global shop_mode, buy_item
    key = pg.key.get_pressed()

    if (shop_mode == 1):
        # でる
        print('1')
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.clear_text()
            # フィールド画面に戻る
            util.back_to_field()
    elif (shop_mode == 2):
        print('2')
        # かう
        buy_item = -1
        if (key[pg.K_0]):
            util.write_text("どうしますか？")
            util.write_text(shop_txt)
            shop_mode = 0
        if (key[pg.K_1]):
            buy_item = 0
        elif (key[pg.K_2]):
            buy_item = 1
        elif (key[pg.K_3]):
            buy_item = 2
        elif (key[pg.K_4]):
            buy_item = 3
        elif (key[pg.K_5]):
            buy_item = 4
        elif (key[pg.K_6]):
            buy_item = 5
        elif (key[pg.K_7]):
            buy_item = 6
        elif (key[pg.K_8]):
            buy_item = 7
        elif (key[pg.K_9]):
            buy_item = 8
        
        if (buy_item >= buy_max or buy_item <= 0):
            print('p')
            pass
        else:
            db = data.shop_db[shop]['shouhin_db']
            if (data.my_money >= buy_item[i]['price']):
                data.my_money -= buy_item[i]['price']
                util.write_text("%sは%d円です まいど！" % (i+1, buy_item[i]['name'], buy_item[i]['price']), i)
            else:
                util.write_text("お金がたりないよっ")

            util.write_text("どうしますか？")
            util.write_text(shop_txt)
            shop_mode = 0

    elif (shop_mode == 3):
        # うる
        if (key[pg.K_0]):
            util.write_text("どうしますか？")
            util.write_text(shop_txt)
    else:
        print('else')
        if (key[pg.K_0]):
            # 出る
            util.write_text("0:みせを でる")
            shop_exit()
        if (key[pg.K_1]):
            # うる
            util.write_text("1:かう")
            shop_buy()
        if (key[pg.K_2]):
            # うる
            util.write_text("2:うる")
            util.write_text("かいとりはまだつくってない！")
            util.write_text(shop_txt)
        elif (key[pg.K_3]):
            # ごねる
            util.write_text("3:ごねる")
            util.write_text("あー こらこら")
            util.write_text(shop_txt)
        elif (key[pg.K_4]):
            # ぬすむ
            util.write_text("4:ぬすむ")
            util.write_text("ポリスをよぶぞ")
            util.write_text(shop_txt)


