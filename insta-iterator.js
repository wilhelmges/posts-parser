import puppeteer from 'puppeteer';
import fs from 'fs/promises';
import iter_posts from "./extractor.js";

const usernames = ['lcd_bachata'] //['salsaclubrivne','salsahubkyiv']
const maxPosts = 6;

(async () => {
    const scrapeInstagramPosts = async (username, maxPosts = 10) => {
        console.log(`Processing user: ${username}`);
        // Налаштування браузера
        const browser = await puppeteer.launch({
            headless: true,
            ignoreDefaultArgs: ['--enable-automation'],
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-software-rasterizer',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-xdg-open',
                '--disable-notifications',
                '--disable-default-apps',
                '--disable-popup-blocking',
                '--disable-prompt-on-repost',
                '--no-default-browser-check',
                '--no-first-run',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-background-timer-throttling'
            ]
        });

        // Створення нової сторінки
        const page = await browser.newPage();
        await preparePuppeteer(page);

        try {
            // Перехід на сторінку Instagram
            console.log('Перехід на сторінку Instagram');
            await page.goto(`https://www.instagram.com/${username}/`, {
                waitUntil: 'networkidle0'
            });
            console.log('Сторінка завантажена');
            await sleep(1000); //new Promise(resolve => setTimeout(resolve, 1000));

            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            // створення артифактів
            // Створення скріншота
            console.log('Створення скріншота');

            const screenshotPath = `./saved/${username}_${timestamp}.png`;
            await page.screenshot({
                path: screenshotPath,
                fullPage: true
            });
            console.log(`Скріншот збережено у файл: ${screenshotPath}`);

            // Збереження HTML
            const html = await page.content();
            console.log(iter_posts(html))

            const fileName = `./saved/${username}_${timestamp}.html`;
            await fs.writeFile(fileName, html);
            console.log(`HTML-сторінку збережено у файл: ${fileName}`);
            return true;
        } catch (error) {
            console.error('Error:', error);
            return [];
        } finally {
            await browser.close();
        }
    };

    for (let user of usernames) await scrapeInstagramPosts(user, maxPosts);

})();

async function preparePuppeteer(page) {
    // Налаштування viewport для мобільної версії
    await page.setViewport({
        width: 390,
        height: 844,
        isMobile: true,
        hasTouch: true,
    });

    console.log('Встановлення User-Agent для mobile browser');
    const android = 'Mozilla/5.0 (Linux; Android 12; RMX3085) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36';
    const lynx = 'Lynx/2.8.9dev.16 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.0.2k'
    const basichtml = 'retawq/0.2.6c [text-mode]'

    await page.setUserAgent(android);
}

function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}

