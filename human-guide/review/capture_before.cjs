// Development-only renderer. Requires playwright-core outside the guide ZIP.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.argv[2]);
const root=path.resolve(__dirname,'..'),out=path.join(__dirname,'ui');
(async()=>{
  fs.mkdirSync(out,{recursive:true});
  const inputs=[...fs.readdirSync(path.join(root,'chapters')).map(n=>'chapters/'+n),
    ...fs.readdirSync(path.join(root,'recipes')).filter(n=>n.endsWith('.py')).map(n=>'recipes/'+n),
    'QUICKSTART.md','COMPETITION.md','TOOL-CHOOSER.md','HANDBOOK.md'];
  fs.writeFileSync(path.join(out,'content-before.json'),JSON.stringify(Object.fromEntries(inputs.map(n=>[n,crypto.createHash('sha256').update(fs.readFileSync(path.join(root,n))).digest('hex')])),null,2));
  const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
  try {
    const page=await browser.newPage({viewport:{width:1440,height:1000},offline:true});
    await page.goto(pathToFileURL(path.join(root,'index.html')).href);
    await page.screenshot({path:path.join(out,'before-desktop.png')});
    console.log('Baseline screenshot saved; browser '+browser.version());
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
