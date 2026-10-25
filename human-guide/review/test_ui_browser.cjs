// Local-file Chrome checks. Development dependency stays outside the reader ZIP.
// node test_ui_browser.cjs PATH_TO_PLAYWRIGHT_CORE [PATH_TO_CHROME]
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.argv[2]);
const root=path.resolve(__dirname,'..'),out=path.join(__dirname,'ui');
const requests=[],errors=[],checks=[];
function luminance(hex){const c=hex.trim().replace('#','').match(/.{2}/g).map(v=>parseInt(v,16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722;}
function contrast(a,b){const values=[luminance(a),luminance(b)].sort((a,b)=>b-a);return (values[0]+.05)/(values[1]+.05);}
(async()=>{
  fs.mkdirSync(out,{recursive:true});
  const baseline=JSON.parse(fs.readFileSync(path.join(out,'content-before.json'),'utf8'));
  for(const [name,hash] of Object.entries(baseline).filter(([name])=>name!=='HANDBOOK.md'))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,name))).digest('hex'),hash,'Reader content changed: '+name);
  checks.push('27 baseline guide/helper files unchanged; combined HANDBOOK extended with CPTS notes');
  const browser=await chromium.launch({executablePath:process.argv[3]||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
  try{
    const context=await browser.newContext({viewport:{width:1440,height:1000},offline:true,reducedMotion:'reduce'});
    const page=await context.newPage();
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
    await page.goto(pathToFileURL(path.join(root,'index.html')).href);
    const route=async id=>{await page.evaluate(id=>location.hash=id,id);await page.waitForFunction(id=>document.getElementById('content').dataset.chapter===id,id);};
    const noOverflow=async label=>{assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),label+': whole-page horizontal overflow');};
    assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
    assert.equal(await page.locator('.task-item').count(),8);
    assert.equal(await page.locator('#content>p').first().evaluate(p=>getComputedStyle(p).fontSize),'16px');
    await noOverflow('desktop');
    await page.screenshot({path:path.join(out,'desktop-dark.png')});
    await page.locator('.task-links a[href="#quickstart--web-paths"]').click();
    await page.waitForFunction(()=>document.getElementById('quickstart--web-paths').getBoundingClientRect().top>=60);
    await page.screenshot({path:path.join(out,'command-view.png')});
    checks.push('desktop dark rendering, readable body and direct task navigation');
    await page.locator('#focus-button').click();
    assert.equal(await page.locator('#sidebar').isVisible(),false);
    assert.equal(await page.locator('#toc').isVisible(),false);
    await page.locator('#text-size').selectOption('18');
    assert.equal(await page.locator('#content>p').first().evaluate(p=>getComputedStyle(p).fontSize),'18px');
    await page.screenshot({path:path.join(out,'focused-reading.png')});
    await page.locator('#focus-button').click();
    await page.locator('#text-size').selectOption('16');
    checks.push('focus hides panels and text-size setting changes rendered type');
    await route('06-reverse-engineering');
    const expand=page.locator('.expand-code').first();
    await expand.click();assert.equal(await expand.getAttribute('aria-expanded'),'true');
    await expand.click();assert.equal(await expand.getAttribute('aria-expanded'),'false');
    checks.push('long script expands and collapses in Chrome');
    const paletteResults={};
    for(const mode of ['dark','light']){
      if(await page.locator('html').getAttribute('data-theme')!==mode)await page.locator('#theme-button').click();
      const colors=await page.evaluate(()=>{const s=getComputedStyle(document.documentElement);return Object.fromEntries(['bg','paper','sidebar','raised','ink','muted','accent','accent-soft','code','code-ink'].map(n=>[n,s.getPropertyValue('--'+n).trim()]));});
      // Expand three-digit tokens before measuring.
      Object.keys(colors).forEach(k=>{if(colors[k].length===4)colors[k]='#'+colors[k].slice(1).split('').map(x=>x+x).join('');});
      const pairs=[['ink','bg'],['ink','paper'],['muted','bg'],['muted','sidebar'],['muted','paper'],['accent','bg'],['accent','accent-soft'],['code-ink','code']];
      paletteResults[mode]=Object.fromEntries(pairs.map(([fg,bg])=>{const ratio=contrast(colors[fg],colors[bg]);assert.ok(ratio>=4.5,mode+' '+fg+'/'+bg+' '+ratio);return [fg+'/'+bg,Number(ratio.toFixed(2))];}));
    }
    await route('quickstart');
    await page.screenshot({path:path.join(out,'desktop-light.png')});
    await page.locator('#theme-button').click();
    await route('tool-chooser');
    await page.screenshot({path:path.join(out,'tool-chooser.png')});
    checks.push('both themes pass 4.5:1 for eight primary text/background combinations');
    const chapters=await page.evaluate(()=>JSON.parse(document.getElementById('guide-data').textContent).chapters.map(c=>c.id));
    for(const width of [1440,768,320]){
      await page.setViewportSize({width,height:1000});
      for(const id of chapters){
        await route(id);await noOverflow(width+' '+id);
        const preserved=await page.evaluate(id=>{
          const c=JSON.parse(document.getElementById('guide-data').textContent).chapters.find(c=>c.id===id);
          const original=new DOMParser().parseFromString(c.html,'text/html');
          return JSON.stringify(Array.from(original.querySelectorAll('pre code'),x=>x.textContent))===JSON.stringify(Array.from(document.querySelectorAll('#content pre code'),x=>x.textContent));
        },id);
        assert.ok(preserved,'Changed code text: '+id);
      }
    }
    checks.push('all '+chapters.length+' pages reflow at 1440, 768 and 320px; all code text preserved');
    await page.setViewportSize({width:1440,height:1000});
    await route('cpts');
    assert.equal(await page.locator('#chapter-nav>.nav-section').count(),6);
    await page.screenshot({path:path.join(out,'cpts-overview.png')});
    const imageNote=await page.evaluate(()=>JSON.parse(document.getElementById('guide-data').textContent).chapters.find(c=>c.note_path&&c.html.includes('<img')).id);
    await route(imageNote);
    assert.ok(await page.locator('.nav-link[aria-current="page"]').evaluate(a=>{for(let p=a.parentElement;p;p=p.parentElement){if(p.tagName==='DETAILS'&&!p.open)return false;}return true;}));
    const firstImage=page.locator('.cpts-image').first();
    await firstImage.scrollIntoViewIfNeeded();
    await page.waitForFunction(()=>Array.from(document.querySelectorAll('.cpts-image')).some(img=>img.naturalWidth>0));
    await page.locator('.cpts-figure>button').first().click();
    assert.equal(await page.locator('.cpts-figure>button').first().getAttribute('aria-expanded'),'true');
    await noOverflow('full size CPTS image');
    await page.locator('.cpts-figure>button').first().click();
    await page.screenshot({path:path.join(out,'cpts-note.png')});
    checks.push('CPTS folder ancestors reveal active note; screenshot loads offline and full-size view stays within reader');
    await page.setViewportSize({width:390,height:844});await route('quickstart');
    await page.screenshot({path:path.join(out,'mobile-dark.png')});
    await page.locator('#menu-button').click();
    assert.equal(await page.locator('#sidebar').isVisible(),true);
    await page.screenshot({path:path.join(out,'mobile-navigation.png')});
    await page.locator('.nav-link[href="#competition"]').click();
    await page.waitForFunction(()=>document.getElementById('content').dataset.chapter==='competition');
    assert.equal(await page.locator('#menu-button').getAttribute('aria-expanded'),'false');
    assert.equal(await page.locator('#main').evaluate(n=>n.inert),false);
    await page.locator('#menu-button').click();await page.keyboard.press('Escape');
    assert.equal(await page.locator('#menu-button').getAttribute('aria-expanded'),'false');
    await page.locator('#menu-button').click();
    await page.locator('#search').fill('RSA');
    await page.locator('a.result').first().waitFor();
    assert.equal(await page.locator('#menu-button').getAttribute('aria-expanded'),'false');
    assert.equal(await page.locator('#main').evaluate(n=>n.inert),false);
    await page.locator('a.result[href="#quickstart--rsa"]').click();
    await page.waitForFunction(()=>location.hash==='#quickstart--rsa');
    checks.push('mobile drawer opens, navigates and closes with Escape');
    checks.push('search from an open mobile drawer exposes clickable results');
    await page.setViewportSize({width:320,height:1000});
    await page.locator('#text-size').selectOption('20');
    for(const id of ['quickstart','competition','tool-chooser']){await route(id);await noOverflow('20px '+id);}
    await page.addStyleTag({content:'*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}'});
    for(const id of ['quickstart','competition','tool-chooser']){
      await route(id);await noOverflow('spacing override '+id);
      assert.ok(await page.evaluate(()=>document.getElementById('main').getBoundingClientRect().top+scrollY>=document.querySelector('.topbar').getBoundingClientRect().bottom-1),'Header overlaps reading area');
    }
    await page.screenshot({path:path.join(out,'spacing-320.png')});
    checks.push('20px text and WCAG spacing override reflow on three key pages at 320px');
    // A new page avoids carrying the synthetic spacing override into print checks.
    const printPage=await context.newPage();
    await printPage.goto(pathToFileURL(path.join(root,'index.html')).href);
    await printPage.evaluate(()=>dispatchEvent(new Event('beforeprint')));
    await printPage.emulateMedia({media:'print'});
    assert.equal(await printPage.locator('.setup-note').evaluate(d=>d.open),true);
    assert.equal(await printPage.locator('.setup-note p').first().evaluate(p=>getComputedStyle(p).color),'rgb(0, 0, 0)');
    assert.equal(await printPage.locator('.reading-path p').evaluate(p=>getComputedStyle(p).color),'rgb(0, 0, 0)');
    assert.equal(await printPage.locator('.topbar').isVisible(),false);
    assert.equal(await printPage.locator('.task-index').isVisible(),true);
    await printPage.close();
    checks.push('print reveals setup notes and uses dark text on light paper');
    assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
    checks.push('no page exceptions or HTTP requests while offline');
    const result={browser:'Chrome '+browser.version(),html_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'index.html'))).digest('hex'),passed:checks.length,checks,contrast:paletteResults,errors,external_requests:requests,
      scope:'Automated local-file Chrome rendering/interaction. Screenshots inspected separately. Contrast checks cover primary pairs, not a full accessibility certification. No event infrastructure or challenge commands executed.'};
    fs.writeFileSync(path.join(__dirname,'ui-validation.json'),JSON.stringify(result,null,2)+'\n');
    console.log(JSON.stringify(result,null,2));
    await context.close();
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
