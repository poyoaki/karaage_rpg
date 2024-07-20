import pygame as pg, sys, time, os, random
import util
import data
import battle
import shop



# 画像などは同じフォルダに置く
dpath = os.path.dirname(__file__)+"/"
pg.init()

screen_x = 1920
screen_y = 1080
#screen = pg.display.set_mode((screen_x, screen_y),pg.FULLSCREEN)
screen = pg.display.set_mode((screen_x, screen_y))

pg.display.set_caption("からあげ(仮)")


def main():
    
    while True:

        if (data.screen_sw == 0):
            field_main()
        elif (data.screen_sw == 1):
            battle.battle_main()
        elif (data.screen_sw == 3):
            shop.shop_main()

        pg.display.update()
        #pg.time.Clock().tick(60)
        pg.time.Clock().tick(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()



"""
フィールドの描画、キー入力など
"""
# Global フィールドの表示開始位置を保存、共有用
dispx = 0
dispy = 0

# フィールド画面と自キャラを書く
def update_field():
    global dispx, dispy

    #マップのロード
    map = data.field_db[data.now_field]
    fd_map_size_y = len(map)
    fd_map_size_x = len(map[0])

    #描画開始の座標を考える
    dispx = data.my_x-int(data.map_disp_size_x/2)
    dispy = data.my_y-int(data.map_disp_size_y/2)
    if (dispx < 0):
        dispx = 0
    elif (dispx + data.map_disp_size_x > fd_map_size_x):
        dispx = fd_map_size_x - data.map_disp_size_x

    if (dispy < 0):
        dispy = 0
    elif (dispy + data.map_disp_size_y > fd_map_size_y):
        dispy = fd_map_size_y - data.map_disp_size_y

    #print(dispx, dispy)

    # 地面描画
    for i in range(0, data.map_disp_size_x, 1):
        for j in range(0, data.map_disp_size_y, 1):
            image=data.fd_obj_db[map[dispy+j][dispx+i]]['img']
            screen.blit(image, (16+i*90, 40+j*90))
    #自分を描画
    screen.blit(data.my_chr_db[data.my_chr]['img'], (16+(data.my_x-dispx)*90, 40+(data.my_y-dispy)*90))

    pg.display.update()

my_x_bak=0
my_y_bak=0

# フィールド画面のメインルーチン
def field_main():
    global my_x_bak, my_y_bak
    #マップのロード
    map = data.field_db[data.now_field]

    moved = False
    key = pg.key.get_pressed()

    if (key[pg.K_RIGHT]):
        if (data.fd_obj_db[map[data.my_y][data.my_x+1]]['walk']):
            data.my_x += 1
            moved = True
    if (key[pg.K_LEFT]):
        if (data.fd_obj_db[map[data.my_y][data.my_x-1]]['walk']):
            data.my_x -= 1
            moved = True
    if (key[pg.K_UP]):
        if (data.fd_obj_db[map[data.my_y-1][data.my_x]]['walk']):
            data.my_y -= 1
            moved = True
    if (key[pg.K_DOWN]):
        if (data.fd_obj_db[map[data.my_y+1][data.my_x]]['walk']):
            data.my_y += 1
            moved = True

    update_field()    

    # 移動先の場所に応じてイベントを実行する
    if (moved):
        # event = data.fd_obj_db[data.fd_map[data.my_y][data.my_x]]['event']
        event = data.fd_obj_db[map[data.my_y][data.my_x]]['event']
        if (event != None):
            # 敵とのエンカウント
            if (event == data.ENCOUNT1):
                battle.encount1()

            if (event == data.ENCOUNT2):
                # 敵の遭遇率を上げるなど?
                pass
            
            if (event == data.CITY1):            
                print("町1に入る")
                my_x_bak = data.my_x
                my_y_bak = data.my_y
                data.now_field = 1
                data.my_x = 4
                data.my_y = 4
                util.map_switch_effect()

            if (event == data.EXIT_CITY):            
                print("町1から出る")
                data.my_x = my_x_bak
                data.my_y = my_y_bak
                data.now_field = 0
                util.map_switch_effect()


            if (event == data.CITY2):
                pass

            if (event == data.KARAAGEYA):
                shop.shop_start(0)
                util.switch_to_shop()


def encount1():
    pass


if __name__ == "__main__":
    main()
