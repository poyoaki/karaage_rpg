import pygame as pg, sys, time, os, random

import data
import util


battle_txt = "[1]たたかう [2]まほう [3]アイテム [4]にげる"

"""
バトルのルール（仮）
先攻を決める
20面ダイス+修正値を振り、相手のACより小さい数字なら当たる。
ダメージ計算は武器や敵の属性により変わる。
dmg_mul*randrange(dmg_roll)のダメージを相手のHPから引く。
"""

# 敵のパラメーターコピー用（複数の敵にするときはリストにする）
mon = 0
mon_name = ''
mon_hp = 0
mon_ac = 0
mon_dmg_mul = 0
mon_dmg_roll = 0
mon_exp = 0
battle_end = False
mon_money = 0

magic_flag = False
battle_flag = True

def effect():
    for i in range(5):
        x_offset = random.randint(-8, 8)
        util.disp_battle_chr(mon, 0, x_offset)
        pg.time.Clock().tick(10)
        pg.display.update()

def battle_start(monster):
    global mon, mon_name,mon_hp,mon_ac,mon_dmg_mul,mon_dmg_roll,mon_exp, battle_end, mon_money
    print("battle_start( %s )" %(monster))
    # 敵を決定する
    mon = monster
    mon_name = data.monster_db[mon]['name']
    mon_hp = data.monster_db[mon]['hp']
    mon_ac = data.monster_db[mon]['ac']
    mon_exp = data.monster_db[mon]['exp']
    mon_money = data.monster_db[mon]['money']
    mon_dmg_mul = data.monster_db[mon]['dmg_mul']
    mon_dmg_roll = data.monster_db[mon]['dmg_roll']
    battle_end = False
    util.battle_start_effect()
    util.write_text("%sが あらわれた！" %(mon_name))
    util.write_text(" ")
    util.write_text(battle_txt)
    util.write_text(" ")
    util.disp_battle_chr(mon, 0, 0)
    util.disp_status()
    util.switch_to_battle()

                
def battle_win():
    global g_mode,mon_exp,my_x,my_y, battle_end, mon_money

    util.write_text("戦いに 勝利した")
    data.my_exp += mon_exp
    util.write_text("%dの経験値と%d円を得た" %(mon_exp, mon_money))

    # レベルアップ処理
    level_up_check()

    battle_end = True



def battle_lose():
    global battle_end
    util.write_text("戦いに まけてしまった!")
    util.write_text("死ぬ処理まだつくってない")
    util.write_text(" ")
    util.wait_for_spc_key()
    battle_end = True
    
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

# たたかう    
def battle_fight():
    global mon, mon_name,mon_hp,mon_ac,mon_dmg_mul,mon_dmg_roll,my_buki_name

    # とりあえず、先攻はプレイヤー（後で、dex+乱数の比較などに変えるとよい）
    util.write_text(data.my_chr_name+"は"+data.my_buki_name+"で攻撃した")
    hit = False
    damage = 0
    # ダメージ計算はDungeons&Dragons, Wizardryと同じ。適当
    bairitu = random.randrange(0,200)
    bairitu *= 0.01
    ransuu = random.randrange(0,100)

    if ransuu > 20:
        hit = True
    if hit:
        damage = random
        # 適当エフェクト
        for i in range(5):
            x_offset = random.randint(-8, 8)
            util.disp_battle_chr(mon, 0, x_offset)
            pg.time.Clock().tick(10)
            pg.display.update()
        util.write_text("%dのダメージをあたえた" %(damage))
        util.write_text(" ")
    else:
        util.write_text("しかし あたらなかった")
        util.write_text(" ")

    mon_hp -= damage
    if mon_hp <= 0:
        battle_win()
        return
    
    # wait
    for i in range(10):
        pg.time.Clock().tick(10)

    util.write_text(mon_name+"の攻撃")
    hit = False
    d20 = random.randrange(1,20)
    bairitu = random.randrange(0,200)
    bairitu *= 0.01
    ransuu = random.randrange(0,100)
    if d20 < data.my_ac:
        hit = True
    if hit:
        damage = mon_dmg_mul*random.randrange(1,mon_dmg_roll)

        # 適当エフェクト
        for cnt in range(6):
            x_offset = random.randint(-8, 8)
            y_offset = random.randint(-8, 8)
            util.update_write(x_offset, y_offset)
            #time.sleep(0.2)
            pg.time.Clock().tick(10)
            pg.display.update()

        util.write_text("%dのダメージ!" %(damage))
        util.write_text(" ")
    else:
        util.write_text("しかし あたらなかった")
        util.write_text(" ")

    data.my_hp -= damage
    if data.my_hp < 0:
        battle_lose()
    else:
        util.write_text(battle_txt)
        util.write_text(" ")

def magic():
    util.write_text("[1]おがみばし [2]かみばし [3]せせりばし [4]たたきばし [5]ねぶりばし")
    util.write_text("[6]ふりばし [7]まよいばし [8]よせばし [9]わたしばし")
    util.write_text("[10]ちぎりばし [↓]もどる")
    util.write_text(" ")

    #無限に打てるのはバランスが崩壊するのでMP('m'ajic cho'p'sticks)制を導入予定
    #おかん攻撃は強すぎるのでレベルアップによるMP増加では届かないMP消費量にし、特殊ルートでの使用解禁を想定
    while True():
        key = pg.key.get_pressed()
        if magic_flag == True:
            if (key[pg.K_1]):
                kaminokibunn = random.randrange(0,100)
                util.write_text("おがみばし 攻撃！") #これはランダム効果にしたい
                util.write_text("わりばしは 神におがんだ")
                if 0<=kaminokibunn<=33:
                    util.write_text("神は 三回攻撃を避けることを 許した！")
                elif 34 <= kaminokibunn <=66:
                    util.write_text("神は 傷を癒やした！")
                    
                elif 67 <= kaminokibunn <= 99:
                    util.write_text("神は 面倒臭がった・・・")
            
            elif (key[pg.K_2]):
                util.write_text("かみばし 攻撃！")
                util.write_text("わりばしは 相手を噛んだ")
                mon_hp = mon_hp // 2
                effect()
        
            elif (key[pg.K_3]):
                util.write_text("せせりばし 攻撃！")
                util.write_text("わりばしは 敵の鳩尾を つついた")
                mon_hp -= 100
                util.write_text("大ダメージ！")
                for i in range(5):
                    x_offset = random.randint(-15, 15)
                    util.disp_battle_chr(mon, 0, x_offset)
                    pg.time.Clock().tick(10)
                    pg.display.update()
                util.write_text("  人人人人人人人人人人人人人人人人人人人")
                util.write_text("＞よい子も 悪い子も マネしないでください＜")
                util.write_text("  Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y")
        
            elif (key[pg.K_4]):
                util.write_text("たたきばし 攻撃！")
                util.write_text("叩いた！")
                effect()
                mon_hp -= 25
                util.write_text("おや...")
                util.write_text("叩いた音で 悪霊が呼び出された！")
                util.write_text("悪霊は" "を攻撃した！")
                mon_hp -= 75
                effect()
        
            elif (key[pg.K_5]):
                util.write_text("ねぶりばし 攻撃！")
                util.write_text("わりばしは " + data.my_buki_name + "を 舐めた")
                util.write_text("敵は怖気づき 攻撃力が弱まった！")

            elif (key[pg.K_6]):
                util.write_text("ふりばし 攻撃！")
                util.write_text("ふりだしに戻り")
                util.write_text("この場にいる全員の傷が 無に帰った！")
                    
            elif (key[pg.K_7]):
                util.write_text("まよいばし 攻撃！")
                util.write_text("わりばしは あちらこちらへと動き回り")
                util.write_text("敵を切り刻んだ")
                mon_hp -= 50
                for i in range(10):
                    x_offset = random.randint(-3, 3)
                    util.disp_battle_chr(mon, 0, x_offset)
                    pg.time.Clock().tick(10)
                    pg.display.update()

            elif (key[pg.K_8]):
                util.write_text("よせばし 攻撃！")
                util.write_text("わりばしは" "を寄せた後")
                util.write_text("を投げ飛ばした！")
                mon_hp -= 70
                effect()

            elif (key[pg.K_9]):
                util.write_text("わたしばし 攻撃！")
                util.write_text("わりばしは 爆弾を渡した")
                util.write_text("大爆発！！！")
                mon_hp -= 200
                for i in range(5):
                    x_offset = random.randint(-20, 20)
                    util.disp_battle_chr(mon, 0, x_offset)
                    pg.time.Clock().tick(10)
                    pg.display.update()

        #この技は命中率5%～10%想定
            elif (key[pg.K_0]):
                util.write_text("ちぎりばし 攻撃！")
                util.write_text("わりばしは 相手を引き千切った！")
                util.write_text("必殺ダメージ！")
                mon_hp -= mon_hp
                for i in range(5):
                    x_offset = random.randint(-3, 3)
                    util.disp_battle_chr(mon, 0, x_offset)
                    pg.time.Clock().tick(10)
                    pg.display.update()
                    
        if (key[pg.K_DOWN]):
            break
            magic_flag = False

def item():
    util.write_text("アイテムを 選べ")
    util.write_text(" ")
    a = 0
    util.clear_status_box()
    util.write_status("1", a+0)
    util.write_status("2", a+1)
    util.write_status("3", a+2)
    util.write_status("4", a+3)
    util.write_status("5", a+4)
    util.write_status("6", a+5)
    util.write_status("7", a+6)
    util.write_status("8", a+7)
    util.write_status("0 閉じる", a+8)

#逃げる
def nigeru():
    nigeru_count = random.randint(0, 100)
    if (nigeru_count > 20):
        util.write_text(" ")
        util.write_text("逃げ切ることが できた")
        battle_end = True
        for i in range(10):
            pg.time.Clock().tick(10)
        util.clear_text()
        util.back_to_field()
    else:
        util.write_text("逃げ切ることは できなかった")
        util.write_text(" ")


# 戦闘画面のメインルーチン
def battle_main():
    global battle_end
    key = pg.key.get_pressed()

    if (battle_end == True):
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.clear_text()
            # フィールド画面に戻る
            util.back_to_field()

    else:
        if (key[pg.K_1]):
            # たたかう
            battle_fight()
        elif (key[pg.K_2]):
            # まほう
            magic_flag = True
            while True:
                magic()
            magic_flag = False
        elif (key[pg.K_3]):
            # アイテム
            item()
        elif (key[pg.K_4]):
            # にげる
            nigeru()


def encount1():
    # 確率で敵と遭遇させる
    rnd = random.randint(0, 100)
    if (rnd < 10): #10%
        # どの敵が出たか決める
        # 初期位置から離れるほど強い敵を出す？
        enemy = random.randint(0, data.monster_num-1)
        
        battle_start(enemy)


def level_up_check():
    print("level up mada dekitenai")
    pass