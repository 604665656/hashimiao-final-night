# -*- coding: utf-8 -*-
"""收尾：双战报对比速览 / 开发日记 / 排期第十三节 / 交付包 / 清理 / 一致性校验。"""
import os, glob, re, zipfile, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = '/data/workspace'
FONT = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
f1 = ImageFont.truetype(FONT, 21) if os.path.exists(FONT) else ImageFont.load_default()
f2 = ImageFont.truetype(FONT, 12.5 if False else 13) if os.path.exists(FONT) else ImageFont.load_default()
f3 = ImageFont.truetype(FONT, 11) if os.path.exists(FONT) else ImageFont.load_default()

# ---------- 1) 速览 ----------
items = [
    ('_m_abstract_04_live_open.png', '赛前 · 虚拟抽象战报开场（平行宇宙）'),
    ('_m_abstract_05_live_scene.png', '赛前 · 抽象名场面（龙坑 / 大龙）'),
    ('_m_real_04_live_open.png', '赛后回填 · 真实口径战报'),
    ('_m_abstract_06_result.png', '结算 · 抽象剧本声明 + 版本'),
    ('_m_abstract_card.png', '分享卡 · 抽象冠军（模拟）'),
    ('_m_abstract_07_info.png', '说明页 · 双战报 + 单版合并'),
]
W, H, lab, pad, top = 270, 585, 22, 10, 62
cols, rows = 3, 2
rowh = H + lab + pad
s = Image.new('RGB', (W*cols+pad*(cols+1), top+pad+rows*rowh+pad), (20,22,29))
d = ImageDraw.Draw(s)
d.text((pad, 8), '合并单版 · 虚拟抽象战报 ↔ 真实口径战报', fill=(231,194,131), font=f1)
d.text((pad, 38), '赛前走平行宇宙抽象剧本，11.15 回填后自动切真实；根目录只留一个 HTML', fill=(178,172,160), font=f3)
for i, (fn, label) in enumerate(items):
    im = Image.open(os.path.join(ROOT, fn)).convert('RGB'); im.thumbnail((W, H))
    x = pad+(i%cols)*(W+pad); y = top+pad+(i//cols)*rowh
    s.paste(im, (x, y))
    d.rectangle((x, y+im.height, x+W, y+im.height+lab), fill=(28,30,38))
    d.text((x+5, y+im.height+3), label, fill=(210,215,230), font=f2)
s.save(os.path.join(ROOT, '哈士喵_合并单版与抽象战报_速览.png'))
print('[1] 速览', s.size)

# ---------- 2) 开发日记 ----------
diary = '''# 哈士喵 · 决赛押宝夜 AVG｜合并单版 + 虚拟抽象战报 · 开发日记

日期：2026-11-12　｜　触发：用户「没有虚拟抽象战报诶，两版有啥不同吗，合并一版怎么样」

---

## 一、要解决什么

一句话里三件事：

1. **「没有虚拟抽象战报」**：项目最初是「抽象的决赛云观赛小游戏」，站队用「深蓝不熬夜 / 赤焰别上头 / TBD 空降」，加押一血、龙坑大翻盘等名场面。后来按用户要求接了真实 BLG vs GEN，战报全变成真实队名 + 具体赛事播报，P0 又加了逐项核对，梗味被账单味盖住。用户念的是那份**抽象玩梗**没了。
2. **「两版有啥不同」**：需要把 `哈士喵决赛押宝夜AVG.html`（主成品）与 `哈士喵决赛押宝夜AVG_分层架构验证.html` 的真实差异说清，而不是含糊说「一个分层一个没分层」。
3. **「合并一版」**：双份维护几轮下来每次都要同步注入两次、回归两次，该收敛了。

**本轮口径**：把「虚拟抽象战报」实现为**赛前模拟推演的专属剧本**——只在 `R.demo===true`（11.15 真实赛果未产生）时走，用抽象代号与梗化名场面，明确「平行宇宙、非真实赛果、非官方预测」；回填真实赛果后自动切回 BLG/GEN 真实口径。**押注项仍是现实对阵**，结算公式与冻结规则完全不动，只换叙事层。这样既接了现实，又不把随机推演包装成真实赛果预测。

**硬约束不变**：单 HTML、零外链、断网可开、< 1 MB、音效默认关、P0 七项与 Toy 层全部保留。

---

## 二、怎么做的

### 1）先精确 diff，答案是「玩法零差异，只差美术组织」

对两版做行级 diff（base64 大行做哈希归约），99 行差异全部集中在五处：

| 维度 | 主成品 | 分层验证版 |
|---|---|---|
| 资源表 | `ASSETS` 一张表 15 项 | `P`(8 透明层) + `BGS`(6 空场景) + `CHARS`(12 槽) + `CHARMAP` |
| 立绘卡 | 整图 + 当前全屏背景当卡底 | 按对白 `bgKey` 独立换背景板、角色用透明层，72 组合 |
| CSS | `height:auto` | `aspect-ratio:3/4` + `object-fit:cover`，防变形 |

标题立绘 / 押注台小头像 / 分享卡也分别走 `ASSETS.host_*` vs `P.*`、`IMG.layer`。**玩法、WORLDS 快照、Toy 双榜体力、19 项押注、冻结幂等、规则表、音效、四项声明、版本标识：零差异**。所以合并没有取舍难题：以分层解耦版为唯一基线即可，旧两版复制进交付包归档，根目录只留一个 HTML。

### 2）虚拟抽象战报

- 新增 `ABS_NAME`（深蓝不熬夜 / 赤焰别上头 / 河道蟹本人 / 谁也没翻 / 大龙本龙）、`ABS_SCENE` 十条抽象梗句、`ABS_QUOTE` 六条喵喵吐槽、`absSide()` / `absActualText()`。
- `buildFeed(R)` 开头加 `if(R.demo)return buildAbstractFeed(R)`，真实模式的原有战报**一行未改**。
- 抽象剧本结构：喵喵开场（host_tbd「玄学空降」差分）→ 谁先破功（抽象一血）→ 逐局抽象名场面（按 flipAt/baronAt 触发 `host_flip` 龙坑大翻盘、`host_baron` 大龙本龙，其余随机梗句）→ 灯牌（打满五局→「灯牌打到没电」）→ 喵喵终场（抽象冠军 + 明确非真实赛果、非官方预测）→ **虚拟核对**（已押项逐条给分，标成「平行宇宙实际 / 虚拟账」）。
- 顺手把 `CHARMAP` 从 8 槽扩到 12 槽：`host_flip/host_baron/host_quote/host_tbd` 映射到此前定义却一直没用上的 4 个角色槽，抽象名场面终于有专属差分。
- 结算页 quote 追加「喵喵模拟推演 · 平行宇宙抽象剧本，与 11.15 真实赛果无关」；分享卡 demo 时冠军行改成「抽象冠军 · 深蓝不熬夜（模拟）」；标题页 / 押注台按 `worldResult()` 显示「赛前：虚拟抽象战报 / 赛后：真实口径战报」；说明页新增「虚拟抽象战报」「单版合并」两段。
- 版本标签改为 `11.12 封盘版 · 合并单版`（保留 `11.12 封盘版` 前缀，旧断言仍成立）。

### 3）边做边排查

真机目检抽象战报时抓到「理由是看看风景。。」双句号：梗句自带句号，`bits.join('，')+'。'` 又补一个。抽象与真实两条生成路径一起改成 `.replace(/。+$/,'')+'。'`，并同步回注入脚本源码，保证可复现。

---

## 三、验证

**jsdom**：`regress_merge.js` 单版 × 赛前 / 已回填 / 坏档 = **3 组全 PASS**。覆盖：

- 合并版标签、`P/BGS/CHARS`、CHARMAP 12 槽、零外链、音效默认关且未解锁、P0 规则/摘要/冻结/幂等/四项声明、WORLDS 与 Toy、`versionTag()`；
- 赛前战报：含平行宇宙 / 抽象代号 / 喵喵开场 / 虚拟核对 / 龙坑与大龙名场面，**不含**「导播信号接入」「数据来源：官方赛程快照」，且确实用上了 `host_tbd/host_flip/host_baron` 三个闲置槽；
- 赛后战报：含真实开场与官方快照口径，**不含**「平行宇宙」「虚拟核对」；
- 两种模式都保留 2 条已押项核对、冻结深拷贝（篡改 `S.picks` 为 9999 仍按冻结结算）、重复 `settle()` 幂等、PNG 分享卡、说明页双战报与合并、10 音效无非法 ramp、坏档回退与备份、无 JS 运行时错误。

**Chromium 真机 390×844 @2x**：`shot_merge.js` 两态各 7 屏 + PNG 卡，`page errors: none`、`warnings: 0`；真机直接读 localStorage 里的 `feed` 断言「平行宇宙 + 虚拟核对」/「导播信号接入且无平行宇宙」，并逐张目检立绘差分、背景板、打字机与声明。

**成品**：`node --check` 通过，script 4/4，**零外链**，单文件 **434 KB**，断网可开。根目录只剩 `哈士喵决赛押宝夜AVG.html` 一个 HTML；旧两版在交付包 `归档/` 内可回溯。

---

## 四、坑

1. **别用「看起来像」判断两版差异**：两版 KB 几乎一样、截图也像，直觉会说「差不多」，但资源表与立绘卡渲染路径完全不同。必须做行级 diff；base64 大行要先哈希归约，否则 diff 被几万字符淹没。
2. **抽象战报不能写成「模拟的 BLG 3:1 GEN」**：随机推演一旦挂真实队名，就像在发布赛果预测。叙述层用抽象代号，核对层才出现押注单里的真实选项，并明确标「虚拟账」。
3. **梗句自带标点，拼接别再补**：`join('，')+'。'` 是两版战报共有的老问题，抽象剧本梗句更长所以更显眼。修一处要记得修两条生成路径。
4. **补丁源码要同步**：标点补丁第一次只改了 HTML，注入脚本源码里还留着旧写法，重新注入会复活双句号；改成幂等脚本后统一。
5. **回归调用方式**：坏档是第二个参数（`pre corrupt`），不是 `mode=corrupt`；写成后者会走进完整流程并按真实模式断言，报一个看似「真实战报不对」的假故障。
6. **测试断言别写恒真式**：`includes(...)===false||true` 这种占位断言会永远 PASS，已换成实际检查版本标识；`every` 里 `&&`/`||` 也补了括号。
7. **真机别拿打字机中间态断言**：把 `setTimeout` 压到 2ms 后，`#dlg` 的文本可能只打到半句。改读 localStorage 里已 `save()` 的完整 `feed`，稳。
8. **归档会被重跑覆盖**：`patch_merge.py` 开头会把当前 MAIN 复制进归档，重跑一次就把「旧主成品」覆盖成合并版。要复现必须从未改动的基线目录跑，别在原地重跑。
9. **`CHARMAP` 闲置槽不等于可用**：之前定义了 `char_flip/char_baron/char_quote/char_tbd`，但 `CHARMAP` 只映射 8 个 `host_*`，`setPortrait` 遇到新 key 会 fallback 到 `char_idle`。扩映射后差分才真的换。
10. **合并别丢分层版的 `bgKey`**：分层版 `setPortrait(key,fx,bgKey)` 按对白换卡内背景，主版用全局 `CUR_BG`。合并取分层版，抽象战报每条才能按 `hot` 走月夜、其余走雪夜。
11. **如实说明口径**：本轮是「按赛前/赛后自动切」，不是「随时手动切抽象/真实」。若后面要开关，得在 `startLive` 前加口径选择并写进冻结快照，否则同一份存档回放会不一致。

---

## 五、下一步

- **11.15 赛后**：重跑快照脚本回填真实赛果，重新内嵌；页面自动从抽象剧本切到真实口径战报，结算进实战榜。
- **B站 Toy**：官方规范到手后实现 `ToyImpl` 并 `mount`，把封盘时间、每日次数、分享发奖移到服务端。
- **可选**：加「战报口径手动切换 / 回看对比」，需把口径写进 `S.locked` 快照；横版 1200×630 分享卡；`build.js` 合并所有注入与回归脚本并加体积校验。
'''
open(os.path.join(ROOT, '哈士喵_合并单版与抽象战报_开发日记.md'), 'w', encoding='utf-8').write(diary)
print('[2] 日记', len(diary), 'bytes')

# ---------- 3) 排期第十三节 ----------
p = os.path.join(ROOT, '哈士喵决赛押宝夜_美术生成排期.md')
t = open(p, encoding='utf-8').read()
t += '''

---

## 十三、合并单版 + 虚拟抽象战报（11.12 完成）

触发：用户「没有虚拟抽象战报诶，两版有啥不同吗，合并一版怎么样」。

- [x] **两版差异查清**：行级 diff 99 行，玩法 / 数据 / 音效 / P0 零差异，只差美术资源组织（ASSETS 单表 vs P+BGS+CHARS 分层解耦）与立绘卡渲染
- [x] **合并单版**：以分层解耦版（8 透明角色层 × 6 生成空场景 = 72 组合）为唯一基线，旧两版归档，根目录只留一个 HTML
- [x] **虚拟抽象战报**：赛前 `demo` 走「喵喵模拟推演 · 平行宇宙」——深蓝不熬夜 / 赤焰别上头 / TBD 空降，一血 / 龙坑大翻盘 / 先动大龙 / 打满五局梗化名场面，不把模拟赛果写成真实队名；逐项核对标「虚拟账」
- [x] **真实战报不动**：11.15 回填后自动切回 BLG / GEN + 官方快照口径
- [x] **CHARMAP 扩到 12 槽**：`host_flip / host_baron / host_quote / host_tbd` 用上此前闲置的 4 个角色差分
- [x] 六处口径同步：标题 / 押注台 / 结算 quote / 分享卡 / 说明页 / 版本标签（`11.12 封盘版 · 合并单版`）
- [x] 排查修复：梗句双句号（两条生成路径一起改）、回归调用方式、恒真断言、真机打字机中间态断言
- [x] **验证**：jsdom 3 组（赛前 / 已回填 / 坏档）全 PASS；Chromium 真机双态各 7 屏 + PNG 卡，`page errors: none`；单文件 434 KB、零外链、script 4/4
- [ ] 11.15 回填真实赛果；B站 Toy 官方规范到手后 `mount(ToyImpl)`
- [ ] 可选：战报口径手动切换（需写进冻结快照）、横版分享卡、`build.js` 统一构建

> 完整明细见《哈士喵_合并单版与抽象战报_开发日记.md》。
'''
open(p, 'w', encoding='utf-8').write(t)
print('[3] 排期第十三节', len(t), 'bytes')

# ---------- 4) 交付包 ----------
zpath = os.path.join(ROOT, '哈士喵_合并单版_交付包.zip')
z = zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=6)
z.write(os.path.join(ROOT, '哈士喵_合并单版与抽象战报_速览.png'), '速览/双战报对比.png')
for n in ['patch_merge.py','patch_punct.py','regress_merge.js','shot_merge.js','finalize.py']:
    z.write(os.path.join(ROOT, '_merge', n), '管线与验证/'+n)
for n in ['归档_主成品_ASSETS单表.html','归档_分层验证版_P_BGS.html']:
    z.write(os.path.join(ROOT, '_merge', 'archive', n), '归档/'+n)
for n in ['哈士喵_合并单版与抽象战报_开发日记.md','哈士喵决赛押宝夜_美术生成排期.md']:
    z.write(os.path.join(ROOT, n), n)
z.close()
print('[4] 交付包', os.path.getsize(zpath)//1024, 'KB', len(z.namelist()), 'files')

# ---------- 5) 清理：根目录只留合并版 ----------
for f in glob.glob(os.path.join(ROOT, '_m_*.png')) + \
         glob.glob(os.path.join(ROOT, '_chk_*.js')) + \
         glob.glob(os.path.join(ROOT, 'package*.json')) + \
         glob.glob(os.path.join(ROOT, '_s_*.png')):
    os.remove(f)
layer = os.path.join(ROOT, '哈士喵决赛押宝夜AVG_分层架构验证.html')
if os.path.exists(layer): os.remove(layer)
for dd in ['node_modules','_merge','_p0','_gen2']:
    pp = os.path.join(ROOT, dd)
    if os.path.isdir(pp): shutil.rmtree(pp)
print('[5] 清理完成；根目录 HTML:', [x for x in os.listdir(ROOT) if x.endswith('.html')])

# ---------- 6) 一致性 ----------
h = open(os.path.join(ROOT, '哈士喵决赛押宝夜AVG.html'), encoding='utf-8').read()
clean = '\n'.join(l for l in h.split('\n') if 'base64' not in l and len(l) < 1400)
print('[6] 最终校验')
print('  KB', len(h.encode())//1024, '| script', h.count('<script>'), '/', h.count('</script>'),
      '| 外链', len(re.findall(r'(?:src|href)="https?://', h)))
print('  合并标签', '合并单版' in h, '| 抽象战报', 'buildAbstractFeed' in h,
      '| 12 槽', '"host_tbd":"char_tbd"' in h,
      '| 双句号残留', h.count("bits.join('，')+'。'"))
print('  P0 保留', all(k in h for k in ['rulesHtml','goSummary','S.locked','S.last.token===token']),
      '| 音效门禁', '!enabled||!unlocked' in h,
      '| 四项声明', '未成年人（未满 18 周岁）' in h,
      '| 旧字眼', len(re.findall(r'同图色调派生|程序化绘制|深蓝|赤焰|TBD 空降', clean)))
d = open(os.path.join(ROOT, '哈士喵_合并单版与抽象战报_开发日记.md'), encoding='utf-8').read()
print('  四小节', all(k in d for k in ['一、要解决什么','二、怎么做的','三、验证','四、坑']))
print('  临时残留', len([x for x in os.listdir(ROOT) if x.startswith(('_m_','_chk_','_s_','_p0','_gen','_merge','node_modules','package'))]))
