const { chromium } = require('/usr/local/lib/node_modules/playwright');
const fs = require('fs');
const mode = process.argv[2] || 'pre';
const ROOT = '/data/workspace';
let file = '哈士喵决赛押宝夜AVG.html';
if (mode === 'completed') {
  let h = fs.readFileSync(ROOT + '/' + file, 'utf8');
  const r = {champion:'BLG',score:'3:1',bw:3,rw:1,firstblood:'GEN',dragonflip:'BLG',
             firstbaron:'BLG',fullseries:'no',note:'回归用例，非真实赛果'};
  h = h.replace(/("result":)(null)/, '$1'+JSON.stringify(r))
       .replace(/("state":)"unstarted"/, '$1"completed"')
       .replace(/("score":)null/, '$1"3:1"');
  file = '_merge2/_completed_preview.html';
  fs.writeFileSync(ROOT + '/' + file, h);
}
const URL = 'file://' + ROOT + '/' + encodeURIComponent(file).replace(/%2F/g, '/');
(async()=>{
  const b=await chromium.launch({headless:true,executablePath:'/usr/local/bin/chromium',
    args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
  const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
  const errs=[],warns=[];
  p.on('pageerror',e=>errs.push('pageerror: '+e.message));
  p.on('console',m=>{if(m.type()==='error')errs.push(m.text());if(m.type()==='warning')warns.push(m.text());});
  await p.addInitScript(()=>{const raw=window.setTimeout.bind(window);
    window.setTimeout=(fn,ms,...r)=>raw(fn,Math.min(ms||0,2),...r);window.setInterval=()=>0;});
  await p.goto(URL);
  await p.evaluate(()=>{try{localStorage.clear();}catch(e){}});
  await p.reload();await p.waitForTimeout(600);
  const tag=mode==='pre'?'abstract':'real';
  const shot=async n=>{await p.evaluate(()=>{try{window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0;}catch(e){}});
    await p.waitForTimeout(60);await p.screenshot({path:ROOT+'/_m_'+tag+'_'+n+'.png'});};
  const until=async sel=>{for(let i=0;i<280;i++){if(await p.locator(sel).count())return true;
    if(await p.locator('#dlg').count())await p.locator('#dlg').click();await p.waitForTimeout(10);}return false;};
  const ok=(c,m)=>{if(!c)throw new Error('FAIL: '+m);console.log('  ok - '+m);};

  console.log('\n=== 真机 |',mode,'===');
  ok((await p.evaluate(()=>({on:window.SFX.enabled,ctx:window.SFX.ctxCreated}))).on===false,'默认音效关');
  await shot('01_title');
  const title=await p.locator('#stage').textContent();
  ok(title.includes(mode==='pre'?'赛前：虚拟抽象战报':'赛后：真实口径战报'),'标题战报口径正确');
  await p.click('#sfxBtn');await p.waitForTimeout(100);
  await p.click('#startBtn');await p.waitForTimeout(180);
  await until('.choice');await p.locator('.choice').nth(0).click();
  await until('#betScroll');await shot('02_bet');
  await p.click('.opt[data-g="champion"][data-o="blue"]');
  await p.click('.opt[data-g="firstblood"][data-o="blue"]');
  await p.click('.opt[data-g="dragonflip"][data-o="blue"]');
  await p.click('.opt[data-g="fullseries"][data-o="yes"]');
  await p.waitForTimeout(140);
  await p.click('#goBtn');await p.waitForTimeout(160);
  await shot('03_summary');
  await p.click('#sumOk');await p.waitForTimeout(140);
  await until('.choice');await p.locator('.choice').nth(0).click();
  await p.waitForTimeout(200);
  await shot('04_live_open');
  // 推进到「一血」与「龙坑/大龙」条，看抽象名场面差分
  for(let i=0;i<2;i++){if(await p.locator('#dlg').count())await p.locator('#dlg').click();await p.waitForTimeout(90);}
  await shot('05_live_scene');
  const feedTxt=await p.evaluate(()=>{try{return (JSON.parse(localStorage.getItem('hashimiao-s-final-avg-v2')).feed||[]).map(f=>f.t||'').join(' ');}catch(e){return '';}});
  if(mode==='pre')ok(feedTxt.includes('平行宇宙')&&feedTxt.includes('虚拟核对'),'真机生成抽象战报（平行宇宙 + 虚拟核对）');
  else ok(feedTxt.includes('导播信号接入')&&!feedTxt.includes('平行宇宙'),'真机生成真实口径战报');
  await until('#shareBtn');await p.waitForTimeout(260);
  await shot('06_result');
  const res=await p.locator('#stage').textContent();
  ok(res.includes('11.12 封盘版'),'结算版本标识');
  if(mode==='pre')ok(res.includes('平行宇宙抽象剧本'),'结算抽象声明');
  else ok(res.includes('3:1'),'真实比分');
  await p.click('#shareBtn');await p.waitForTimeout(480);
  const data=await p.locator('#shareImg').getAttribute('src');
  fs.writeFileSync(ROOT+'/_m_'+tag+'_card.png',Buffer.from(data.split(',')[1],'base64'));
  await p.click('#infoBtn');await p.waitForTimeout(200);
  const info=await p.locator('#modal').textContent();
  ok(info.includes('虚拟抽象战报')&&info.includes('单版合并'),'说明页双战报 + 合并');
  await shot('07_info');
  await p.click('#closeM');
  console.log(mode,'page errors:',errs.length?errs:'none','| warnings:',warns.length);
  if(errs.length)throw new Error('JS 错误');
  await b.close();
})().catch(e=>{console.error('FAILED:',e.message);process.exit(1);});
