import puppeteer from 'puppeteer';

const scrapeInstagramPosts = async (username, maxPosts = 10) => {
    const url = `https://www.instagram.com/${username}/`;

    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    try {

                await page.goto('https://www.instagram.com/accounts/login/', { waitUntil: 'networkidle2' });

// Wait for the login form to load
        await page.waitForSelector('input[name="username"]');

        // Enter username and password
        await page.type('input[name="username"]', 'younglionrasmus');  // Replace 'your_username' with your Instagram username
        await page.type('input[name="password"]', 'Fgzpz3XGQ8ZKvh2');  // Replace 'your_password' with your Instagram password

        // Click the login button
        await page.click('button[type="submit"]');

        // Wait for the page to load after login
        await page.waitForNavigation({ waitUntil: 'networkidle2' });


        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
        // Переходимо на сторінку профілю користувача
        await page.goto(url, { waitUntil: 'networkidle2' });
        // Переходимо на сторінку профілю користувача
        await page.goto(url, { waitUntil: 'networkidle2' });

        // Чекаємо завантаження основних елементів сторінки
        await page.waitForSelector('article div img', { timeout: 10000 });

        // Витягуємо дані публікацій
        const posts = await page.evaluate((maxPosts) => {
            const nodes = document.querySelectorAll('div div div div a');
            return Array.from(nodes)
                .slice(0, maxPosts)
                .map(node => {
                    const postUrl = node.href;
                    const textElement = node.querySelector('img[alt]');
                    const text = textElement ? textElement.alt : 'No text';
                    return { postUrl, text };
                });
        }, maxPosts);

        console.log('Posts:', posts);
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
    const username = 'ethkyiv_ua'; // Замініть на потрібне ім'я користувача
    const maxPosts = 10;

    console.log(`Починаємо обробку для користувача: ${username}`);
    const posts = await scrapeInstagramPosts(username, maxPosts);

    console.log('Отримані публікації:');
    posts.forEach((post, index) => {
        console.log(`${index + 1}. URL: ${post.postUrl}`);
        console.log(`   Опис: ${post.text}`);
    });
};

main();