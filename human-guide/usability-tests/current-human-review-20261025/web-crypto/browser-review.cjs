const {chromium} = require(process.env.TEMP + '/ctf-guide-dom-review/node_modules/playwright-core');
const path = require('path');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 try {
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 await page.context().setOffline(true);
 await page.goto('file:///' + path.resolve('human-guide/index.html').replace(/\\/g,'/'));
 await page.getByRole('searchbox').fill('ffuf');
 await page.waitForTimeout(250);
 await page.screenshot({path:path.join(__dirname,'browser-search-ffuf.png')});
 await page.getByRole('link').filter({hasText:'CPTS / Enumeration/Service Enumeration/80,443 http'}).click();
 console.log('NOTE URL',page.url());
 console.log('NOTE TOP', (await page.locator('main').innerText()).slice(0,1500));
 console.log('NOTE BUTTONS',await page.getByRole('button').evaluateAll(es=>es.map(e=>({text:e.innerText,label:e.getAttribute('aria-label')}))));
 console.log('NOTE IMAGES', await page.locator('main img').evaluateAll(es=>es.map(e=>({alt:e.alt,width:e.width,height:e.height}))));
 await page.screenshot({path:path.join(__dirname,'browser-cpts-http.png')});
 await page.keyboard.press('Control+Home');
 await page.screenshot({path:path.join(__dirname,'browser-cpts-http-top.png')});
 await page.context().grantPermissions(['clipboard-read','clipboard-write']);
 await page.getByRole('button').filter({hasText:/^Copy$/}).first().click();
 await page.waitForTimeout(100);
 console.log('COPY BUTTON',await page.getByRole('button').filter({hasText:/^Copied$/}).count());
 console.log('CLIPBOARD',await page.evaluate(()=>navigator.clipboard.readText()));
 await page.getByRole('link',{name:'80,443 http',exact:true}).click();
 console.log('SIDEBAR NOTE URL',page.url());
 await page.getByRole('link',{name:'Event tool rules',exact:true}).click();
 console.log('RULES TOP', (await page.locator('main').innerText()).slice(0,4800));
 } finally { await browser.close(); }
})();
