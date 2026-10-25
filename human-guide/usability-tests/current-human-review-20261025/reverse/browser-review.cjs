const { chromium } = require(process.env.TEMP + '/ctf-guide-dom-review/node_modules/playwright-core');
(async () => {
 const browser = await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page = await browser.newPage({viewport:{width:1440,height:1000}});
 await page.goto('file:///C:/Users/verno/Downloads/ctf-skills-main/ctf-skills-main/human-guide/index.html');
 console.log('TITLE', await page.title());
 console.log('INPUTS', await page.locator('input').evaluateAll(xs=>xs.map(x=>({placeholder:x.placeholder,type:x.type}))));
 console.log('BUTTONS', await page.getByRole('button').allTextContents());
 console.log('LINKS', (await page.getByRole('link').allTextContents()).slice(0,60));
 await page.screenshot({path:__dirname+'/website-start.png'});
 await browser.close();
})();
