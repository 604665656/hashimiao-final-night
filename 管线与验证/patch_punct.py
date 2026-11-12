# -*- coding: utf-8 -*-
"""真机目检：战报梗句本身带句号，join 后又补一个 →「看看风景。。」双句号。
两处生成路径一起修：抽象战报 + 真实战报。同步改注入脚本源码（幂等，可重复跑）。"""
O = "bits.join('，')+'。'"
N = "bits.join('，').replace(/。+$/,'')+'。'"
for f in ['/data/workspace/哈士喵决赛押宝夜AVG.html', '/data/workspace/_merge/patch_merge.py']:
    h = open(f, encoding='utf-8').read()
    c = h.count(O)
    if c == 0:
        print('  SKIP (已修)', f.split('/')[-1]); continue
    open(f, 'w', encoding='utf-8').write(h.replace(O, N))
    print('  OK', f.split('/')[-1], '| 替换', c, '处')
