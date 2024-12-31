import puppeteer from 'puppeteer';
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

    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    try {

        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

        // Navigate to Instagram login page
        await page.goto('https://www.instagram.com/accounts/login/', { waitUntil: 'networkidle2' });

        // Wait for the login form to load
        await page.waitForSelector('input[name="username"]');

        // Enter username and password
        await page.type('input[name="username"]', 'shimabukurocoder');  // Replace 'your_username' with your Instagram username
        await page.type('input[name="password"]', 'Publ1cPassw0rd');  // Replace 'your_password' with your Instagram password

        // Click the login button
        await page.click('button[type="submit"]');

        // Wait for the page to load after login
        await page.waitForNavigation({ waitUntil: 'networkidle2' });
        // Переходимо на сторінку профілю користувача
        await page.goto(url, { waitUntil: 'networkidle2' });

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