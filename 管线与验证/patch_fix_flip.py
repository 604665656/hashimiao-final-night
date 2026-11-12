# -*- coding: utf-8 -*-
"""回归随机失败暴露的真 bug：flipAt 与 baronAt 撞在同一局时，
龙坑翻盘的 `host_flip` 差分会被大龙分支的 `host_baron` 覆盖，抽象战报少一个名场面。
两处生成路径（抽象 / 真实）统一错开，且同步注入脚本源码。"""
import sys
O = "  var flipAt=1+Math.floor(Math.random()*Math.max(1,n-1)),baronAt=1+Math.floor(Math.random()*Math.max(1,n-1));"
N = O + "\n  if(baronAt===flipAt)baronAt=1+(baronAt%Math.max(1,n-1));  /* 名场面别挤同一局，避免角色差分互相覆盖 */"
for f, expect in [('/data/workspace/哈士喵决赛押宝夜AVG.html', 2),
                  ('/data/workspace/_merge/patch_merge.py', 1)]:
    h = open(f, encoding='utf-8').read()
    c = h.count(O)
    if c == 0:
        print('  SKIP (已修)', f.split('/')[-1]); continue
    if c != expect:
        print('MISMATCH', f, c); sys.exit(1)
    open(f, 'w', encoding='utf-8').write(h.replace(O, N))
    print('  OK', f.split('/')[-1], '| 替换', c, '处')
