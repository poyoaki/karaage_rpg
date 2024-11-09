global monster_num, monster_db
global sougen_img, yama_img, umi_img, machi_img, iwayama_img, mori_img
global map_size_x, map_size_y, map_elem_x, map_elem_y , fd_map, my_x, my_y, my_chr, screen_sw


import pygame as pg, os
from karaage_main import is_desktop_FullHD

map_disp_size_x, map_disp_size_y = 21, 11
if is_desktop_FullHD:
    # 表示されるフィールドは21ｘ11のます（90x90の画像をならべる）
    map_disp_size_x = 21
    map_disp_size_y = 11
else:
    # 表示されるフィールドは14ｘ8のます（90x90の画像をならべる）
    map_disp_size_x = 14
    map_disp_size_y = 8

dpath = os.path.dirname(__file__)+"/"
#dpath = ""



# 画像のロードを行う
sougen_img = pg.image.load(dpath+"sougen.png")
yama_img = pg.image.load(dpath+"yama.png")
umi_img = pg.image.load(dpath+"umi.png")
machi_img = pg.image.load(dpath+"machi.png")
iwayama_img = pg.image.load(dpath+"iwayama.png")
mori_img = pg.image.load(dpath+"mori.png")
waribashi_img = pg.image.load(dpath+"waribashi.png")
karaageya_img = pg.image.load(dpath+"karaageya.png")
kabe_img = pg.image.load(dpath+"kabe.png")
fork_img = pg.image.load(dpath+"fork.png")


# 画面切り替え 0=field, 1=battle, 2=status, 3=からあげや, 4=title, 5=talk
screen_sw = 0

# 表示されるフィールドは21ｘ11のます（90x90の画像をならべる）
map_disp_size_x = 21
map_disp_size_y = 11

# フィールドのイベント
# Noneだとなにもなし(敵も出ない)
ENCOUNT1 = 1
ENCOUNT2 = 2
CITY1=10
CITY2=11
EXIT_CITY = 13
KARAAGEYA = 20
RIVAL = 30

"""フィールドの構造
0 ... 草原
1 ... 山
2 ... 海
3 ... 森
4 ... 岩山
5 ... 町1
6 ... 町2
7 ... 町の中の草原（敵は出ない）
8 ... 町1のからあげ屋
9 ... カベ
10 ... 町1から出る

11 ... フォーク
以下
"""
fd_obj_db = [
    {'num':0, 'walk':True, 'img':sougen_img, 'event':ENCOUNT1},    
    {'num':1, 'walk':True, 'img':yama_img, 'event':ENCOUNT1},
    {'num':2, 'walk':False, 'img':umi_img, 'event':None},
    {'num':3, 'walk':True, 'img':mori_img, 'event':ENCOUNT1},
    {'num':4, 'walk':False, 'img':iwayama_img, 'event':None},
    {'num':5, 'walk':True, 'img':machi_img, 'event':CITY1},
    {'num':6, 'walk':True, 'img':machi_img, 'event':CITY2},
    {'num':7, 'walk':True, 'img':sougen_img, 'event':None},    
    {'num':8, 'walk':True, 'img':karaageya_img, 'event':KARAAGEYA},    
    {'num':9, 'walk':False, 'img':kabe_img, 'event':None},    
    {'num':10, 'walk':True, 'img':sougen_img, 'event':EXIT_CITY},
    {'num':11, 'walk':True, 'img':fork_img, 'event':RIVAL}
]
fd_objs = 6

# マップ配列
# 21ｘ11以上のサイズが必要

# 最初のフィールド
fd_map = [
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,0,0,0,0,0,0,0,1,1,1,1,4,4,1,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,0,0,0,0,0,0,0,1,1,1,2,2,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2],    
    [2,2,0,0,0,0,0,0,0,1,1,1,2,2,2,2,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2], 
    [2,2,0,0,0,0,0,0,0,3,3,1,2,2,2,2,1,3,3,0,0,0,0,0,0,0,0,0,0,2,2], 
    [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,0,0,0,0,0,0,0,0,0,0,11,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
]

# さいしょの町のマップ
city1_map = [
    [9,9,9,9,9,9,9,10,9,9,9,9,9,9,9,9,9,9,9,9,9],
    [9,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,9],
    [9,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,9],
    [9,7,7,7,7,7,7,7,7,7,7,7,7,7,7,8,7,7,7,7,9],
    [9,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,9],
    [9,7,7,7,7,7,7,7,7,7,7,2,2,7,7,7,7,7,7,7,9],
    [9,7,7,7,7,7,7,7,7,7,7,2,2,7,7,7,7,7,7,7,9],
    [9,7,7,7,7,7,7,7,7,7,7,2,2,7,7,7,7,7,7,7,9],
    [9,7,7,7,7,7,7,7,7,7,7,2,2,7,7,7,7,7,7,7,9],
    [9,7,7,7,7,7,7,7,7,7,7,2,2,7,7,7,7,7,7,7,9],
    [9,9,9,9,9,9,9,9,9,9,10,9,9,9,9,9,9,9,9,9,9]
]


now_field = 0
# フィールドを追加したらここに追加していく
field_db = [fd_map, city1_map]


"""
マイキャラ
0 わりばし
以下
"""
my_chr_db = [
    {'num': 0, 'name':"わりばし", 'ini_hp':20, 'img':waribashi_img},
]

my_chr = 0

"""
敵キャラの設定 ウィザードリィ風
hp:耐久力
ac:アーマークラス 大きいほどプレイヤーの攻撃が当たりやすいので弱い。最大20最小1
dex:すばやさ 大きいほどすばやい。逃げやすく攻撃も当たりやすい
dmg_mul ダメージ倍率
dmg_roll ダメージの乱数範囲
exp:経験値
プレイヤーに与えるダメージはdmg_mul*乱数（1～dmg_roll)となる
防具の堅さは未実装
クリティカルヒットも未実装
"""

# 敵の画像
slime_img = pg.image.load(dpath+"slime.png")
gob_img = pg.image.load(dpath+"goblin.png")

monster_num = 2
monster_db = [
    {'name':"なんか青い", 'hp':4, 'ac':19, 'dex':1, 'dmg_mul':1, 'dmg_roll':2, 'exp':10, 'money':30, 'img':slime_img},
    {'name':"なんか緑", 'hp':8, 'ac':18, 'dex':1, 'dmg_mul':1, 'dmg_roll':4, 'exp':15, 'money':60, 'img':gob_img},
]

buki_db = [
    {'name':"おてもとの袋", 'dmg_mul':1, 'dmg_roll':6},
    {'name':"木のささくれ", 'dmg_mul':1, 'dmg_roll':8}
]

bougu_db = [
    {'name':"すっぱだか", 'ac':10},
    {'name':"安いおはしケース", 'ac':9}
]

# 店員の画像
tenin1_img = pg.image.load(dpath+"slime.png")

# アイテム一覧
HEAL1 = 10
HEAL2 = 11
HEAL3 = 12

item_db = [
    {'num':0, 'name':"からあげ（小）", 'price':100, 'func': HEAL1},
    {'num':1, 'name':"からあげ（中）", 'price':150, 'func': HEAL2},
    {'num':2, 'name':"からあげ串（でかい）", 'price':400, 'func': HEAL3},
]

shop_num = 1
shouhin_db1 = [0, 1] #からあげや

shop_db = [
    {'name':"からあげや", 'welcome_msg':"たどりついた からあげや", 'shouhin_db':shouhin_db1, 'img':tenin1_img} ,
]


# 自分のステータス
# セーブロードを実装したら、ここの値を更新すると良い
my_hp = 30
my_mp = 10
my_exp = 0
my_money = 1000
my_buki_name = buki_db[0]['name']
my_bougu_name = bougu_db[0]['name']
my_ac = bougu_db[0]['ac']
my_dmg_mul = buki_db[0]['dmg_mul']
my_dmg_roll = buki_db[0]['dmg_roll']
my_chr_name = my_chr_db[my_chr]['name']
my_item_list = []

#自分がいる場所（map上）
my_x = 4
my_y = 4

def my_item_append(item):
    global my_item_list
    if (len(my_item_list) > 8):
        return -1
    else:
        my_item_list.append(item)
        return 0
    
#こんにちわ
#テストです
#あー
#akabeko