from enum import Enum


class Stage(str, Enum):
    scorch_gorge = "ユノハナ大渓谷"
    eeltail_alley = "ゴンズイ地区"
    hagglefish_market = "ヤガラ市場"
    undertow_spillway = "マテガイ放水路"
    mincemeat_metalworks = "ナメロウ金属"
    mahi_mahi_resort = "マヒマヒリゾート＆スパ"
    museum_dalfonsino = "キンメダイ美術館"
    inkblot_art_academy = "海女美術大学"
    mako_mart = "ザトウマーケット"
    wahoo_world = "スメーシーワールド"
    flounder_heights = "ヒラメが丘団地"
    brinerwater_springs = "クサヤ温泉"
    umami_ruins = "ナンプラー遺跡"
    manta_maria = "マンタマリア号"
    barnacle_and_dime = "タラポートショッピングパーク"
    humpback_pump_track = "コンブトラック"
    crableg_capital = "タカアシ経済特区"
    shipshape_cargo_co = "オヒョウ海運"
    robo_rom_en = "バイガイ亭"
    bluefin_depot = "ネギトロ炭鉱"


class Mode(str, Enum):
    regular_battle = "レギュラーマッチ"
    anarchy_battle_series = "バンカラマッチ（チャレンジ）"
    anarchy_battle_open = "バンカラマッチ（オープン）"
    x_battle = "Xマッチ"


class Rule(str, Enum):
    turf_war = "ナワバリバトル"
    splat_zones = "ガチエリア"
    tower_control = "ガチヤグラ"
    rainmaker = "ガチホコバトル"
    clam_blitz = "ガチアサリ"


class Result(str, Enum):
    win = "勝ち"
    lose = "負け"


class WinCount(Enum):
    w3 = "3勝"
    w3l1 = "3勝1敗"
    w3l2 = "3勝2敗"
    w2l3 = "2勝3敗"
    w1l3 = "1勝3敗"
    l3 = "3敗"
