'''javascript
(async () => {
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
    await page.goto(SAML_URL);

    await page.waitForSelector('input[type=email]', {visible: true});
    await page.type('input[type=email]', EMAIL);
    await page.click('input[type=submit]');
    console.log('Email submitted');
    await page.screenshot({path: 'screenshot1.png'});

    setTimeout(function() {
        console.log('This printed after about 1 second');
    }, 1000);

    await page.waitForSelector('input[type=password]', {visible: true});
    await page.type('input[type=password]', PASSWORD);
    await page.click('input[type=submit]');
    console.log('Password submitted');
    await page.screenshot({path: 'screenshot2.png'});
    await page.waitForSelector('input[name=otc]', {visible: true});

    setTimeout(function() {
        console.log('This printed after about 1 second');
    }, 1000);

    const token = totp.getTOTP(SECRET, 'base32', Date.now(), 6);
    console.log('TOTP: ', token);
    await page.type('input[name=otc]', totp);
    await page.click('input[type=submit]');
    console.log('TOTP submitted');
    await page.waitForNavigation();
    await page.screenshot({path: 'screenshot3.png'});
    const cookieValue = (await page.cookies()).find(cookieData => cookieData.name === 'SVPNCOOKIE').value;
    console.log(cookieValue);

    await browser.close();
})();
'''