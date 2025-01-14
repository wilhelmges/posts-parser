import puppeteer from 'puppeteer';
import fs from 'fs/promises';
import * as lib from './lib.js'
import iter_posts from "./extractor.js";

const usernames = ['salsahubkyiv','salsaclubrivne'] //[,'salsahubkyiv']
const maxPosts = 6;

(async () => {
    const scrapeInstagramPosts = async (username) => {
        console.log(`Processing user: ${username}`);
        // Налаштування браузера
        const browser = await puppeteer.launch({
            headless: true,
            ignoreDefaultArgs: ['--enable-automation'],
            args: lib.puppeteerArguments
        });
        // Створення нової сторінки
        const page = await browser.newPage();
        await preparePuppeteer(page);

        try {
            // Перехід на сторінку Instagram
            const url = `https://www.instagram.com/${username}` //'https://megogo.net/' //
            console.log('Перехід на сторінку Instagram');
            await page.goto(url, {
                waitUntil: 'networkidle0'
            });
            console.log('Сторінка завантажена');
            await lib.sleep(1000); //new Promise(resolve => setTimeout(resolve, 1000));

            const html = await page.content();
            console.log(iter_posts(html))

            // const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            // // створення артифактів
            // console.log('Створення скріншота');
            // const screenshotPath = `./saved/${username}_${timestamp}.png`;
            // await page.screenshot({
            //     path: screenshotPath,
            //     fullPage: true
            // });
            // console.log(`Скріншот збережено у файл: ${screenshotPath}`);
            // const fileName = `./saved/${username}_${timestamp}.html`;
            // await fs.writeFile(fileName, html);
            // console.log(`HTML-сторінку збережено у файл: ${fileName}`);

        } catch (error) {
            console.error('Error:', error);
            return [];
        } finally {
            await browser.close();
        }
    };

    for (let user of usernames) await scrapeInstagramPosts(user);

})();

async function preparePuppeteer(page) {
    // Налаштування viewport для мобільної версії
    await page.setViewport({
        ...lib.getRandomElement(lib.androidSides),
        ...{
        isMobile: true,
        hasTouch: true,
        }
    });

    console.log('Встановлення User-Agent для mobile browser');
    await page.setUserAgent(lib.getRandomElement(lib.userAgents));
}


