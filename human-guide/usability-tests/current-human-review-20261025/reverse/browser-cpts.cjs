const { chromium } = require(process.env.TEMP + '/ctf-guide-dom-review/node_modules/playwright-core');
(async () => {
 const browser = await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page = await browser.newPage({viewport:{width:1440,height:1000}});
 await page.goto('file:///C:/Users/verno/Downloads/ctf-skills-main/ctf-skills-main/human-guide/index.html');
 await page.getByText("Vernon's CPTS notes",{exact:false}).first().click();
 console.log('LINKS',await page.getByRole('link').allTextContents());
 await page.screenshot({path:__dirname+'/website-cpts-sidebar.png'});
 await browser.close();
})();
