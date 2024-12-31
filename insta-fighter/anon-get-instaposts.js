import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
puppeteer.use(StealthPlugin());

import fs from 'fs/promises'; // Використовуємо модуль `fs` із промісами

const writeArrayToFile = async (filePath, stringArray) => {
    try {
      // Перетворюємо масив у єдиний текст із розділенням рядків
      const fileContent = stringArray.join('\n-------------------\n');
  
      // Записуємо текст у файл
      await fs.writeFile(filePath, fileContent, 'utf8');
      console.log(`Масив успішно записаний у файл: ${filePath}`);
    } catch (error) {
      console.error('Помилка запису файлу:', error);
    }
  };

const scrapeInstagramPosts = async (username, maxPosts = 10) => {
    const url = `https://www.instagram.com/${username}/`;

    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
        // Spoof navigator properties to reduce detection
    await page.evaluateOnNewDocument(() => {
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
        Object.defineProperty(navigator, 'userAgent', { get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36' });
    });

    try {



        // Чекаємо завантаження основних елементів сторінки
        await page.waitForSelector('article div img', { timeout: 10000 });

        // Витягуємо дані публікацій
        const posts = await page.evaluate((maxPosts) => {
            const nodes = document.querySelectorAll('article div div div div a');
            return Array.from(nodes)
                .slice(0, maxPosts)
                .map(node => {
                    const postUrl = node.href;
                    const textElement = node.querySelector('img[alt]');
                    const text = textElement ? textElement.alt : 'No text';
                    return { postUrl, text };
                });
        }, maxPosts);

        //console.log('Posts:', posts);
        return posts;
    } catch (error) {
        console.error('Error:', error);
        return [];
    } finally {
        await browser.close();
    }
};

// Використання функції

const main = async () => {
    const username = 'unityhomechurch'; // Замініть на потрібне ім'я користувача
    const maxPosts = 10;

    console.log(`Починаємо обробку для користувача: ${username}`);
    const posts = await scrapeInstagramPosts(username, maxPosts);
    const text_posts = posts.map(obj => obj.text);

    await writeArrayToFile('posts.txt', text_posts);

    // console.log('Отримані публікації:');
    // posts.forEach((post, index) => {
    //     console.log(`${index + 1}. URL: ${post.postUrl}`);
    //     console.log(`   Опис: ${post.text}`);
    // });
};

main();