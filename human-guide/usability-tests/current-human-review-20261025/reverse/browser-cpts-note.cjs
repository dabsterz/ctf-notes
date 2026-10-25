const { chromium } = require(process.env.TEMP + '/ctf-guide-dom-review/node_modules/playwright-core');
(async () => {
 const browser = await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000},permissions:['clipboard-read','clipboard-write']}); const page=await context.newPage();
 await page.goto('file:///C:/Users/verno/Downloads/ctf-skills-main/ctf-skills-main/human-guide/index.html');
 await page.getByRole('searchbox').fill('strings');
 await page.waitForTimeout(400); await page.getByRole('link').filter({hasText:'CPTS / PrivEsc/Linux/SUID Sticky Bit'}).click();
 console.log('URL',page.url());
 console.log((await page.locator('main').innerText()));
 console.log('BUTTONS',await page.getByRole('button').allTextContents());
 console.log('IMAGES',await page.locator('main img').count());
 await page.screenshot({path:__dirname+'/website-cpts-note.png',fullPage:true});
 const copy=page.getByRole('button').filter({hasText:/^Copy$/}).nth(1);
 if(await copy.count()) { await copy.click(); await page.waitForTimeout(150); console.log('COPY AFTER',await copy.innerText()); try { console.log('CLIPBOARD',await page.evaluate(()=>navigator.clipboard.readText())); } catch(e) {console.log('CLIPBOARD READ',e.message);}  }
 const fs=page.getByRole('button',{name:'Full size',exact:true}).first();
 if(await fs.count()) { await fs.click(); await page.locator('main img').first().scrollIntoViewIfNeeded(); console.log('IMAGE SIZE',await page.locator('main img').first().evaluate(x=>({naturalWidth:x.naturalWidth,width:x.width,naturalHeight:x.naturalHeight,height:x.height}))); await page.screenshot({path:__dirname+'/website-cpts-fullsize.png'}); console.log('FULLSIZE clicked'); await page.getByRole('button',{name:'Fit width',exact:true}).click(); console.log('FIT WIDTH restored'); }
 await browser.close();
})();



