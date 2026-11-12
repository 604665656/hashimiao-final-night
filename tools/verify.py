#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合并单版成品静态校验：16 项断言 + 体积/外链/脚本配对。
用法：python tools/verify.py [目标HTML，默认仓库根目录 index.html]
仅依赖 Python 标准库。"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'index.html')

raw = open(target, 'rb').read()
h = raw.decode('utf-8', 'replace')

checks = [
    ('体积 < 1MB',              len(raw) < 1048576),
    ('零外链',                  len(re.findall(r'(?:src|href)="https?://', h)) == 0),
    ('script 标签配对',          h.count('<script>') == h.count('</script>') and h.count('<script>') == 4),
    ('合并单版标签',             '合并单版' in h),
    ('抽象战报生成器',           'buildAbstractFeed' in h),
    ('CHARMAP 12 槽',           '"host_tbd":"char_tbd"' in h),
    ('抽象比分牌',               '平行宇宙模拟比分' in h),
    ('抽象冠军播报',             '平行宇宙冠军' in h),
    ('分享卡降字号',             'teamFs' in h),
    ('撞局修复 ==2',            h.count('名场面别挤同一局') == 2),
    ('双句号残留 ==0',          h.count("bits.join('，')+'。'") == 0),
    ('P0 rulesHtml',            'rulesHtml' in h),
    ('P0 goSummary',            'goSummary' in h),
    ('P0 冻结快照',             'S.locked' in h),
    ('P0 结算幂等',             'S.last.token===token' in h),
    ('音效门禁',                '!enabled||!unlocked' in h),
    ('四项声明',                '未成年人（未满 18 周岁）' in h),
    ('分层资源表',              'var P=' in h and 'var BGS=' in h),
]

failed = []
print('目标:', os.path.relpath(target, ROOT) if target.startswith(ROOT) else target)
print('体积: %d B (%.1f KB) | data:image %d | 外链 %d' % (
    len(raw), len(raw) / 1024, len(re.findall(r'data:image', h)),
    len(re.findall(r'(?:src|href)="https?://', h))))
print('-' * 46)
for name, ok in checks:
    print('  %-20s %s' % (name, 'PASS' if ok else 'FAIL'))
    if not ok:
        failed.append(name)
m = re.search(r"BUILD_LABEL='([^']+)'", h)
print('-' * 46)
print('BUILD_LABEL:', m.group(1) if m else '?')
print('结果: %d/%d PASS' % (len(checks) - len(failed), len(checks)))
if failed:
    print('失败项:', ', '.join(failed))
    sys.exit(1)
print('OK: 合并单版成品校验通过')
