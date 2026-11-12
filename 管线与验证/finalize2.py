# -*- coding: utf-8 -*-
"""最终收尾：重出速览 / 文档补记两处排查 / 重建交付包 / 清理 / 一致性校验。"""
import os, glob, re, zipfile, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = '/data/workspace'
FONT = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
f1 = ImageFont.truetype(FONT, 21) if os.path.exists(FONT) else ImageFont.load_default()
f2 = ImageFont.truetype(FONT, 13) if os.path.exists(FONT) else ImageFont.load_default()
f3 = ImageFont.truetype(FONT, 11) if os.path.exists(FONT) else ImageFont.load_default()

# ---------- 1) 速览（用补漏后的截图） ----------
items = [
    ('_m_abstract_04_live_open.png', '赛前 · 虚拟抽象战报开场（平行宇宙）'),
    ('_m_abstract_05_live_scene.png', '赛前 · 抽象名场面（龙坑 / 大龙）'),
    ('_m_real_04_live_open.png', '赛后回填 · 真实口径战报'),
    ('_m_abstract_06_result.png', '结算 · 抽象比分牌 + 现实押注单'),
    ('_m_abstract_card.png', '分享卡 · 抽象冠军（模拟）'),
    ('_m_abstract_07_info.png', '说明页 · 双战报 + 单版合并'),
]
W,H,lab,pad,top = 270,585,22,10,62
cols,rows = 3,2
rowh = H+lab+pad
s = Image.new('RGB',(W*cols+pad*(cols+1),top+pad+rows*rowh+pad),(20,22,29))
d = ImageDraw.Draw(s)
d.text((pad,8),'合并单版 · 虚拟抽象战报 ↔ 真实口径战报',fill=(231,194,131),font=f1)
d.text((pad,38),'赛前走平行宇宙抽象剧本，11.15 回填后自动切真实；根目录只留一个 HTML',fill=(178,172,160),font=f3)
for i,(fn,label) in enumerate(items):
    im = Image.open(os.path.join(ROOT,fn)).convert('RGB'); im.thumbnail((W,H))
    x = pad+(i%cols)*(W+pad); y = top+pad+(i//cols)*rowh
    s.paste(im,(x,y))
    d.rectangle((x,y+im.height,x+W,y+im.height+lab),fill=(28,30,38))
    d.text((x+5,y+im.height+3),label,fill=(210,215,230),font=f2)
s.save(os.path.join(ROOT,'哈士喵_合并单版与抽象战报_速览.png'))
print('[1] 速览',s.size)

# ---------- 2) 日记补记 ----------
dp = os.path.join(ROOT,'哈士喵_合并单版与抽象战报_开发日记.md')
t = open(dp,encoding='utf-8').read()
o2 = "### 3）边做边排查\n\n真机目检抽象战报时抓到「理由是看看风景。。」双句号：梗句自带句号，`bits.join('，')+'。'` 又补一个。抽象与真实两条生成路径一起改成 `.replace(/。+$/,'')+'。'`，并同步回注入脚本源码，保证可复现。"
n2 = """### 3）边做边排查（三轮）

**第一轮**：真机目检抽象战报时抓到「理由是看看风景。。」双句号——梗句自带句号，`bits.join('，')+'。'` 又补一个。抽象与真实两条生成路径一起改成 `.replace(/。+$/,'')+'。'`。

**第二轮**：速览目检发现「叙事抽象了、结算没抽象」——比分牌 / 赛后梗向播报 / 分享卡仍写「BLG 2:3 GEN」当模拟赛果，像在发布预测。补 `patch_score.py` 把这三处也切到抽象代号并加「平行宇宙模拟比分 · 非 11.15 真实赛果」；**押注单 rows 与逐项核对保留现实选项**，可复核性不丢。分享卡抽象队名较长，字号从 30px 降到 21px 避免压到中间比分。

**第三轮**：5 轮随机回归偶发失败，定位到真 bug——`flipAt` 与 `baronAt` 撞在同一局时，龙坑翻盘的 `host_flip` 差分被大龙分支的 `host_baron` 覆盖，抽象战报少一个名场面。`patch_fix_flip.py` 让两个名场面强制错开（抽象与真实两条路径一起改），并同步注入脚本源码。"""
assert t.count(o2)==1
t = t.replace(o2,n2,1)
o3 = "**Chromium 真机 390×844 @2x**：`shot_merge.js` 两态各 7 屏 + PNG 卡，`page errors: none`、`warnings: 0`；真机直接读 localStorage 里的 `feed` 断言「平行宇宙 + 虚拟核对」/「导播信号接入且无平行宇宙」，并逐张目检立绘差分、背景板、打字机与声明。"
n3 = o3 + "\n\n**随机稳定性**：补完撞局修复后，赛前模式连跑 **5 轮随机回归**全 PASS（此前偶发失败已消失），另加已回填、坏档各 1 组；结算页新增断言「平行宇宙模拟比分 / 平行宇宙冠军」，真实模式断言「不掺抽象比分牌」。"
assert t.count(o3)==1
t = t.replace(o3,n3,1)
o4 = "11. **如实说明口径**：本轮是「按赛前/赛后自动切」，不是「随时手动切抽象/真实」。若后面要开关，得在 `startLive` 前加口径选择并写进冻结快照，否则同一份存档回放会不一致。"
n4 = o4 + """
12. **抽象要贯穿到结算与分享卡**：只改战报不够，比分牌、赛后播报、分享卡只要还写「BLG 3:1 GEN」，用户就会觉得「模拟赛果被当成真预测」。判据是：**叙述层抽象、账单层现实**。
13. **两个随机事件别用同一个 `m` 变量**：`flipAt`/`baronAt` 撞局时后写的分支静默覆盖先写的角色差分，单看代码不显眼，只有多轮随机回归才抓得到。错开事件比「分支里判断 m 是否已被改」更干净。
14. **长抽象队名要降字号**：「深蓝不熬夜」五个字按 30px 画会挤到中间比分，Canvas 没有自动换行，得手动给 `teamFs`。"""
assert t.count(o4)==1
t = t.replace(o4,n4,1)
open(dp,'w',encoding='utf-8').write(t)
print('[2] 日记补记',len(t),'bytes')

# ---------- 3) 排期补两句 ----------
pp = os.path.join(ROOT,'哈士喵决赛押宝夜_美术生成排期.md')
pt = open(pp,encoding='utf-8').read()
o5 = "- [ ] 11.15 回填真实赛果；B站 Toy 官方规范到手后 `mount(ToyImpl)`"
n5 = """- [x] **抽象口径补漏**：结算比分牌 / 赛后播报 / 分享卡在赛前也改用抽象代号并标注「平行宇宙模拟」，押注单与逐项核对仍保留现实选项
- [x] **随机稳定性**：修复「龙坑翻盘与大龙撞同一局导致角色差分被覆盖」，抽象与真实两条路径一起错开；赛前连跑 5 轮随机回归全 PASS
- [ ] 11.15 回填真实赛果；B站 Toy 官方规范到手后 `mount(ToyImpl)`"""
assert pt.count(o5)==1
open(pp,'w',encoding='utf-8').write(pt.replace(o5,n5,1))
print('[3] 排期补记',len(pt),'bytes')

# ---------- 4) 重建交付包 ----------
oldz = os.path.join(ROOT,'哈士喵_合并单版_交付包.zip')
old = {}
with zipfile.ZipFile(oldz,'r') as z:
    for i in z.infolist(): old[i.filename] = z.read(i.filename)
os.remove(oldz)
zp = oldz
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.write(os.path.join(ROOT,'哈士喵_合并单版与抽象战报_速览.png'),'速览/双战报对比.png')
    for n in ['patch_merge.py','patch_punct.py','regress_merge.js','shot_merge.js','finalize.py']:
        z.write(os.path.join(ROOT,'_merge',n),'管线与验证/'+n)
    for n in ['patch_score.py','patch_fix_flip.py','finalize2.py']:
        z.write(os.path.join(ROOT,'_merge2',n),'管线与验证/'+n)
    for name,blob in old.items():
        if name.startswith('归档/'): z.writestr(name,blob)
    for n in ['哈士喵_合并单版与抽象战报_开发日记.md','哈士喵决赛押宝夜_美术生成排期.md']:
        z.write(os.path.join(ROOT,n),n)
print('[4] 交付包',os.path.getsize(zp)//1024,'KB')

# ---------- 5) 清理 ----------
for f in glob.glob(os.path.join(ROOT,'_m_*.png')) + \
         glob.glob(os.path.join(ROOT,'_chk_*.js')) + \
         glob.glob(os.path.join(ROOT,'package*.json')) + \
         glob.glob(os.path.join(ROOT,'_s_*.png')):
    os.remove(f)
for dd in ['node_modules','_merge','_merge2']:
    p2 = os.path.join(ROOT,dd)
    if os.path.isdir(p2): shutil.rmtree(p2)
print('[5] 清理；根目录 HTML:',[x for x in os.listdir(ROOT) if x.endswith('.html')])

# ---------- 6) 最终校验 ----------
h = open(os.path.join(ROOT,'哈士喵决赛押宝夜AVG.html'),encoding='utf-8').read()
clean = '\n'.join(l for l in h.split('\n') if 'base64' not in l and len(l)<1400)
print('[6] 最终校验')
print('  KB',len(h.encode())//1024,'| script',h.count('<script>'),'/',h.count('</script>'),
      '| 外链',len(re.findall(r'(?:src|href)="https?://',h)))
print('  合并', '合并单版' in h, '| 抽象战报', 'buildAbstractFeed' in h,
      '| 12 槽', '"host_tbd":"char_tbd"' in h,
      '| 抽象比分牌', '平行宇宙模拟比分' in h,
      '| 撞局修复', h.count('名场面别挤同一局')==2,
      '| 双句号残留', h.count("bits.join('，')+'。'"))
print('  P0', all(k in h for k in ['rulesHtml','goSummary','S.locked','S.last.token===token']),
      '| 音效门禁', '!enabled||!unlocked' in h,
      '| 四项声明', '未成年人（未满 18 周岁）' in h,
      '| 抽象代号出现', len(re.findall(r'深蓝不熬夜|赤焰别上头|TBD 空降',clean)))
d = open(dp,encoding='utf-8').read()
print('  四小节',all(k in d for k in ['一、要解决什么','二、怎么做的','三、验证','四、坑']),
      '| 坑数',len(re.findall(r'^\d+\. ',d,re.M)))
with zipfile.ZipFile(zp) as z: print('  包内',len(z.namelist()),'项')
print('  临时残留',len([x for x in os.listdir(ROOT) if x.startswith(('_m_','_chk_','_s_','_merge','_p0','_gen','node_modules','package'))]))
