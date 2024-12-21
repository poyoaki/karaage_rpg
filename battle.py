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


battle_flag = True
magic_mode = True

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

damage =0

# たたかう    
def battle_fight():
    global mon, mon_name,mon_hp,mon_ac,mon_dmg_mul,mon_dmg_roll,my_buki_name

    # とりあえず、先攻はプレイヤー（後で、dex+乱数の比較などに変えるとよい）
    util.write_text(data.my_chr_name+"はわりばしのおてもとで攻撃した")
    hit = False
    damage = 0
    # ダメージ計算はDungeons&Dragons, Wizardryと同じ。適当
    bairitu = random.randrange(0,200)
    bairitu *= 0.01
    ransuu = random.randrange(0,100)

    if ransuu > 20:
        hit = True
    if hit:
        damage = random.randint(1, 5)
        # 適当エフェクト
        for i in range(5):
            x_offset = random.randint(-8, 8)
            util.disp_battle_chr(mon, 0, x_offset)
            pg.time.Clock().tick(10)
            pg.display.update()
        util.write_text(str(damage)+"のダメージをあたえた")
        util.write_text(" ")
    else:
        util.write_text("しかし あたらなかった")
        util.write_text(" ")

    mon_hp -= damage
    if mon_hp <= 0:
        battle_win()
        return
    
    battle_atosyori()
    enemy_turn()
    
def enemy_turn():
    # wait
    for i in range(10):
        pg.time.Clock().tick(10)

    global ransuu
    util.write_text(mon_name+"の攻撃")
    hit = False
    d20 = random.randrange(1,20)
    bairitu = random.randrange(0,200)
    bairitu *= 0.01
    ransuu = random.randrange(0,100)
    if d20 < data.my_ac:
        bairitu = random.randrange(0,200)
        bairitu *= 0.01
        ransuu = random.randrange(0,100)
    if bairitu < data.my_ac:
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
        battle_atosyori()

#後処理系
def battle_atosyori():
    global battle_mode
    battle_mode = False
    util.write_text(" ")
    util.write_text(battle_txt)
    util.write_text(" ")

def magic_atosyori():
    global magic_mode
    magic_mode = False
    util.clear_status_box()
    util.write_text(" ")
    util.write_text(battle_txt)
    util.write_text(" ")

def item_atosyori():
    global item_mode
    item_mode = False
    util.clear_status_box()
    util.write_text(" ")
    util.write_text(battle_txt)
    util.write_text(" ")

def run_away_atosyori():
    global run_away_mode
    run_away_mode = False


#魔法記述
def magic_write():
    m = 0
    util.clear_status_box()
    util.write_status("A おがみばし", m+0)
    util.write_status("S かきばし", m+1)
    util.write_status("D すかしばし", m+2)
    util.write_status("F たたきばし", m+3)
    util.write_status("G にぎりばし", m+4)
    util.write_status("H ふりばし", m+5)
    util.write_status("J まよいばし", m+6)
    util.write_status("K さしばし", m+7)
    util.write_status("L 戻る", m+8)

#魔法
def magic():
    global magic_mode
    #無限に打てるのはバランスが崩壊するのでMP('m'ajic cho'p'sticks)制を導入予定
    #さしばしは強すぎるのでレベルアップによるMP増加では届かないMP消費量にし、特殊ルートでの使用解禁を想定
    if magic_mode:         
        keys = pg.key.get_pressed()

        #4ターンの間 攻撃力と防御力を上げる
        if (keys[pg.K_a]):
            util.write_text("いただきます 攻撃")
            magic_atosyori()
            
        #神に祈り効果を授かる(3パターン)
        elif (keys[pg.K_s]):
            util.write_text("おがみばし 攻撃！")
            magic_atosyori()

        #そのターン先行を取っていればダメージを受けない
        elif (keys[pg.K_d]):
            util.write_text("すかしばし 攻撃！")
            magic_atosyori()

        #連続攻撃
        elif (keys[pg.K_f]):
            util.write_text("かきばし 攻撃！")
            magic_atosyori()

        #相手の攻撃力と防御力を下げる
        elif (keys[pg.K_g]):
            util.write_text("にぎりばし 攻撃！")
            magic_atosyori()

        #自分と味方のHPを回復する
        elif (keys[pg.K_h]):
            util.write_text("おかわり 攻撃")
            magic_atosyori()

        #相手の攻撃を2ターン防げる
        elif (keys[pg.K_j]):
            util.write_text("まよいばし 攻撃！")
            magic_atosyori()

        #確率で一撃必殺
        elif (keys[pg.K_k]):
            util.write_text("ごちそうさまでした 攻撃")
            magic_atosyori()

        elif (keys[pg.K_l]):
            util.write_text("では どうする？")
            magic_atosyori()
 
#アイテム
        enemy_atosyori()

#後処理系
def battle_atosyori():
    global battle_mode
    battle_mode = False
    util.write_text(" ")

def magic_atosyori():
    global magic_mode
    magic_mode = False
    util.clear_status_box()
    util.write_text(" ")
    util.write_text(battle_txt)
    util.write_text(" ")

def item_atosyori():
    global item_mode
    item_mode = False
    util.clear_status_box()
    util.write_text(" ")
    util.write_text(battle_txt)
    util.write_text(" ")

def run_away_atosyori():
    global run_away_mode
    run_away_mode = False

def enemy_atosyori():
    util.write_text(" ")
    util.write_text(battle_txt)
    util.write_text(" ")

#魔法記述
def magic_write():
    m = 0
    util.clear_status_box()
    util.write_status("A さぐりばし", m+0)
    util.write_status("S 食らいつく", m+1)
    util.write_status("D よせばし", m+2)
    util.write_status("F ねぶりばし", m+3)
    util.write_status("G ツボをはしで押す", m+4)
    util.write_status("H ふりばし", m+5)
    util.write_status("J まよいばし", m+6)
    util.write_status("K さしばし", m+7)
    util.write_status("L 戻る", m+8)

#魔法
#効果は仮
attack_mode = False
defense_mode = False

def magic():
    global magic_mode , attack_mode , defense_mode ,meat
    if magic_mode:         
        keys = pg.key.get_pressed()

        #さぐりばし
        #攻撃しその被ダメ1/2自分の体力を回復させる
        if (keys[pg.K_a]):
            util.write_text("敵の体内を探った！")
            magic_atosyori()
            
        #食らいつく
        elif (keys[pg.K_s]):
            util.write_text("食らいつく 攻撃！")
            meat = random.randrange(1,100)
            if 1<= meat < 33:
                util.write_text("わりばしは敵の”ばら”を食った！")
                util.write_text("敵の防御力が落ちた！")
            elif 33 <= meat < 66:
                util.write_text("わりばしは敵の”かた”を食った！")
                util.write_text("敵の攻撃力が落ちた！")
            else:
                util.write_text("わりばしは敵の”たん”を食った！")
                util.write_text("敵の体力が半分減った！")

            magic_atosyori()

        #よせばし
        elif (keys[pg.K_d]):
            util.write_text("よせばし 攻撃！")
            util.write_text("敵がこちらへ寄ってきた！")
            util.write_text("クリティカルヒット！！！")
            magic_atosyori()

        #ねぶりばし
        elif (keys[pg.K_f]):
            util.write_text("ねぶりばし 攻撃！")
            util.write_text("敵を舐ってみた")
            util.write_text("敵の攻撃力は落ち 自分の防御力は上がった！")
            magic_atosyori()

        #ツボをはしで押す
        elif (keys[pg.K_g]):
            util.write_text("ツボをはしで押す 攻撃！")
      

        #自分と味方のHPを回復する
        elif (keys[pg.K_h]):
            util.write_text("おかわり")
            util.write_text("HPが 回復した！ ")
            magic_atosyori()

        #相手の攻撃を2ターン防げる
        elif (keys[pg.K_j]):
            util.write_text("まよいばし 攻撃！")
            magic_atosyori()

        #確率で一撃必殺
        elif (keys[pg.K_k]):
            util.write_text("ごちそうさまでした 攻撃")
            magic_atosyori()

        elif (keys[pg.K_l]):
            util.write_text("では どうする？")
            magic_atosyori()
 
#アイテム
def item():
    key = pg.key.get_pressed()
    #アイテムとしての機能は「item_atosyori」の手前に書く
    if (key[pg.K_q]):
        item_atosyori()

    elif (key[pg.K_w]):
        item_atosyori()

    elif (key[pg.K_e]):
        item_atosyori()

    elif (key[pg.K_r]):
        item_atosyori()

    elif (key[pg.K_t]):
        item_atosyori()

    elif (key[pg.K_y]):
        item_atosyori()

    elif (key[pg.K_u]):
        item_atosyori()

    elif (key[pg.K_i]):
        item_atosyori()

    elif (key[pg.K_o]):
        util.write_text("ならば、どうする？")
        item_atosyori()
    
#アイテム記述
def item_write():
    util.write_text("アイテムを 選べ")
    util.write_text(" ")
    a = 0
    util.clear_status_box()
    util.write_status("Q", a+0)
    util.write_status("W", a+1)
    util.write_status("E", a+2)
    util.write_status("R", a+3)
    util.write_status("T", a+4)
    util.write_status("Y", a+5)
    util.write_status("U", a+6)
    util.write_status("I", a+7)
    util.write_status("O 閉じる", a+8)

#逃げる
def run_away():
    global battle_end
    nigeru_count = random.randint(0, 100)
    if (nigeru_count > 100):
        util.write_text(" ")
        util.write_text("逃げ切ることが できた")
        battle_end = True
        for i in range(10):
            pg.time.Clock().tick(10)
        util.clear_text()
        util.back_to_field()
        run_away_atosyori()
        
    else:
        util.write_text("逃げ切ることは できなかった")
        util.write_text(" ")
        util.write_text(battle_txt)
        run_away_atosyori()
        run_away_atosyori()
        enemy_turn()

magic_mode = False
battle_mode = False
item_mode = False
run_away_mode = False

# 戦闘画面のメインルーチン
def battle_main():
    global battle_end, magic_mode,battle_mode,item_mode,run_away_mode
    key = pg.key.get_pressed()

    if (battle_end == True):
        if (key[pg.K_SPACE] or key[pg.K_RETURN]):
            util.clear_text()
            # フィールド画面に戻る
            util.back_to_field()
    elif magic_mode:
        #魔法
        magic()
    elif item_mode:
        #アイテム
        item()
    elif run_away_mode:
        #逃げる
        run_away()
    else:
        if (key[pg.K_1]):
            # たたかう
            battle_mode = True
            battle_fight()
    if battle_mode:
        #戦う
        battle_fight()
        battle_mode = False
    elif magic_mode:
        #魔法
        magic()
    elif item_mode:
        #アイテム
        item()
    elif run_away_mode:
        #逃げる
        run_away()
        run_away_mode = False
    else:
        if (key[pg.K_1]):
            battle_mode = True
        elif (key[pg.K_2]):
            magic_write()
            magic_mode = True
        elif (key[pg.K_3]):
            item_write()
            item_mode = True
        elif (key[pg.K_4]):
            run_away_mode = True


def encount1():
    # 確率で敵と遭遇させる
    rnd = random.randint(0, 100)
<<<<<<< Updated upstream
    if (rnd < 5): #5%
=======

    if (rnd < 5): # 敵の出現確率%
>>>>>>> Stashed changes
        # どの敵が出たか決める
        # 初期位置から離れるほど強い敵を出す？
        enemy = random.randint(0, data.monster_num-1)
        
        battle_start(enemy)

def level_up_check():
    print("level up mada dekitenai")
    pass
