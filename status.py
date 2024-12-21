import pygame as pg, sys, time, os, random
import data
import util

import karaage_main


#0:通常 1:ステータス表示中1
status_mode = 0

#ステータスの何番目の画面か？
status_page = 0



def status_start():
    global status_mode, status_page
    util.clear_status_box()    
    util.write_status(data.my_chr_name,0)
    util.write_status("レベル："+str(data.my_level),1)
    util.write_status("HP："+str(data.my_hp)+"/"+str(data.my_hp_max),2)
    util.write_status("MP："+str(data.my_mp)+"/"+str(data.my_mp_max),3)
    util.write_status("武器："+data.my_buki_name,4)
    util.write_status("防具："+data.my_bougu_name,5)
    util.write_status("EXP："+str(data.my_exp),6)
    util.write_status("お金："+str(data.my_money),7)

    status_mode = 1
    status_page = 0

def disp_status_page2():
    global status_mode, status_page
    util.clear_status_box()    
    util.write_status("もちもの",0)

    for i in range(0,8):
        if data.get_my_item(i) == -1:
            util.write_status("---",i+1)
        else:
            util.write_status(data.get_my_item_name(i),i+1)

    status_mode = 1
    status_page = 1

def disp_save_load():
    global status_mode, status_page
    util.clear_status_box()    
    util.write_status("セーブ・ロード?",0)
    util.write_status("S:セーブ",1)   
    util.write_status("L:ロード",2)
    util.write_status("ENTER:やめる",3)

def disp_save_select():
    util.clear_status_box()    
    util.write_status("＊＊セーブする？＊＊",0)
    util.write_status("1:セーブデータ1",1)   
    util.write_status("2:セーブデータ2",2)
    util.write_status("ENTER:やめる",3)

def disp_load_select():
    util.clear_status_box()    
    util.write_status("＊＊ロードする？＊＊",0)
    util.write_status("1:ロードデータ1",1)   
    util.write_status("2:ロードデータ2",2)
    util.write_status("ENTER:やめる",3)

def disp_confirm():
    global file_save_mode
    util.clear_status_box()    
    util.write_status(file_no+"に"+file_save_mode+"していいですか？",0)
    util.write_status("Y:いいよ",2)   
    util.write_status("ENTER:やめる",3)

def status_exit():
    global status_mode, status_page
    status_mode = 0
    status_page = 0


file_save_mode = ""
file_no = 0
# ステータス表示のメインルーチン
def status_main():
    global status_mode, status_page, file_no, file_save_mode

    pg.event.pump()
    key = pg.key.get_pressed()

    if (status_mode == 1):
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            if status_page == 0:
                disp_status_page2()
                status_page = 1
                file_save_mode = ""
                file_no = 0
            elif status_page == 1:
                disp_save_load()
                status_page = 100
                file_save_mode = ""
                file_no = 0
            else:
                # フィールド画面に戻るのでフラグ等は下げる
                status_exit()
                file_save_mode = ""
                file_no = 0
                util.back_to_field()
        elif (key[pg.K_s]):
            # Save
            disp_save_select()
            status_page = 101
        elif (key[pg.K_l]):
            # Save
            disp_load_select()
            status_page = 102
        elif (key[pg.K_1]):
            if (status_page == 101): #save
                file_save_mode = "SAVE"
                file_no = 1
                status_page = 200
            elif (status_page == 102): #load
                file_save_mode = "LOAD"
                file_no = 1
                status_page = 200
        elif (key[pg.K_2]):
            if (status_page == 101): #save
                file_save_mode = "SAVE"
                file_no = 2
                status_page = 200
            elif (status_page == 102): #load
                file_save_mode = "LOAD"
                file_no = 2
                status_page = 200


    else:
        pass

      
