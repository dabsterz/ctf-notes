'use strict';
const data = JSON.parse(document.getElementById('guide-data').textContent);
const $ = (id) => document.getElementById(id);
const esc = (value) => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const shortNames = {'00-start-here':'Start here','00-tool-rules':'Tools & rules','01-first-ten-minutes':'First ten minutes','02-web-exploitation':'Web exploitation','03-forensics':'Forensics','04-network':'Network','05-steganography':'Steganography','06-reverse-engineering':'Reverse engineering','07-cryptography':'Cryptography','08-binary-exploitation':'Binary exploitation','09-malware':'Malware','10-osint':'OSINT','11-miscellaneous':'Miscellaneous','12-excluded-and-advanced':'Excluded workflows','13-pwn-practice-atlas':'Pwn practice atlas','14-advanced-crypto':'Advanced cryptography','tool-matrix':'Complete tool matrix','source-coverage':'Source coverage'};
const sections = [];
Object.assign(shortNames, {'quickstart':'Quick reference', 'competition':'Competition setup', 'tool-chooser':'Choose a tool', 'recipes':'Recipe downloads', '03-forensics':'Digital forensics', '09-malware':'Malware analysis', '02-web-exploitation':'Web security'});
data.chapters.forEach(chapter => {
  const doc = new DOMParser().parseFromString(chapter.html, 'text/html');
  let section = null;
  Array.from(doc.body.children).forEach(node => {
    if (/^H[123]$/.test(node.tagName)) {
      section = {chapter: chapter.id, chapterTitle:chapter.note_path ? 'CPTS / '+chapter.note_path.replace(/\.md$/,'') : chapter.title, id:node.id, title:node.textContent, body:''};
      sections.push(section);
    }
    if (section) section.body += ' ' + node.textContent;
  });
});
const groupNames={'CONTEST SHORTCUTS':'Pinned pages','GET ORIENTED':'Getting started','COMPETITION CATEGORIES':'Competition categories','SUPPORTING REFERENCE':'Supporting reference','CPTS NOTES':"Vernon's CPTS notes",'REFERENCE':'Appendices'};
function cptsTree(chapters){
  const root={folders:new Map(),notes:[]};
  chapters.forEach(c=>{let folder=root;const parts=(c.note_path||'').split('/');parts.pop();parts.forEach(name=>{if(!folder.folders.has(name))folder.folders.set(name,{folders:new Map(),notes:[]});folder=folder.folders.get(name);});folder.notes.push(c);});
  const render=folder=>folder.notes.map(c=>`<a class="nav-link" href="#${esc(c.id)}" data-chapter="${esc(c.id)}">${esc(c.note_path?c.title:'All CPTS notes')}</a>`).join('')+Array.from(folder.folders,([name,child])=>`<details class="cpts-folder"><summary>${esc(name)}</summary>${render(child)}</details>`).join('');
  return render(root);
}
const navGroups=new Map();
data.chapters.forEach(c=>{if(!navGroups.has(c.group))navGroups.set(c.group,[]);navGroups.get(c.group).push(c);});
$('chapter-nav').innerHTML=Array.from(navGroups,([group,chapters])=>
  `<details class="nav-section" ${['CONTEST SHORTCUTS','COMPETITION CATEGORIES'].includes(group)?'open':''}><summary>${esc(groupNames[group])}<span class="nav-count">${group==='CPTS NOTES'?chapters.length-1:chapters.length}</span></summary>`+
  (group==='CPTS NOTES'?cptsTree(chapters):
  chapters.map(c=>`<a class="nav-link" href="#${esc(c.id)}" data-chapter="${esc(c.id)}"><span class="nav-glyph" aria-hidden="true">${c.group==='CONTEST SHORTCUTS'?'↗':'#'}</span>${esc(shortNames[c.id]||c.title)}</a>`).join(''))+'</details>'
).join('');
function notify(message){$('toast').textContent=message;$('toast').classList.add('visible');clearTimeout(notify.timer);notify.timer=setTimeout(()=>$('toast').classList.remove('visible'),2200);}
function setActive(id){document.querySelectorAll('.nav-link').forEach(a=>{if(a.dataset.chapter===id){a.setAttribute('aria-current','page');for(let parent=a.parentElement;parent;parent=parent.parentElement){if(parent.tagName==='DETAILS')parent.open=true;}}else a.removeAttribute('aria-current');});}
function closeMenu(){$('sidebar').classList.remove('open');$('menu-button').setAttribute('aria-expanded','false');$('main').inert=false;}
function addCopyButtons(){
  $('content').querySelectorAll('pre').forEach(pre=>{
    const code=pre.querySelector('code'); if(!code)return;
    const language=Array.from(code.classList).find(c=>c.startsWith('language-'))?.replace('language-','') || 'text';
    const lines=code.textContent.trimEnd().split('\n').length;
    const frame=document.createElement('div');frame.className='command-block'+(lines>18?' long-code':'');
    const toolbar=document.createElement('div');toolbar.className='code-toolbar';
    const label=document.createElement('span');label.className='code-language';label.textContent=language+' / '+lines+' '+(lines===1?'line':'lines');
    const actions=document.createElement('div');actions.className='code-actions';
    toolbar.append(label,actions);pre.replaceWith(frame);frame.append(toolbar,pre);
    pre.tabIndex=0;pre.setAttribute('aria-label',language+' code');
    if(lines>18){
      const expand=document.createElement('button');expand.className='expand-code';expand.textContent='Expand';expand.setAttribute('aria-expanded','false');
      expand.addEventListener('click',()=>{const opened=frame.classList.toggle('is-expanded');expand.setAttribute('aria-expanded',String(opened));expand.textContent=opened?'Collapse':'Expand';});actions.append(expand);
    }
    const button=document.createElement('button');button.className='copy-button';button.textContent='Copy';button.setAttribute('aria-label',`Copy ${language} block`);
    button.addEventListener('click',async()=>{
      const text=code.textContent;
      let success=false;
      try {if(navigator.clipboard){await navigator.clipboard.writeText(text);success=true;}} catch (_) {}
      if(!success){
        const area=document.createElement('textarea');area.value=text;area.style.position='fixed';area.style.opacity='0';document.body.appendChild(area);area.select();
        try{success=document.execCommand('copy');}catch(_){} area.remove();button.focus();
      }
      if(success){button.textContent='Copied';notify('Command copied. Check the placeholders before running.');setTimeout(()=>button.textContent='Copy',1800);}
      else {const range=document.createRange();range.selectNodeContents(code);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);notify('Text selected. Press Ctrl+C to copy.');}
    });actions.appendChild(button);
  });
}
function prepareReading(chapter){
  $('content').dataset.chapter=chapter.id;
  if(chapter.note_path){
    const meta=document.createElement('p');meta.className='cpts-provenance';
    meta.append(document.createTextNode(chapter.note_path.replace(/\.md$/,'')+' · Personal reference · '));
    const rules=document.createElement('a');rules.href='#competition--what-is-allowed';rules.textContent='Event tool rules';meta.append(rules);
    $('content').querySelector('h1').after(meta);
    $('content').querySelectorAll('img.cpts-image').forEach(img=>{
      const figure=document.createElement('figure');figure.className='cpts-figure';
      const button=document.createElement('button');button.type='button';button.textContent='Full size';button.setAttribute('aria-expanded','false');
      const viewport=document.createElement('div');viewport.className='cpts-image-viewport';viewport.tabIndex=0;viewport.setAttribute('aria-label',img.alt);
      const parent=img.parentElement;parent.before(figure);viewport.append(img);figure.append(button,viewport);if(!parent.textContent.trim()&&!parent.children.length)parent.remove();
      button.addEventListener('click',()=>{const full=figure.classList.toggle('full-size');button.textContent=full?'Fit width':'Full size';button.setAttribute('aria-expanded',String(full));});
    });
  }
  if(chapter.id==='quickstart'){
    const table=$('content').querySelector('.table-scroll');
    if(table){
      const index=document.createElement('nav');index.className='task-index';index.setAttribute('aria-label','Choose a route by what you have');
      table.querySelectorAll('tbody tr').forEach(row=>{
        const cells=row.querySelectorAll('td');if(cells.length!==2)return;
        const item=document.createElement('div');item.className='task-item';
        const label=document.createElement('strong');label.textContent=cells[0].textContent;
        const links=document.createElement('div');links.className='task-links';
        cells[1].querySelectorAll('a').forEach(a=>links.append(a.cloneNode(true)));
        item.append(label,links);index.append(item);
      });table.replaceWith(index);
    }
  }
  if(['quickstart','tool-chooser'].includes(chapter.id)){
    const intro=Array.from($('content').children).filter(n=>n.tagName==='P').slice(1,3);
    if(intro.length===2){const details=document.createElement('details');details.className='setup-note';const summary=document.createElement('summary');summary.textContent=chapter.id==='quickstart'?'Setup & competition notes':'Environment labels & examples';intro[0].before(details);details.append(summary,...intro);}
  }
  $('content').querySelectorAll('.table-scroll').forEach(table=>{table.tabIndex=0;table.setAttribute('role','region');table.setAttribute('aria-label','Scrollable reference table');});
}
let tocObserver;
function markToc(id){$('toc').querySelectorAll('a').forEach(a=>{if(a.getAttribute('href')==='#'+id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}
function createToc(){
  if(tocObserver)tocObserver.disconnect();
  const headings=Array.from($('content').querySelectorAll('h2'));
  $('toc').innerHTML=headings.length ? `<details class="outline-disclosure" ${window.innerWidth>1200?'open':''}><summary>On this page <span>${headings.length}</span></summary><nav aria-label="Page sections">`+headings.map(h=>`<a href="#${esc(h.id)}">${esc(h.textContent)}</a>`).join('')+'</nav></details>' : '';
  if('IntersectionObserver' in window){tocObserver=new IntersectionObserver(entries=>{const visible=entries.filter(e=>e.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top);if(visible.length)markToc(visible[0].target.id);},{rootMargin:'-120px 0px -55% 0px'});headings.forEach(h=>tocObserver.observe(h));}
}
let activeChapter='quickstart';
function showChapter(id,anchor){
  const fromMobileNav=window.innerWidth<=900&&$('sidebar').contains(document.activeElement);
  const chapter=data.chapters.find(c=>c.id===id) || data.chapters[0];activeChapter=chapter.id;
  $('content').innerHTML=chapter.html;
  $('reading-title').textContent=shortNames[chapter.id]||chapter.title;
  $('chapter-kind').textContent=groupNames[chapter.group]||'Field guide';
  document.title=(shortNames[chapter.id]||chapter.title)+' · Fieldnotes';
  setActive(chapter.id);prepareReading(chapter);addCopyButtons();createToc();closeMenu();
  if(fromMobileNav)$('content').focus({preventScroll:true});
  if(anchor){markToc(anchor);requestAnimationFrame(()=>document.getElementById(anchor)?.scrollIntoView());}
  else window.scrollTo({top:0,behavior:'instant'});
}
function route(){
  clearTimeout(search.timer);
  let raw;try{raw=decodeURIComponent(location.hash.slice(1));}catch(_){raw='quickstart';}
  if(raw==='content'){$('content').focus();$('content').scrollIntoView();return;}
  $('search').value='';
  if(raw==='tools'){showTools();return;}
  const id=raw.split('--')[0]||'quickstart';
  showChapter(id,raw.includes('--')?raw:null);
}
function highlight(text,words){
  const regex = new RegExp('('+words.map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','gi');
  return text.split(regex).map((part,i)=>i%2?'<mark>'+esc(part)+'</mark>':esc(part)).join('');
}
function search(){
  const query=$('search').value.trim();if(!query){showChapter(activeChapter);return;}
  closeMenu();
  const words=query.toLowerCase().split(/\s+/).filter(Boolean);
  const results=sections.map(s=>{
    const hay=(s.title+' '+s.chapterTitle+' '+s.body).toLowerCase();
    return {s,score:words.every(w=>hay.includes(w))?words.reduce((n,w)=>n+(s.title.toLowerCase().includes(w)?8:0)+(s.body.toLowerCase().includes(w)?2:0),0):0};
  }).filter(r=>r.score>0).sort((a,b)=>b.score-a.score);
  if(tocObserver)tocObserver.disconnect();$('toc').innerHTML='';setActive('');$('reading-title').textContent=`${results.length} matching sections`;$('chapter-kind').textContent='Search';
  $('content').innerHTML='<h1>Search results</h1><p>'+results.length+' sections match <strong>'+esc(query)+'</strong>. Showing '+Math.min(80,results.length)+'.</p>'+(results.length?results.slice(0,80).map(({s})=>{
    const position=Math.max(0,s.body.toLowerCase().indexOf(words[0])-75);const snippet=(position?'…':'')+s.body.slice(position,position+280).replace(/\s+/g,' ')+'…';
    return `<a class="result" href="#${esc(s.id||s.chapter)}"><span class="result-chapter">${esc(shortNames[s.chapter]||s.chapterTitle)}</span><strong>${highlight(s.title,words)}</strong><p>${highlight(snippet,words)}</p></a>`;
  }).join(''):'<div class="empty-state"><strong>No matching sections.</strong><p>Try fewer words or a synonym: “JWT”, “packet”, “memory”, “XOR”, “radare2”. Tool lookup can also search installation notes.</p><a href="#tools">Open tool lookup →</a></div>');
}
function showTools(){
  if(tocObserver)tocObserver.disconnect();$('toc').innerHTML='';setActive('tool-matrix');closeMenu();$('chapter-kind').textContent='Reference';$('reading-title').textContent='282 workbook entries';
  $('content').innerHTML='<h1>Tool inventory</h1><p>Approval and installation are separate facts. Search the supplied list before choosing a tool. Windows entries may be installed inside WSL; check the location.</p><div class="tool-controls"><label>Tool or note<input id="tool-query" type="search" placeholder="e.g. radare2, symbols, FUSE"></label><label>Environment<select id="tool-platform"><option value="">All environments</option><option>Kali</option><option>Windows / WSL</option></select></label><label>Status<select id="tool-status"><option value="">All entries</option><option>Approved</option><option>Unapproved</option></select></label></div><p id="tool-count" role="status"></p><div id="tool-results"></div>';
  function update(){
    const query=$('tool-query').value.toLowerCase().trim();
    const found=data.tools.filter(t=>(!$('tool-platform').value||t.platform===$('tool-platform').value)&&(!$('tool-status').value||t.status===$('tool-status').value)&&(!query||[t.name,t.notes,t.location,t.version].join(' ').toLowerCase().includes(query)));
    $('tool-count').textContent=found.length+' matching entries';
    $('tool-results').innerHTML=found.map(t=>`<section class="tool-card"><span class="badge ${t.status==='Unapproved'?'rejected':''}">${esc(t.status)} · ${esc(t.platform)}</span><h2>${esc(t.name)}</h2>${t.version?'<p><strong>Recorded version:</strong> '+esc(t.version)+'</p>':''}${t.location?'<p><strong>Location:</strong> '+esc(t.location)+'</p>':''}${t.notes?'<p>'+esc(t.notes)+'</p>':''}<small>${esc(t.sheet)}!${esc(t.cell)}</small></section>`).join('')||'<div class="empty-state">No entries match these filters. A missing entry does not establish approval.</div>';
  }
  ['tool-query','tool-platform','tool-status'].forEach(id=>$(id).addEventListener('input',update));update();window.scrollTo({top:0,behavior:'instant'});
}
$('search').addEventListener('input',()=>{clearTimeout(search.timer);search.timer=setTimeout(search,120);});
$('tools-button').addEventListener('click',()=>{if(location.hash==='#tools')showTools();else location.hash='tools';});
$('print-button').addEventListener('click',()=>window.print());
$('download-button').addEventListener('click',()=>{
  const url=URL.createObjectURL(new Blob([data.markdown],{type:'text/markdown;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='Cyber-SEA-Game-HANDBOOK.md';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('Markdown handbook downloaded.');
});
$('menu-button').addEventListener('click',()=>{const open=$('sidebar').classList.toggle('open');$('menu-button').setAttribute('aria-expanded',String(open));$('main').inert=open&&window.innerWidth<=900;});
$('nav-backdrop').addEventListener('click',()=>{closeMenu();$('menu-button').focus();});
function focusMode(enabled){document.body.classList.toggle('focus-mode',enabled);$('focus-button').setAttribute('aria-pressed',String(enabled));$('focus-button').textContent=enabled?'Show panels':'Focus';closeMenu();}
$('focus-button').addEventListener('click',()=>focusMode(!document.body.classList.contains('focus-mode')));
function readingSize(value){const size=['16','18','20'].includes(value)?value:'16';document.documentElement.style.setProperty('--reader-size',size+'px');$('text-size').value=size;}
try{readingSize(localStorage.getItem('ctf-fieldnotes-size'));}catch(_){readingSize('16');}
$('text-size').addEventListener('change',()=>{readingSize($('text-size').value);try{localStorage.setItem('ctf-fieldnotes-size',$('text-size').value);}catch(_){} });
function theme(value){document.documentElement.dataset.theme=value;$('theme-button').textContent=value==='dark'?'Light':'Dark';$('theme-button').setAttribute('aria-label','Switch to '+(value==='dark'?'light':'dark')+' theme');}
try{const saved=localStorage.getItem('ctf-fieldnotes-theme');theme(saved==='light'?'light':'dark');}catch(_){theme('dark');}
$('theme-button').addEventListener('click',()=>{const value=document.documentElement.dataset.theme==='dark'?'light':'dark';theme(value);try{localStorage.setItem('ctf-fieldnotes-theme',value);}catch(_){} });
document.addEventListener('keydown',event=>{
  if(event.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){event.preventDefault();$('search').focus();}
  if(event.key==='Escape'){
    if($('sidebar').classList.contains('open')){closeMenu();$('menu-button').focus();}
    else if($('search').value||document.activeElement===$('search')){clearTimeout(search.timer);$('search').value='';route();$('search').blur();}
    document.querySelectorAll('.page-menu[open]').forEach(menu=>menu.open=false);
  }
});
let printDetails=[];
window.addEventListener('beforeprint',()=>{printDetails=Array.from($('content').querySelectorAll('details')).map(d=>[d,d.open]);printDetails.forEach(([d])=>d.open=true);});
window.addEventListener('afterprint',()=>{printDetails.forEach(([d,open])=>d.open=open);printDetails=[];});
document.addEventListener('click',event=>{
  if(event.target.closest('a[href="CPTS-NOTES.md"]')&&data.cptsMarkdown){
    event.preventDefault();const url=URL.createObjectURL(new Blob([data.cptsMarkdown],{type:'text/markdown;charset=utf-8'}));
    const a=document.createElement('a');a.href=url;a.download='CPTS-NOTES.md';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);return;
  }
  const download=event.target.closest('a[href^="recipes/"]');
  if(download){
    const name=download.getAttribute('href').slice('recipes/'.length);
    if(Object.prototype.hasOwnProperty.call(data.recipes,name)){
      event.preventDefault();
      const url=URL.createObjectURL(new Blob([data.recipes[name]],{type:'text/plain;charset=utf-8'}));
      const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
      setTimeout(()=>URL.revokeObjectURL(url),1000);notify('Downloaded '+name+'. Save it in your recipes folder.');
      return;
    }
  }
  const link=event.target.closest('a[href^="#"]');if(!link)return;
  if(link.hash===location.hash){event.preventDefault();route();}
});
window.addEventListener('hashchange',route);
window.addEventListener('resize',()=>{if(window.innerWidth>900)closeMenu();});
if('ResizeObserver' in window){new ResizeObserver(()=>document.documentElement.style.setProperty('--bar-height',Math.ceil(document.querySelector('.topbar').getBoundingClientRect().height)+'px')).observe(document.querySelector('.topbar'));}
route();
