/* 合并单版专项回归：抽象/真实双战报 + P0 全保留 + 音效门禁 + 坏档 */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = '哈士喵决赛押宝夜AVG.html';
const mode = process.argv[2] || 'pre';
const corrupt = process.argv[3] === 'corrupt';
let html = fs.readFileSync('/data/workspace/' + file, 'utf8');
if (mode === 'completed') {
  const r = {champion:'BLG',score:'3:1',bw:3,rw:1,firstblood:'GEN',dragonflip:'BLG',
             firstbaron:'BLG',fullseries:'no',note:'回归用例，非真实赛果'};
  html = html.replace(/("result":)(null)/, '$1'+JSON.stringify(r))
             .replace(/("state":)"unstarted"/, '$1"completed"')
             .replace(/("score":)null/, '$1"3:1"');
}
html = html.replace('/* ================= 分享卡 ================= */',
  'window.__t={settle:settle,S:S,versionTag:versionTag,buildFeed:buildFeed,buildAbstractFeed:buildAbstractFeed,load:load,totalStake:totalStake};\n/* ================= 分享卡 ================= */');

const errors=[];
const vc=new VirtualConsole();
vc.on('jsdomError',e=>errors.push('jsdomError: '+e.message));
vc.on('error',(...a)=>errors.push('console.error: '+a.join(' ')));
function MockAudio(win){
  const c={osc:0,gain:0,buffer:0,src:0,filter:0,start:0,stop:0,ramp:0,badRamp:0};win.__audioCalls=c;
  function P(){this.value=0;}
  P.prototype.setValueAtTime=function(){return this;};
  P.prototype.exponentialRampToValueAtTime=function(v){c.ramp++;if(typeof v!=='number'||!isFinite(v)||v<=0)c.badRamp++;return this;};
  function N(){this.gain=new P();this.frequency=new P();this.Q=new P();this.type='';}
  N.prototype.connect=function(){return this;};N.prototype.start=function(){c.start++;};N.prototype.stop=function(){c.stop++;};
  function C(){this.currentTime=0;this.sampleRate=44100;this.state='running';this.destination={};}
  C.prototype.createGain=function(){c.gain++;return new N();};
  C.prototype.createOscillator=function(){c.osc++;return new N();};
  C.prototype.createBiquadFilter=function(){c.filter++;return new N();};
  C.prototype.createBufferSource=function(){c.src++;return new N();};
  C.prototype.createBuffer=function(ch,len){c.buffer++;return {getChannelData:()=>new Float32Array(len)};};
  C.prototype.resume=function(){this.state='running';return Promise.resolve();};
  win.AudioContext=C;
}
const dom=new JSDOM(html,{runScripts:'dangerously',url:'http://localhost/',pretendToBeVisual:true,virtualConsole:vc,
  beforeParse(win){
    const raw=win.setTimeout.bind(win);
    win.setTimeout=(fn,ms,...r)=>raw(fn,Math.min(ms||0,1),...r);
    win.setInterval=()=>0;win.scrollTo=()=>{};win.HTMLElement.prototype.scrollIntoView=()=>{};
    MockAudio(win);
    if(corrupt){try{win.localStorage.setItem('hashimiao-s-final-avg-v2','{"balance":"NaN","picks":[');}catch(e){}}
    else{try{win.localStorage.clear();}catch(e){}}
    const fake=new Proxy({},{get(t,k){if(k==='createLinearGradient'||k==='createRadialGradient')return()=>({addColorStop(){}});return()=>{};},set(){return true;}});
    win.HTMLCanvasElement.prototype.getContext=()=>fake;
    win.HTMLCanvasElement.prototype.toDataURL=()=> 'data:image/png;base64,AAA';
    win.addEventListener('error',e=>errors.push('window.error: '+e.message));
  }});
const d=dom.window.document,W=dom.window;
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const $=s=>d.querySelector(s),txt=s=>($(s)||{}).textContent||'';
const ok=(c,m)=>{if(!c)throw new Error('FAIL: '+m);console.log('  ok - '+m);};
async function until(sel,max=360){for(let i=0;i<max;i++){if($(sel))return true;const dlg=$('#dlg');if(dlg)dlg.click();await wait(8);}return !!$(sel);}

(async()=>{
  console.log('\n=== 合并单版 |',mode,corrupt?'| 坏档':'','===');
  await wait(60);
  const S=W.__t.S;

  console.log('[0] 单版结构 / 抽象层 / 硬约束');
  ok(html.includes('合并单版')&&html.includes('buildAbstractFeed'),'合并版标签 + 抽象战报在');
  ok(html.includes('var P=')&&html.includes('var BGS=')&&html.includes('var CHARS='),'分层解耦 P / BGS / CHARS 保留');
  ok(html.includes('"host_tbd":"char_tbd"'),'CHARMAP 扩到 12 槽（抽象名场面差分可用）');
  ok(!/<script[^>]+src=|<link[^>]+href=|@import\s+url|fonts\.googleapis\.com\/css/.test(html),'无外链脚本/样式/字体');
  ok((html.match(/(?:src|href)="https?:\/\//g)||[]).length===0,'零外链');
  ok(html.includes('rulesHtml')&&html.includes('goSummary')&&html.includes('S.locked'),'P0 规则/摘要/冻结保留');
  ok(html.includes('S.last.token===token')&&html.includes('未成年人（未满 18 周岁）'),'幂等 + 四项声明保留');
  ok(html.includes("if(!enabled||!unlocked||!B[name])"),'音效刷新门禁保留');
  ok(W.SFX.enabled===false&&W.SFX.unlocked===false&&W.SFX.ctxCreated===false,'音效默认关且未解锁');
  ok(W.__audioCalls.osc===0,'默认关零音频节点');
  ok(html.includes('var WORLDS =')&&html.includes('ToyAdapter.cloud.save'),'真实快照 + Toy 层保留');
  ok(W.ASSETS&&W.BGS&&Object.keys(W.BGS).length===6&&W.CHARS&&Object.keys(W.CHARS).length===12,'BGS 6 × CHARS 12');
  ok(W.__t.versionTag().includes('11.12 封盘版'),'版本标识仍可复核');

  console.log('[1] 存档加固');
  ok(S.schemaVersion===3&&S.buildId==='s16-final-avg-2026-11-12','schemaVersion / buildId');
  if(corrupt){
    ok(S.balance===1000&&Object.keys(S.picks).length===0,'坏档回退初始状态');
    ok((W.localStorage.getItem('hashimiao-s-final-avg-v2.bad')||'').includes('NaN'),'坏档已备份');
    ok(errors.length===0,'坏档路径无 JS 错误');console.log('PASS');return;
  }

  console.log('[2] 标题 → 站队 → 押注台');
  ok(!!$('#startBtn'),'标题页');
  ok(d.body.textContent.includes('合并单版'),'标题页标明合并单版');
  ok(d.body.textContent.includes(mode==='completed'?'赛后：真实口径战报':'赛前：虚拟抽象战报'),'标题页标明当前战报口径');
  $('#startBtn').click();ok(!!$('#dlg'),'序章对白');
  ok(!!$('#pBg')&&!!$('#pImg'),'立绘卡双层（分层解耦）');
  ok(await until('.choice'),'站队选项');
  ok(d.querySelectorAll('.choice').length===3,'BLG / GEN / 中立');
  d.querySelectorAll('.choice')[0].click();
  ok(txt('#stanceChip').includes('BLG'),'立场写入 HUD');
  ok(await until('#betScroll'),'押注台');
  ok(d.querySelectorAll('.opt').length===19,'6 组 19 项');
  ok(txt('#betScroll').includes(mode==='completed'?'真实口径战报':'虚拟抽象战报'),'押注台标明战报口径');
  $('#ruleBtn').click();
  ok((txt('#modal').match(/x\d+\.\d{2}/g)||[]).length>=19,'规则速查 19 项');
  $('#closeM').click();

  console.log('[3] 摘要 → 冻结');
  $('.opt[data-g="champion"][data-o="blue"]').click();
  $('.opt[data-g="score"][data-o="3:1"]').click();
  $('.opt[data-g="firstblood"][data-o="blue"]').click();
  $('[data-act="remove"][data-g="score"][data-o="3:1"]').click();
  ok(txt('#slip').includes('2 项'),'最终 2 项');
  $('#goBtn').click();
  ok(!!$('#sumOk'),'封盘摘要');
  $('#sumBack').click();ok(!$('#mask').classList.contains('show')&&!S.locked,'返回不冻结');
  $('#goBtn').click();$('#sumOk').click();
  ok(!!S.locked&&S.locked.stake===W.__t.totalStake(),'冻结深拷贝');
  ok(await until('.choice'),'封盘确认');
  const before=S.balance;
  Object.keys(S.picks).forEach(k=>{S.picks[k].stake=9999;});
  d.querySelectorAll('.choice')[0].click();
  ok(!!$('#progI'),'LIVE 战报启动');

  console.log('[4] 战报口径：'+mode);
  const feed=S.feed||[],all=feed.map(f=>f.t||'').join(' ');
  const checks=feed.filter(f=>(f.t||'').indexOf('核对 ·')>=0);
  ok(checks.length===2,'已押 2 项逐条核对 ('+checks.length+')');
  ok(checks.every(f=>{var t=f.t||'';return t.includes('你押')&&(t.includes('命中 +')||t.includes('未中 −'));}),'每条含你押 / 得分');
  const portraits=feed.map(f=>f.m);
  if(mode==='pre'){
    ok(all.includes('平行宇宙')&&all.includes('喵喵模拟推演'),'抽象战报：平行宇宙声明');
    ok(all.includes('深蓝不熬夜')||all.includes('赤焰别上头'),'抽象代号队伍在场');
    ok(all.includes('喵喵开场')&&all.includes('虚拟核对'),'抽象开场 + 虚拟核对标签');
    ok(all.includes('龙坑上演大翻盘')||all.includes('连大龙都看困了'),'龙坑名场面抽象化');
    ok(all.includes('大龙本龙')||all.includes('率先摸了一下大龙'),'大龙名场面抽象化');
    ok(!all.includes('导播信号接入'),'不冒充真实赛事播报');
    ok(!all.includes('数据来源：官方赛程快照'),'不冒充官方快照');
    ok(portraits.includes('host_tbd')&&portraits.includes('host_flip')&&portraits.includes('host_baron'),'用上 3 个闲置抽象差分槽');
    ok(feed.every(f=>(f.tag||'').includes('虚拟'))||all.includes('虚拟核对'),'战报标签为虚拟口径');
  }else{
    ok(all.includes('导播信号接入')&&all.includes('数据来源：官方赛程快照'),'真实口径战报');
    ok(all.includes('BLG')||all.includes('GEN'),'真实队名在场');
    ok(!all.includes('平行宇宙')&&!all.includes('虚拟核对'),'真实模式不掺抽象剧本');
    ok(portraits.includes('host_dark'),'真实战报角色差分');
  }

  console.log('[5] 结算 / 幂等 / 分享卡 / 说明页 / 音效');
  ok(await until('#shareBtn',380),'战报播完自动结算');
  ok(S.last.token&&S.last.locked===true,'结算带 token 与冻结标记');
  ok(S.last.t===S.locked.stake,'结算读冻结（9999 篡改无效）');
  ok(S.balance===before-S.locked.stake+S.last.back,'余额未被污染');
  ok(!$('#stage').textContent.includes('undefined'),'结算页无 undefined');
  ok($('#stage').textContent.includes('11.12 封盘版'),'结算页版本标识');
  if(mode==='pre'){
    ok($('#stage').textContent.includes('平行宇宙抽象剧本'),'结算页抽象剧本声明');
    ok($('#stage').textContent.includes('平行宇宙模拟比分'),'结算比分牌改用抽象代号');
    ok($('#stage').textContent.includes('平行宇宙冠军'),'结算梗向播报抽象化');
  }else{
    ok($('#stage').textContent.includes('3:1'),'真实比分 3:1 生效');
    ok(!$('#stage').textContent.includes('平行宇宙模拟比分'),'真实结算不掺抽象比分牌');
  }
  const bal=S.balance,hit=S.last.hitN;
  W.__t.settle();W.__t.settle();
  ok(S.balance===bal&&S.last.hitN===hit,'重复 settle 幂等');
  $('#shareBtn').click();await wait(30);
  ok(($('#shareImg').getAttribute('src')||'').startsWith('data:image/png'),'PNG 分享卡');
  $('#infoBtn').click();
  const info=txt('#modal');
  ok(info.includes('虚拟抽象战报')&&info.includes('单版合并'),'说明页写明两种战报与合并');
  ok(info.includes('规则一屏')&&info.includes('纯 Canvas'),'说明页 P0 口径保留');
  $('#closeM').click();
  const btn=$('#sfxBtn');btn.click();
  ['tap','coin','select','tick','scene','confirm','win','lose','share','toggle'].forEach(n=>W.SFX.play(n));
  ok(W.__audioCalls.osc>=19&&W.__audioCalls.badRamp===0,'10 音效合成正常');
  btn.click();ok(!W.SFX.enabled,'再点关闭');
  ok(errors.length===0,'无 JS 运行时错误'+(errors.length?' -> '+errors.join('|'):''));
  console.log('PASS');
})().catch(e=>{console.error(e.message,'\nERRORS:',errors);process.exit(1);});
