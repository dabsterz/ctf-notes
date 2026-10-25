const { chromium } = require(process.env.TEMP + '/ctf-guide-dom-review/node_modules/playwright-core');
(async () => {
 const browser = await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page = await browser.newPage({viewport:{width:1440,height:1000}});
 await page.goto('file:///C:/Users/verno/Downloads/ctf-skills-main/ctf-skills-main/human-guide/index.html');
 await page.getByRole('searchbox').fill('strings');
 await page.waitForTimeout(400);
 console.log((await page.locator('body').innerText()).slice(0,15000));
 await page.screenshot({path:__dirname+'/website-search-strings.png'});
 await browser.close();
})();

