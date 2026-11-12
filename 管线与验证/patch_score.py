# -*- coding: utf-8 -*-
"""速览目检补漏：赛前叙事已抽象，但结算比分牌 / 梗向播报 / 分享卡仍写「BLG 2:3 GEN」当模拟赛果。
把这三处也切到抽象代号，并明确标「平行宇宙模拟 · 非真实赛果」；
押注单 rows 与逐项核对仍保留现实选项，保证可复核。"""
import sys
F = '/data/workspace/哈士喵决赛押宝夜AVG.html'
h = open(F, encoding='utf-8').read()

O_SCORE = """'<div class="score-line"><span class="b">BLG</span><span class="v">'+R.score+'</span><span class="r">GEN</span></div></div>';"""
N_SCORE = """'<div class="score-line"><span class="b">'+(R.demo?ABS_NAME.blue:'BLG')+'</span><span class="v">'+R.score+'</span><span class="r">'+(R.demo?ABS_NAME.red:'GEN')+'</span></div>'+(R.demo?'<div class="rate" style="margin-top:5px">平行宇宙模拟比分 · 非 11.15 真实赛果</div>':'')+'</div>';"""

O_QUOTE = """  '<br>冠军：<b>'+TEAM[R.champion]+'</b>，一血 <b>'+SHORT[R.firstblood]+'</b>，龙坑 <b>'+(R.dragonflip==='nobody'?'无人翻盘':SHORT[R.dragonflip]+' 大翻盘')+'</b>。<br>数据来源：<b>'+(R.demo?'模拟推演（真实赛果未产生）':'官方赛程快照')+'</b>。</div>';"""
N_QUOTE = """  '<br>'+(R.demo
     ?'平行宇宙冠军：<b>'+absSide(R.champion)+'</b>（对应押注单 '+TEAM[R.champion]+' 一侧），一血 <b>'+absSide(R.firstblood)+'</b>，龙坑 <b>'+(R.dragonflip==='nobody'?ABS_NAME.nobody:absSide(R.dragonflip)+' 大翻盘')+'</b>。'
     :'冠军：<b>'+TEAM[R.champion]+'</b>，一血 <b>'+SHORT[R.firstblood]+'</b>，龙坑 <b>'+(R.dragonflip==='nobody'?'无人翻盘':SHORT[R.dragonflip]+' 大翻盘')+'</b>。')+
     '<br>数据来源：<b>'+(R.demo?'模拟推演（真实赛果未产生）':'官方赛程快照')+'</b>。</div>';"""

O_CARD_L = """  x.fillStyle='#35b6ff';x.font='900 30px "PingFang SC",sans-serif';x.fillText('BLG',W/2-172,486);"""
N_CARD_L = """  var lName=R.demo?ABS_NAME.blue:'BLG',rName=R.demo?ABS_NAME.red:'GEN',teamFs=R.demo?21:30;
  x.fillStyle='#35b6ff';x.font='900 '+teamFs+'px "PingFang SC",sans-serif';x.fillText(lName,W/2-172,486);"""
O_CARD_R = """  x.fillStyle='#ff5d6c';x.font='900 30px "PingFang SC",sans-serif';x.fillText('GEN',W/2+172,486);"""
N_CARD_R = """  x.fillStyle='#ff5d6c';x.font='900 '+teamFs+'px "PingFang SC",sans-serif';x.fillText(rName,W/2+172,486);"""

O_INFO = """两种战报不改押注规则与结算公式。</p>'+"""
N_INFO = """结算比分牌与分享卡在赛前也改用抽象代号并标注「平行宇宙模拟」，只有押注单与逐项核对保留现实选项以便复核。两种战报不改押注规则与结算公式。</p>'+"""

for name, o, n in [('结算比分牌',O_SCORE,N_SCORE),('结算梗向播报',O_QUOTE,N_QUOTE),
                   ('分享卡左队',O_CARD_L,N_CARD_L),('分享卡右队',O_CARD_R,N_CARD_R),
                   ('说明页补注',O_INFO,N_INFO)]:
    c = h.count(o)
    if c != 1:
        print('MISMATCH', name, c); sys.exit(1)
    h = h.replace(o, n, 1)
open(F, 'w', encoding='utf-8').write(h)
print('OK | KB', len(h.encode())//1024,
      '| 抽象比分牌', '平行宇宙模拟比分' in h,
      '| 抽象冠军播报', '平行宇宙冠军' in h,
      '| 分享卡变量', 'teamFs' in h)
