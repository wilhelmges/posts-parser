import puppeteer from 'puppeteer';
import fs from 'fs/promises';
import iter_posts from "./extractor.js";

const usernames = ['salsahubkyiv'] //['salsaclubrivne','salsahubkyiv']
const maxPosts = 6;

(async () => {
    const scrapeInstagramPosts = async (username) => {
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
            const url = 'https://megogo.net/' // `https://www.instagram.com/${username}`
            console.log('Перехід на сторінку Instagram');
            await page.goto(url, {
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
            //console.log(iter_posts(html))

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

function getRandomElement(arr) {
    const randomIndex = Math.floor(Math.random() * arr.length);
    return arr[randomIndex];
}
const androidSides = [
    { width: 600, height: 860 }, // Стандартний екран
    { width: 1080, height: 1920 }, // Samsung Galaxy S5
    { width: 1080, height: 2340 }, // Xiaomi Redmi Note 8 Pro
    { width: 1440, height: 2560 }, // Samsung Galaxy S6
    { width: 1080, height: 2400 }, // OnePlus 8
    { width: 750, height: 1334 }, // iPhone 6 (для порівняння)
    { width: 1440, height: 2960 }, // Samsung Galaxy S8
    { width: 1080, height: 2340 }, // Huawei P30
    { width: 1440, height: 3040 }, // Samsung Galaxy S10
    { width: 1080, height: 2220 }, // Google Pixel 2
    { width: 1440, height: 3088 }, // Samsung Galaxy Note 10
    { width: 1125, height: 2436 }, // Google Pixel 3
    { width: 1440, height: 3200 }, // Samsung Galaxy S20
    { width: 1080, height: 2400 }, // Xiaomi Mi 10
    { width: 1080, height: 2280 } // Motorola Moto G6
];
const userAgents = [
    // Chrome на Android
    'Mozilla/5.0 (Linux; Android 12; RMX3085) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',

    // Samsung Internet (базується на Chrome/AppleWebKit)
    'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/16.0 Chrome/92.0.4515.159 Mobile Safari/537.36',

    // Firefox для Android
    'Mozilla/5.0 (Android 10; Mobile; rv:102.0) Gecko/102.0 Firefox/102.0',

    // Opera для Android
    'Mozilla/5.0 (Linux; Android 9; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36 OPR/63.3.3216.58675',

    // Microsoft Edge для Android (базується на Chromium)
    'Mozilla/5.0 (Linux; Android 10; SM-A750F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36 EdgA/100.0.1185.50',

    // UC Browser для Android
    'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1816) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 UCBrowser/12.13.2.1207 (UWA/2.0.0) Mobile',

    // DuckDuckGo для Android (базується на Chromium)
    'Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36 DuckDuckGo/5',

    // Vivaldi для Android
    'Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36 Vivaldi/4.1',

    // Brave для Android (базується на Chromium)
    'Mozilla/5.0 (Linux; Android 12; SM-A127F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36 Brave/96.0.4664.110',

    // Kiwi Browser для Android (на базі Chromium)
    'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36 Kiwi/93.0.4577.51'
];
const lynx = 'Lynx/2.8.9dev.16 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.0.2k'

async function preparePuppeteer(page) {
    // Налаштування viewport для мобільної версії
    await page.setViewport({
        ...getRandomElement(androidSides),
        ...{
        isMobile: true,
        hasTouch: true,
        }
    });

    console.log('Встановлення User-Agent для mobile browser');
    await page.setUserAgent(getRandomElement(userAgents));
}

function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}

