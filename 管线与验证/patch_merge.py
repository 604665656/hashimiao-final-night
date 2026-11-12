# -*- coding: utf-8 -*-
"""以分层解耦版为唯一基线，合并成一版，并补「虚拟抽象战报」。
赛前（demo）走平行宇宙抽象剧本；11.15 回填真实赛果后自动切回真实口径战报。
所有锚点必须唯一，否则中止。"""
import os, sys, shutil

ROOT = '/data/workspace'
LAYER = os.path.join(ROOT, '哈士喵决赛押宝夜AVG_分层架构验证.html')
MAIN = os.path.join(ROOT, '哈士喵决赛押宝夜AVG.html')
ARCH = os.path.join(ROOT, '_merge', 'archive')
os.makedirs(ARCH, exist_ok=True)

# 归档旧两版（合并后根目录只留一个 HTML）
shutil.copy(MAIN, os.path.join(ARCH, '归档_主成品_ASSETS单表.html'))
shutil.copy(LAYER, os.path.join(ARCH, '归档_分层验证版_P_BGS.html'))
h = open(LAYER, encoding='utf-8').read()

# ---------------- 1) 版本标签标明合并单版 ----------------
O_LABEL = "var BUILD_ID='s16-final-avg-2026-11-12', BUILD_LABEL='11.12 封盘版', SCHEMA=3;"
N_LABEL = "var BUILD_ID='s16-final-avg-2026-11-12', BUILD_LABEL='11.12 封盘版 · 合并单版', SCHEMA=3;"

# ---------------- 2) CHARMAP 扩展 4 个抽象名场面槽 ----------------
O_MAP = 'var CHARMAP={"host_idle":"char_idle","host_hi":"char_hi","host_hype":"char_hype","host_fancy":"char_fancy","host_dark":"char_dark","host_shock":"char_shock","host_blade":"char_blade","host_origin":"char_origin"};'
N_MAP = ('var CHARMAP={"host_idle":"char_idle","host_hi":"char_hi","host_hype":"char_hype",'
         '"host_fancy":"char_fancy","host_dark":"char_dark","host_shock":"char_shock",'
         '"host_blade":"char_blade","host_origin":"char_origin",'
         '"host_flip":"char_flip","host_baron":"char_baron","host_quote":"char_quote","host_tbd":"char_tbd"};')

# ---------------- 3) 抽象词表 + 抽象战报生成（插在 buildFeed 之前） ----------------
O_FEED_HEAD = "function buildFeed(R){\n  var f=[];"
ABS = r"""/* ===== 虚拟抽象战报：赛前模拟推演专用，平行宇宙口径，不冒充真实赛果 ===== */
var ABS_NAME={blue:'深蓝不熬夜',red:'赤焰别上头',peace:'河道蟹本人',nobody:'谁也没翻',baron:'大龙本龙'};
var ABS_SCENE=[
 '中路摆了三分钟 pose，谁也没先动手，导播切了个空镜。',
 '有人把闪现交给了空气，空气礼貌地收下了。',
 '一波兵线引发的哲学讨论，持续了整整两分钟。',
 '龙坑里雾太大，两边隔着雾互相点头。',
 '辅助先打了个哈欠，全场跟着打了个哈欠。',
 '经济差像心率一样来回横跳，解说开始念诗。',
 '有人绕后绕到了自家泉水，理由是看看风景。',
 '灯牌忽然全亮，原因是保洁阿姨按错了开关。',
 '猫把台词本叼走了，剩下的部分靠即兴。',
 '时间暂停了一秒，用来给弹幕想梗。'
];
var ABS_QUOTE=[
 '平行宇宙嘛，别太较真。','这剧本我编的，我负责。','猫爪一挥，剧本就歪了。',
 '别记笔记，这场不算数。','抽象是对具体的一种温柔反抗。','灯牌亮着就行，比分随它去。'
];
function absSide(k){return ABS_NAME[k]||'TBD 空降';}
function absActualText(gid,R){
  return actualText(gid,R)
    .replace(/BLG/g,ABS_NAME.blue).replace(/GEN/g,ABS_NAME.red)
    .replace(/无人认领/g,ABS_NAME.peace).replace(/无人翻盘/g,ABS_NAME.nobody)
    .replace(/全场未动大龙/g,'大龙本龙全程观战');
}
function buildAbstractFeed(R){
  var f=[];
  function add(tag,cls,m,fx,t,say,tag2,no){
    f.push({who:'哈士喵',m:m,fx:fx,bg:(cls==='hot'?'bg_moon':undefined),tag:tag2||'CLOUD WATCH / 虚拟抽象战报',no:no,
      t:'<b>【'+tag+'】</b> '+t+(say?'<br><em>「'+say+'」</em>':'')});
  }
  add('喵喵开场','hot','host_tbd','pop',
    '导播把信号接进了<em>平行宇宙频道</em>：<span class="b">'+ABS_NAME.blue+'</span> 对 <span class="r">'+ABS_NAME.red+'</span>，外加随时可能空降的 <em>TBD</em>。今晚不播真实赛果，只播一份抽象剧本。',
    '喵喵模拟推演 · 与 11.15 真实赛果无关，纯属玩梗。');
  if(R.firstblood==='peace'){
    add('谁先破功','','host_shock','shake','前两分钟大家都在研究河道蟹的种族，<em>一血：'+ABS_NAME.peace+' 认领</em>。','连破功都这么客气。');
  }else{
    add('谁先破功','','host_blade','shake','开局没多久，<span class="'+(R.firstblood==='blue'?'b':'r')+'">'+absSide(R.firstblood)+'</span> 先没绷住，<em>一血归它</em>，灯牌亮了一半。',rnd(ABS_QUOTE));
  }
  var pool=[],n=R.bw+R.rw;
  for(var b=0;b<R.bw-(R.champion==='blue'?1:0);b++)pool.push('blue');
  for(var q=0;q<R.rw-(R.champion==='red'?1:0);q++)pool.push('red');
  shuffle(pool);pool.push(R.champion);
  var flipAt=1+Math.floor(Math.random()*Math.max(1,n-1)),baronAt=1+Math.floor(Math.random()*Math.max(1,n-1));
  if(baronAt===flipAt)baronAt=1+(baronAt%Math.max(1,n-1));  /* 名场面别挤同一局，避免角色差分互相覆盖 */
  for(var i=0;i<n;i++){
    var w=pool[i],m='host_idle',fx='',say=rnd(ABS_QUOTE);
    var bits=['<span class="'+(w==='blue'?'b':'r')+'">'+absSide(w)+'</span> 收下平行宇宙第 '+(i+1)+' 局'];
    if(i+1===flipAt){
      if(R.dragonflip==='nobody'){bits.push('龙坑两边隔河相望，<em>连大龙都看困了</em>');m='host_flip';}
      else{bits.push('<em>'+absSide(R.dragonflip)+' 在龙坑上演大翻盘</em>，猫把台词本撕了');m='host_flip';fx='shake';}
    }
    if(i+1===baronAt){
      if(R.baron==='baron'){bits.push('这一局谁都没摸大龙，<em>大龙本龙全程观战并打了哈欠</em>');m='host_baron';}
      else{bits.push('<em>'+absSide(R.baron)+'</em> 率先摸了一下大龙，摸完就跑');m='host_baron';}
    }
    if(Math.random()<.65)bits.push(rnd(ABS_SCENE));
    if(i===n-1){m='host_quote';fx='pop';}
    add('第'+(i+1)+'局 · 抽象',w,m,fx,bits.join('，').replace(/。+$/,'')+'。',say);
  }
  add('灯牌','hot','host_hype','',R.fullseries==='yes'
      ?'<em>打满五局</em>，灯牌打到没电，决胜局靠手电筒收尾。'
      :'<em>没打满</em>，灯牌提前收工，保洁阿姨开始收椅子。',
      R.fullseries==='yes'?'这一晚值了，虽然它不存在。':'没打满，但抽象程度满了。');
  add('喵喵终场','hot','host_dark','pop',
    '平行宇宙最终比分 <em>'+R.score+'</em>，抽象冠军 <em>'+absSide(R.champion)+'</em>（对应押注单里的 '+TEAM[R.champion]+' 一侧）。<br><em>虚拟抽象战报 · 非真实赛果、非官方预测；11.15 回填后自动切回真实战报。</em>',
    '好了，翻页吧，别拿这个去跟人打赌。');
  /* 虚拟账也逐条核对：数值照算，但明确标成平行宇宙 */
  var P=(S.locked&&S.locked.picks)||S.picks,cnt=0;
  GROUPS.forEach(function(g){
    var p=P[g.id];if(!p)return;
    var o=optById(g,p.id);if(!o)return;
    var yes=hit(g.id,p.id,R),gain=yes?Math.round(p.stake*o.o):0;
    cnt++;
    add('虚拟核对 · '+g.title,'',yes?'host_fancy':'host_shock','',
      '<b>你押</b> '+esc(o.l)+'（'+fmt(p.stake)+' 币 · x'+o.o.toFixed(2)+'） → <b>平行宇宙实际</b> '+esc(absActualText(g.id,R))+
      ' → '+(yes?'<em>命中 +'+fmt(gain)+' 币</em>':'<em>未中 −'+fmt(p.stake)+' 币</em>'),
      '模拟账也照算，别声张。','CLOUD WATCH / 虚拟核对',String(cnt));
  });
  if(cnt)add('核对完毕','hot','host_idle','','<em>'+cnt+' 项押注已逐条核对（虚拟账）</em>，下面进入结算。','翻页吧。');
  return f;
}
function buildFeed(R){
  if(R.demo)return buildAbstractFeed(R);   /* 赛前：虚拟抽象战报；赛后回填：真实口径 */
  var f=[];"""

# ---------------- 4) 结算页 quote 补抽象声明 ----------------
O_QUOTE = """  h+='<div class="quote"><div class="q">赛 后 播 报 · 哈士喵</div>'+rnd(delta>=0?WIN_Q:LOSE_Q)+'<br>'+endingLine(L)+"""
N_QUOTE = """  h+='<div class="quote"><div class="q">赛 后 播 报 · 哈士喵</div>'+rnd(delta>=0?WIN_Q:LOSE_Q)+'<br>'+endingLine(L)+
     (R.demo?'<br><em>喵喵模拟推演 · 平行宇宙抽象剧本，与 11.15 真实赛果无关，不构成预测。</em>':'')+"""

# ---------------- 5) 分享卡抽象冠军 ----------------
O_CARD = """  x.fillText('冠军 · '+TEAM[R.champion]+'　|　立场 '+(S.stance?STANCE_NAME[S.stance]:'未定'),W/2,534);"""
N_CARD = """  x.fillText((R.demo?'抽象冠军 · '+absSide(R.champion)+'（模拟）':'冠军 · '+TEAM[R.champion])+'　|　立场 '+(S.stance?STANCE_NAME[S.stance]:'未定'),W/2,534);"""

# ---------------- 6) 说明页：抽象战报 + 单版合并 ----------------
O_INFO = """  '<p><b>版本：</b><b>'+esc(versionTag())+'</b>（'+esc(BUILD_ID)+'）。模拟版与赛后真实版分开标识，旧页面不会静默切换赛果；存档带版本号，损坏时自动回退并备份。</p>'+"""
N_INFO = """  '<p><b>版本：</b><b>'+esc(versionTag())+'</b>（'+esc(BUILD_ID)+'）。模拟版与赛后真实版分开标识，旧页面不会静默切换赛果；存档带版本号，损坏时自动回退并备份。</p>'+
  '<p><b>虚拟抽象战报：</b>赛前（真实赛果未产生）开演走 <b>喵喵模拟推演 · 平行宇宙</b>——队伍用「深蓝不熬夜 / 赤焰别上头 / TBD 空降」抽象代号，一血 / 龙坑大翻盘 / 先动大龙 / 打满五局都念成梗化名场面，<b>不把模拟赛果写成真实队名</b>；逐项核对照常给分，但标成「虚拟账」。11.15 回填真实赛果后，战报自动切回 BLG / GEN 真实口径 + 官方快照。两种战报不改押注规则与结算公式。</p>'+
  '<p><b>单版合并：</b>此前「主成品」与「分层验证版」的玩法 / 数据 / 音效 / 规则完全相同，只差美术资源组织；现以分层解耦版（8 张透明角色层 × 6 张生成空场景）为唯一基线，旧两版已归档，不再双份维护。</p>'+"""

# ---------------- 7) 标题 / 押注台：战报口径提示 ----------------
O_TITLE = """  s+='<div class="title-meta">生图美术 · S16 决赛 BLG vs GEN · 11.15 03:00<br>官方赛程快照内嵌 · 页面不联网 · 11.13 封盘<br><b style="color:#e7c283">'+esc(versionTag())+'</b><br>虚拟币无现金价值 · 非官方粉丝玩梗 · 未成年人需监护人同意</div>';"""
N_TITLE = """  s+='<div class="title-meta">生图美术 · S16 决赛 BLG vs GEN · 11.15 03:00<br>官方赛程快照内嵌 · 页面不联网 · 11.13 封盘<br><b style="color:#e7c283">'+esc(versionTag())+'</b><br>'+(worldResult()?'赛后：真实口径战报':'赛前：虚拟抽象战报 · 平行宇宙玩梗')+' <b style="color:#e7c283">｜ 合并单版</b><br>虚拟币无现金价值 · 非官方粉丝玩梗 · 未成年人需监护人同意</div>';"""

O_BETTAG = """     +'<br><b style="color:#e7c283">'+esc(versionTag())+'</b>'"""
N_BETTAG = """     +'<br><b style="color:#e7c283">'+esc(versionTag())+'</b> · '+(worldResult()?'真实口径战报':'虚拟抽象战报 · 平行宇宙')"""

PAIRS = [
    ('合并版标签', O_LABEL, N_LABEL),
    ('CHARMAP 扩展', O_MAP, N_MAP),
    ('抽象战报生成器', O_FEED_HEAD, ABS),
    ('结算页抽象声明', O_QUOTE, N_QUOTE),
    ('分享卡抽象冠军', O_CARD, N_CARD),
    ('说明页两新段', O_INFO, N_INFO),
    ('标题战报口径', O_TITLE, N_TITLE),
    ('押注台战报口径', O_BETTAG, N_BETTAG),
]

for name, old, new in PAIRS:
    c = h.count(old)
    if c != 1:
        print('  !!', name, 'anchor count =', c); sys.exit(1)
    h = h.replace(old, new, 1)

# 分层版注释改成合并版口径
h = h.replace('/* ===== 分层解耦：BGS(6) × CHARS(12) = 72 组合；角色层与背景板独立替换 ===== */',
              '/* ===== 合并单版：分层解耦 BGS(6) × CHARS(12) = 72 组合；角色层与背景板独立替换 ===== */', 1)

open(MAIN, 'w', encoding='utf-8').write(h)
print('[merge] 写出', os.path.basename(MAIN), len(h.encode())//1024, 'KB')
print('  script', h.count('<script>'), '/', h.count('</script>'),
      '| 抽象战报', 'buildAbstractFeed' in h,
      '| CHARMAP 12', h.count('host_tbd') >= 2,
      '| 归档', len(os.listdir(ARCH)), '份')
