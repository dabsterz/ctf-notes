'use strict';
const data = JSON.parse(document.getElementById('guide-data').textContent);
const $ = (id) => document.getElementById(id);
const esc = (value) => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const shortNames = {'00-start-here':'Start here','00-tool-rules':'Tools & rules','01-first-ten-minutes':'First ten minutes','02-web-exploitation':'Web exploitation','03-forensics':'Forensics','04-network':'Network','05-steganography':'Steganography','06-reverse-engineering':'Reverse engineering','07-cryptography':'Cryptography','08-binary-exploitation':'Binary exploitation','09-malware':'Malware','10-osint':'OSINT','11-miscellaneous':'Miscellaneous','12-excluded-and-advanced':'Excluded workflows','13-pwn-practice-atlas':'Pwn practice atlas','14-advanced-crypto':'Advanced cryptography','tool-matrix':'Complete tool matrix','source-coverage':'Source coverage'};
const sections = [];
data.chapters.forEach(chapter => {
  const doc = new DOMParser().parseFromString(chapter.html, 'text/html');
  let section = null;
  Array.from(doc.body.children).forEach(node => {
    if (/^H[123]$/.test(node.tagName)) {
      section = {chapter: chapter.id, chapterTitle:chapter.title, id:node.id, title:node.textContent, body:''};
      sections.push(section);
    }
    if (section) section.body += ' ' + node.textContent;
  });
});
let previousGroup = '';
$('chapter-nav').innerHTML = data.chapters.map(chapter => {
  const number = parseInt(chapter.id, 10);
  const group = chapter.id.startsWith('00') || number === 1 ? 'GET ORIENTED' : number >= 2 && number <= 7 ? 'CORE SUBJECTS' : Number.isFinite(number) ? 'GO FURTHER' : 'REFERENCE';
  const label = group !== previousGroup ? `<div class="nav-group">${group}</div>` : '';
  previousGroup = group;
  return label + `<a class="nav-link" href="#${chapter.id}" data-chapter="${chapter.id}"><span class="nav-number">${Number.isFinite(number) ? String(number).padStart(2,'0') : '↗'}</span>${esc(shortNames[chapter.id] || chapter.title)}</a>`;
}).join('');
function notify(message){$('toast').textContent=message;$('toast').classList.add('visible');clearTimeout(notify.timer);notify.timer=setTimeout(()=>$('toast').classList.remove('visible'),2200);}
function setActive(id){document.querySelectorAll('.nav-link').forEach(a=>{if(a.dataset.chapter===id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});}
function closeMenu(){$('sidebar').classList.remove('open');$('menu-button').setAttribute('aria-expanded','false');}
function addCopyButtons(){
  $('content').querySelectorAll('pre').forEach(pre=>{
    const code=pre.querySelector('code'); if(!code)return;
    const language=Array.from(code.classList).find(c=>c.startsWith('language-'))?.replace('language-','') || 'text';
    pre.dataset.language=language;
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
    });pre.appendChild(button);
  });
}
function createToc(){
  const headings=Array.from($('content').querySelectorAll('h2'));
  $('toc').innerHTML=headings.length ? '<h2>ON THIS PAGE</h2>'+headings.map(h=>`<a href="#${esc(h.id)}">${esc(h.textContent)}</a>`).join('') : '';
}
let activeChapter='00-start-here';
function showChapter(id,anchor){
  const chapter=data.chapters.find(c=>c.id===id) || data.chapters[0];activeChapter=chapter.id;
  $('hero').hidden=chapter.id!=='00-start-here';
  $('content').innerHTML=chapter.html;
  $('reading-title').textContent=shortNames[chapter.id]||chapter.title;
  $('chapter-kind').textContent='FIELD GUIDE / '+(chapter.path.startsWith('chapters/')?'CHAPTER':'REFERENCE');
  document.title=(shortNames[chapter.id]||chapter.title)+' · Fieldnotes';
  setActive(chapter.id);addCopyButtons();createToc();closeMenu();
  if(anchor){requestAnimationFrame(()=>document.getElementById(anchor)?.scrollIntoView());}
  else window.scrollTo({top:0,behavior:'instant'});
}
function route(){
  clearTimeout(search.timer);
  let raw;try{raw=decodeURIComponent(location.hash.slice(1));}catch(_){raw='00-start-here';}
  if(raw==='content'){$('content').focus();$('content').scrollIntoView();return;}
  $('search').value='';
  if(raw==='tools'){showTools();return;}
  const id=raw.split('--')[0]||'00-start-here';
  showChapter(id,raw.includes('--')?raw:null);
}
function highlight(text,words){
  const regex = new RegExp('('+words.map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','gi');
  return text.split(regex).map((part,i)=>i%2?'<mark>'+esc(part)+'</mark>':esc(part)).join('');
}
function search(){
  const query=$('search').value.trim();if(!query){showChapter(activeChapter);return;}
  const words=query.toLowerCase().split(/\s+/).filter(Boolean);
  const results=sections.map(s=>{
    const hay=(s.title+' '+s.chapterTitle+' '+s.body).toLowerCase();
    return {s,score:words.every(w=>hay.includes(w))?words.reduce((n,w)=>n+(s.title.toLowerCase().includes(w)?8:0)+(s.body.toLowerCase().includes(w)?2:0),0):0};
  }).filter(r=>r.score>0).sort((a,b)=>b.score-a.score);
  $('hero').hidden=true;$('toc').innerHTML='';setActive('');$('reading-title').textContent=`${results.length} matching sections`;$('chapter-kind').textContent='SEARCH / ALL CHAPTERS';
  $('content').innerHTML='<h1>Follow the evidence.</h1><p>'+results.length+' sections match <strong>'+esc(query)+'</strong>. Showing '+Math.min(80,results.length)+'.</p>'+(results.length?results.slice(0,80).map(({s})=>{
    const position=Math.max(0,s.body.toLowerCase().indexOf(words[0])-75);const snippet=(position?'…':'')+s.body.slice(position,position+280).replace(/\s+/g,' ')+'…';
    return `<a class="result" href="#${esc(s.id||s.chapter)}"><span class="result-chapter">${esc(shortNames[s.chapter]||s.chapterTitle)}</span><strong>${highlight(s.title,words)}</strong><p>${highlight(snippet,words)}</p></a>`;
  }).join(''):'<div class="empty-state"><strong>No matching sections.</strong><p>Try fewer words or a synonym: “JWT”, “packet”, “memory”, “XOR”, “radare2”. Tool lookup can also search installation notes.</p><a href="#tools">Open tool lookup →</a></div>');
}
function showTools(){
  $('hero').hidden=true;$('toc').innerHTML='';setActive('tool-matrix');closeMenu();$('chapter-kind').textContent='REFERENCE / TOOL LOOKUP';$('reading-title').textContent='282 entries · exact workbook provenance';
  $('content').innerHTML='<h1>Know what is available.</h1><p>Approval and installation are separate facts. Search the supplied list before choosing a tool. Windows entries may be installed inside WSL; check the location.</p><div class="tool-controls"><label>Tool or note<input id="tool-query" type="search" placeholder="e.g. radare2, symbols, FUSE"></label><label>Environment<select id="tool-platform"><option value="">All environments</option><option>Kali</option><option>Windows / WSL</option></select></label><label>Status<select id="tool-status"><option value="">All entries</option><option>Approved</option><option>Unapproved</option></select></label></div><p id="tool-count" role="status"></p><div id="tool-results"></div>';
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
$('menu-button').addEventListener('click',()=>{const open=$('sidebar').classList.toggle('open');$('menu-button').setAttribute('aria-expanded',String(open));});
function theme(value){document.documentElement.dataset.theme=value;$('theme-button').textContent=value==='dark'?'Light':'Dark';$('theme-button').setAttribute('aria-label','Switch to '+(value==='dark'?'light':'dark')+' theme');}
try{theme(localStorage.getItem('ctf-fieldnotes-theme')||'light');}catch(_){theme('light');}
$('theme-button').addEventListener('click',()=>{const value=document.documentElement.dataset.theme==='dark'?'light':'dark';theme(value);try{localStorage.setItem('ctf-fieldnotes-theme',value);}catch(_){} });
document.addEventListener('keydown',event=>{
  if(event.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){event.preventDefault();$('search').focus();}
  if(event.key==='Escape'){clearTimeout(search.timer);$('search').value='';closeMenu();route();$('search').blur();}
});
document.addEventListener('click',event=>{
  const link=event.target.closest('a[href^="#"]');if(!link)return;
  if(link.hash===location.hash){event.preventDefault();route();}
});
window.addEventListener('hashchange',route);
route();
