/* DOM integration, not a real-browser layout or file-dialog test.
   Usage: node test_site.cjs ABSOLUTE_PATH_TO_JSDOM_MODULE (tested with jsdom 26.1.0).
   Install developer test dependencies outside the reader ZIP. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {JSDOM, ResourceLoader, VirtualConsole} = require(process.argv[2] || 'jsdom');
const root = path.resolve(__dirname,'..');
const errors=[],requests=[],downloads=[],blobs=new Map();
let copied='', printed=0;
class Offline extends ResourceLoader {
  fetch(url){requests.push(url);return Promise.reject(new Error('Unexpected resource request: '+url));}
}
const consoleProxy = new VirtualConsole();
consoleProxy.on('jsdomError',e=>errors.push(String(e)));
const dom = new JSDOM(fs.readFileSync(path.join(root,'index.html'),'utf8'),{
  url:'file:///offline-guide/index.html',runScripts:'dangerously',pretendToBeVisual:true,
  resources:new Offline(),virtualConsole:consoleProxy,
  beforeParse(window){
    window.scrollTo=()=>{};
    window.HTMLElement.prototype.scrollIntoView=()=>{};
    window.print=()=>{printed++;};
    window.fetch=()=>{throw new Error('No network is allowed');};
    window.URL.createObjectURL=blob=>{const url='blob:offline-'+blobs.size;blobs.set(url,blob);return url;};
    window.URL.revokeObjectURL=()=>{};
    Object.defineProperty(window.navigator,'clipboard',{value:{writeText:async text=>{copied=text;}}});
    window.HTMLAnchorElement.prototype.click=function(){
      if(this.download){downloads.push({name:this.download,blob:blobs.get(this.href)});}
      else this.dispatchEvent(new window.MouseEvent('click',{bubbles:true,cancelable:true}));
    };
  }
});
const {window:w}=dom,d=w.document;
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const go=async hash=>{w.location.hash=hash;await delay(30);};
const blobText=blob=>new Promise((resolve,reject)=>{const reader=new w.FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsText(blob);});
(async()=>{
  const checks=[];
  await delay(30);
  assert.equal(d.querySelector('#content h1').textContent,'Contest quick reference');
  checks.push('default route is short guide');
  assert.equal(d.documentElement.dataset.theme,'dark');
  assert.equal(d.querySelectorAll('.task-index .task-item').length,8);
  const focus=d.getElementById('focus-button');
  focus.click();
  assert.equal(focus.getAttribute('aria-pressed'),'true');
  assert.ok(d.body.classList.contains('focus-mode'));
  focus.click();
  assert.equal(focus.getAttribute('aria-pressed'),'false');
  const textSize=d.getElementById('text-size');
  textSize.value='18';textSize.dispatchEvent(new w.Event('change',{bubbles:true}));
  assert.equal(d.documentElement.style.getPropertyValue('--reader-size'),'18px');
  await go('14-advanced-crypto');
  assert.equal(d.querySelector('.nav-link[aria-current="page"]').closest('details').open,true);
  assert.equal(d.documentElement.style.getPropertyValue('--reader-size'),'18px');
  textSize.value='16';textSize.dispatchEvent(new w.Event('change',{bubbles:true}));
  checks.push('dark workspace, task routes, focus, text size and hidden-group deep link');
  await go('06-reverse-engineering');
  assert.equal(d.querySelector('.deep-reference').open,false);
  const expand=d.querySelector('.expand-code');
  assert.ok(expand);expand.click();
  assert.equal(expand.getAttribute('aria-expanded'),'true');
  assert.ok(expand.closest('.command-block').classList.contains('is-expanded'));
  expand.click();assert.equal(expand.getAttribute('aria-expanded'),'false');
  await go('quickstart');
  const setup=d.querySelector('.setup-note');assert.equal(setup.open,false);
  w.dispatchEvent(new w.Event('beforeprint'));assert.equal(setup.open,true);
  w.dispatchEvent(new w.Event('afterprint'));assert.equal(setup.open,false);
  checks.push('long script expansion and print restores collapsed setup content');
  await go('02-web-exploitation--1-establish-a-baseline-you-can-reproduce');
  assert.equal(d.querySelector('.deep-reference').open,true);
  assert.ok(d.getElementById('02-web-exploitation--1-establish-a-baseline-you-can-reproduce'));
  await go('02-web-exploitation');
  assert.equal(d.querySelector('.deep-reference').open,false);
  assert.ok([...d.querySelectorAll('#toc a')].every(a=>!a.hash.includes('--1-establish')));
  d.getElementById('search').value='Establish a baseline';
  d.getElementById('search').dispatchEvent(new w.Event('input',{bubbles:true}));await delay(160);
  assert.ok(d.querySelector('a.result[href="#02-web-exploitation--1-establish-a-baseline-you-can-reproduce"]'));
  checks.push('full reference hidden by default, searchable and opened by old deep links');
  const currentData=JSON.parse(d.getElementById('guide-data').textContent);
  assert.deepEqual(currentData.chapters.filter(c=>c.group==='COMPETITION CATEGORIES').map(c=>c.id),
    ['03-forensics','09-malware','02-web-exploitation','06-reverse-engineering','10-osint','07-cryptography','11-miscellaneous']);
  assert.match(d.getElementById('chapter-nav').textContent,/Competition categories/i);
  assert.doesNotMatch(d.getElementById('chapter-nav').textContent,/CORE SUBJECTS/);
  await go('competition');
  assert.equal(d.querySelector('#content h1').textContent,'Competition setup and rules');
  assert.ok(d.querySelector('#content a[href="sources/practice-environment.pdf#page=7"]'));
  assert.match(d.getElementById('content').textContent,/2 vCPU, 8 GiB RAM, 40 GB/);
  assert.match(d.getElementById('content').textContent,/Practice-session reference only/);
  checks.push('seven PDF categories and competition setup route with offline source link');
  await go('tool-chooser');
  assert.equal(d.querySelectorAll('#content table').length,11);
  const gadget=[...d.querySelectorAll('#content code')].find(x=>x.textContent.includes('ROPgadget --binary'));
  assert.equal(gadget.textContent,"ROPgadget --binary challenge --only 'pop|ret'");
  checks.push('all category tables and literal pipe command render');
  const originalWidth=w.innerWidth;w.innerWidth=390;
  d.getElementById('menu-button').click();assert.equal(d.getElementById('main').inert,true);
  d.getElementById('search').value='RSA';
  d.getElementById('search').dispatchEvent(new w.Event('input',{bubbles:true}));
  await delay(160);
  assert.equal(d.getElementById('main').inert,false,'Mobile search must make its results interactive');
  assert.equal(d.getElementById('menu-button').getAttribute('aria-expanded'),'false');w.innerWidth=originalWidth;
  assert.ok(d.querySelector('a.result[href="#quickstart--rsa"]'));
  await go('quickstart--rsa');
  assert.ok(d.getElementById('quickstart--rsa'));
  const pre=[...d.querySelectorAll('#content pre')].find(x=>x.querySelector('code').textContent.includes('recipes/rsa.py'));
  pre.closest('.command-block').querySelector('.copy-button').click();await delay(10);
  assert.equal(copied,pre.querySelector('code').textContent);
  checks.push('search result, section route and clipboard text');
  await go('recipes');
  d.querySelector('a[href="recipes/rsa.py"]').click();await delay(10);
  assert.equal(downloads.at(-1).name,'rsa.py');
  assert.equal(await blobText(downloads.at(-1).blob),fs.readFileSync(path.join(root,'recipes/rsa.py'),'utf8').replace(/\r\n/g,'\n'));
  checks.push('offline recipe download contains exact source');
  d.getElementById('download-button').click();
  const payload=JSON.parse(d.getElementById('guide-data').textContent);
  assert.equal(await blobText(downloads.at(-1).blob),payload.markdown);
  checks.push('Markdown download contains full current handbook');
  await go('cpts');
  // Dispatch a real click: the offline handler creates a second, Blob-backed anchor.
  d.querySelector('a[href="CPTS-NOTES.md"]').dispatchEvent(new w.MouseEvent('click',{bubbles:true,cancelable:true}));
  assert.equal(downloads.at(-1).name,'CPTS-NOTES.md');
  assert.equal(await blobText(downloads.at(-1).blob),payload.cptsMarkdown);
  const note=payload.chapters.find(c=>c.note_path&&c.html.includes('<img'));
  await go(note.id);
  assert.ok(d.querySelector('.cpts-image').src.startsWith('data:image/png;base64,'));
  assert.ok(d.querySelector('.cpts-provenance').textContent.includes(note.note_path.replace(/\.md$/,'')));
  for(let p=d.querySelector('.nav-link[aria-current="page"]').parentElement;p;p=p.parentElement){if(p.tagName==='DETAILS')assert.equal(p.open,true);}
  d.getElementById('search').value='CPTS '+note.title;
  d.getElementById('search').dispatchEvent(new w.Event('input',{bubbles:true}));await delay(160);
  assert.ok([...d.querySelectorAll('.result-chapter')].some(n=>n.textContent.includes(note.note_path.replace(/\.md$/,''))));
  checks.push('CPTS Markdown download, offline image, nested navigation and path-aware search');
  await go('tools');
  d.getElementById('tool-query').value='radare2';
  d.getElementById('tool-platform').value='Kali';
  d.getElementById('tool-query').dispatchEvent(new w.Event('input',{bubbles:true}));
  assert.equal(d.querySelectorAll('.tool-card').length,1);
  assert.match(d.querySelector('.tool-card').textContent,/C123/);
  checks.push('tool lookup filters and workbook reference');
  d.getElementById('menu-button').click();
  assert.equal(d.getElementById('menu-button').getAttribute('aria-expanded'),'true');
  d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
  assert.equal(d.getElementById('menu-button').getAttribute('aria-expanded'),'false');
  d.getElementById('print-button').click();assert.equal(printed,1);
  checks.push('menu state, Escape and print action');
  assert.deepEqual(requests,[]);assert.deepEqual(errors,[]);
  checks.push('no external resource requests or DOM runtime errors');
  const result={passed:checks.length,checks,scope:'jsdom DOM integration; separate Chrome layout checks in ui-validation.json. Organizer tools are not tested here.'};
  fs.writeFileSync(path.join(__dirname,'site-validation.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result,null,2));
  w.close();
})().catch(e=>{console.error(e);w.close();process.exitCode=1;});
