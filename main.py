from flask import Flask, Response, render_template
from flask_caching import Cache
import uuid
import random
import collections
import json
import os
import copy
import numpy as np

app = Flask(__name__)

# Cacheインスタンスの作成
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379'),
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 2,
})

'''
キーカード(5x5)
- NGが１つ
- 赤8つ
- 青9つ
先行チームのほうが1つ多い

ターンチェンジ
- 自分のエージェント以外（はずれや相手エージェント）を選択した場合

'''

answers = [
    'かわら',
    'くじ',
    'しっぽ',
    'たいまつ',
    'つり',
    'てんぷら',
    'ねっど',
    'めざめ',
    'アイドル',
    'アステカ',
    'アトランティス',
    'アニメ',
    'アマゾン',
    'アルプス',
    'イス',
    'イヌ',
    'イモムシ',
    'インド',
    'ウェーブ',
    'ウサギ',
    'ウマ',
    'エイリアン',
    'エジプト',
    'エンジン',
    'エース',
    'オペラ',
    'オーストラリア',
    'カギ',
    'カバー',
    'カボチャ',
    'カモ',
    'カモノハシ',
    'カンガルー',
    'ガス',
    'キング',
    'ギター',
    'ギリシア',
    'クシ',
    'クマ',
    'クモ',
    'クラゲ',
    'クラッシュ',
    'クラブ',
    'クロス',
    'クール',
    'ゲーム',
    'コミック',
    'コンサート',
    'コート',
    'コード',
    'ゴースト',
    'サイクル',
    'サウンド',
    'サギ',
    'サケ',
    'サトウ',
    'サーバー',
    'シェイクスピア',
    'シャドウ',
    'シャンプー',
    'シュート',
    'ショップ',
    'シール',
    'ジェット機',
    'ジム',
    'ジャック',
    'ジャム',
    'ジャングル',
    'ジャンプ',
    'スキューバダイバー',
    'スクリーン',
    'スタジアム',
    'スタッフ',
    'ストック',
    'ストライク',
    'スナック',
    'スパイク',
    'スリップ',
    'スーツ',
    'スーパーヒーロー',
    'センター',
    'ゾンビ',
    'タイガー',
    'タップ',
    'タブレット',
    'タンス',
    'ダイス',
    'ダイヤ',
    'ダンス',
    'チャージ',
    'チョコレート',
    'チーズ',
    'ツメ',
    'ツル',
    'デッキ',
    'デート',
    'トライアングル',
    'トラック',
    'トリップ',
    'ドラゴン',
    'ドラフト',
    'ドラム',
    'ドレス',
    'ドワーフ',
    'ニンジン',
    'ネクタイ',
    'ネコ',
    'ノート',
    'ハチミツ',
    'ハム',
    'ハリウッド',
    'ハロウィン',
    'ハワイ',
    'ハンド',
    'ハート',
    'ハーフ',
    'バッテリー',
    'バット',
    'バミューダ',
    'バラ',
    'バンド',
    'バーツ',
    'バーベキュー',
    'パイプ',
    'パイロット',
    'パラシュート',
    'パン',
    'パンダ',
    'ヒマラヤ',
    'ビタミン',
    'ビッグバン',
    'ビル',
    'ピアノ',
    'ピストル',
    'ピラミッド',
    'ピース',
    'フェンス',
    'フック',
    'フランス',
    'フード',
    'ブレス',
    'ヘリコプター',
    'ベビー',
    'ベルト',
    'ベルリン',
    'ペンギン',
    'ペースト',
    'ホース',
    'ボス',
    'ボルト',
    'ボンド',
    'ボール',
    'ポイント',
    'ポップコーン',
    'ポンド',
    'マーク',
    'マーチ',
    'ミイラ',
    'ミサイル',
    'ムチ',
    'メキシコ',
    'メール',
    'モスクワ',
    'モール',
    'ライター',
    'ライン',
    'ラケット',
    'ラップ',
    'リュックサック',
    'リング',
    'リーダー',
    'ルート',
    'ルーム',
    'ルール',
    'レジェンド',
    'レモン',
    'レーザー',
    'ロケット',
    'ロック',
    'ローマ',
    'ワゴン車',
    'ワシントン',
    '京都',
    '侍',
    '億万長者',
    '兵士',
    '分',
    '列',
    '剣',
    '劇場',
    '勇者',
    '北京',
    '医者',
    '協会',
    '南極',
    '命',
    '土星',
    '壁',
    '夢',
    '天使',
    '天才',
    '太平洋',
    '宝',
    '密売人',
    '工場',
    '巨人',
    '幸運',
    '弁護士',
    '忍者',
    '戦争',
    '手袋',
    '掃除機',
    '救急車',
    '教師',
    '日記',
    '森',
    '橋',
    '歯',
    '死',
    '水星',
    '氷',
    '洗濯',
    '浜',
    '海賊',
    '港',
    '潜水艦',
    '火',
    '炭酸',
    '爆弾',
    '王冠',
    '皮',
    '看護師',
    '空気',
    '美人',
    '脳',
    '船',
    '草原',
    '葬儀屋',
    '虹',
    '象牙',
    '蹄鉄',
    '遊び',
    '野菜',
    '鉄',
    '鉄道',
    '鏡',
    '雪',
    '雪だるま',
    '霧',
    '靴下',
    '顔',
    '顕微鏡',
    '風船',
    '飛行機',
    '魔女',
    '魚',
]

@app.route('/')
def homepage():
    return render_template('index.html')


# create the game group
@app.route('/create')
@app.route('/create/<nickname>')
def create_game(nickname=''):
    game = {
        'status': 'waiting',
        'routeidx': 0,
        'stocks': list(range(2, 99)),
        'players': []}
    player = {}

    gameid = str(uuid.uuid4())
    game['gameid'] = gameid
    player['playerid'] = gameid
    player['nickname'] = nickname if nickname != '' else gameid
    player['holdcards'] = []
    game['players'].append(player)

    app.logger.debug(gameid)
    app.logger.debug(game)
    cache.set(gameid, game)
    return gameid


# re:wait the game
@app.route('/<gameid>/waiting')
def waiting_game(gameid):
    game = cache.get(gameid)
    game['status'] = 'waiting'
    cache.set(gameid, game)
    return 'reset game status'


# join the game
@app.route('/<gameid>/join')
@app.route('/<gameid>/join/<nickname>')
def join_game(gameid, nickname='default'):
    game = cache.get(gameid)
    if game['status'] == 'waiting':
        player = {}

        playerid = str(uuid.uuid4())
        player['playerid'] = playerid
        if nickname == 'default':
            player['nickname'] = playerid
        else:
            player['nickname'] = nickname
        player['holdcards'] = []
        game['players'].append(player)

        cache.set(gameid, game)
        return playerid + ' ,' + player['nickname'] + ' ,' + game['status']
    else:
        return 'Already started'


# start the game
@app.route('/<gameid>/start')
def start_game(gameid):
    game = cache.get(gameid)
    app.logger.debug(gameid)
    app.logger.debug(game)
    game['status'] = 'started'

    game['turn'] = 0
    game['board'] = []

    game['answers'] = copy.deepcopy(answers)
    random.shuffle(game['answers'])
    game['answers'] = game['answers'][:25]
    app.logger.debug(game['answers'])
    setting_answers = copy.deepcopy(game['answers'][:25])

    players = game['players']
    for player in players:
        player['teamid'] = 9

    for pos in range(25):
        board = {'codename': '', 'type': 3}
        if pos < 9:
            board['type'] = 0
        elif pos < 17:
            board['type'] = 1
        elif pos < 18:
            board['type'] = 2

        board['codename'] = setting_answers.pop(random.randint(0, len(setting_answers) - 1))
        game['board'].append(board)

    random.shuffle(game['board'])

    cache.set(gameid, game)
    return 'ok'


# set the team
@app.route('/<gameid>/<playerid>/set/<teamid>')
def set_team(gameid, playerid, teamid):
    game = cache.get(gameid)

    player = [player for player in game['players'] if player['playerid'] == playerid][0]
    player['teamid'] = teamid

    cache.set(gameid, game)
    return 'ok'


# next to team the game
@app.route('/<gameid>/next')
def next_game(gameid):
    game = cache.get(gameid)

    game['turn'] = (game['turn'] + 1) % 2

    cache.set(gameid, game)
    return 'ok'


# set the card on the line
@app.route('/<gameid>/set/<int:teamid>/<answer_inp>')
def setcard_game(gameid, teamid, answer_inp):
    game = cache.get(gameid)

    app.logger.debug(answer_inp)
    app.logger.debug(game['answers'])

    # game['answers'].pop(aIdx for (aIdx, answer) in enumerate(game['answers']) if answer == answer_inp)
    for aIdx, answer in enumerate(game['answers']):
        if answer == answer_inp:
            app.logger.debug('hit!')
            game['answers'].pop(aIdx)

    app.logger.debug(game['board'])
    answer = [answer for answer in game['board'] if answer['codename'] == answer_inp][0]
    app.logger.debug(answer)
    app.logger.debug(teamid)

    if answer['type'] != teamid:
        if answer['type'] == 3:
            answer['type'] += 10
            game['status'] = 'end'
            cache.set(gameid, game)
            return 'ng'

        answer['type'] += 10
        game['turn'] = (game['turn'] + 1) % 2

        cache.set(gameid, game)
        return 'ng'

    answer['type'] += 10

    cache.set(gameid, game)
    return 'ok'


# all status the game
@app.route('/<gameid>/status')
def game_status(gameid):
    game = cache.get(gameid)

    return json.dumps(game)


if __name__ == "__main__":
    # port = int(os.getenv("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
    app.run(debug=True)
