import puppeteer from 'puppeteer';
import fs from 'fs/promises';
import * as lib from './lib.js'
import supabaseClient from './supabaseClient.js';
import iter_posts from "./extractor.js";
import calculateTextAnAnnouncementPossibility from "./aiapi.js";

const usernames = ['salsahubkyiv'] //[,'salsabo_dance','salsaclubrivne']
const maxPosts = 6;

(async () => {
    const city = "Львів"
    const category = "dance"
    const scrapeInstagramPosts = async (username, id) => {

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
            let url = 'https://megogo.net/'
            url = `https://www.instagram.com/${username}`
            console.log('Перехід на сторінку Instagram');
            await page.goto(url, {
                waitUntil: 'networkidle0'
            });
            console.log('Сторінка завантажена');
            const html = await page.content();
            //await lib.sleep(1000); //new Promise(resolve => setTimeout(resolve, 1000));
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const datestamp = timestamp.slice(0,10)
            console.log('Створення скріншота');// створення артифактів
            const screenshotPath = `./saved/${username}_${timestamp}.png`;
            await page.screenshot({
                path: screenshotPath,
                fullPage: true
            });
            console.log(`Скріншот збережено у файл: ${screenshotPath}`);
            const fileName = `./saved/${username}_${timestamp}.html`;
            await fs.writeFile(fileName, html);
            console.log(`HTML-сторінку збережено у файл: ${fileName}`);

            const posts = iter_posts(html)
            if (posts.length===0){
                console.log('no posts found for '+username)
                process.exit()
            }

            let records = []
            for (let post of posts) {
                    const {data, error} = await supabaseClient
                        .from('posts')
                        .select('id, url_slug')
                        .eq('url_slug', post.slug)

                    if (data.length === 0) {
                        let p= await calculateTextAnAnnouncementPossibility(post.text)
                        console.log(p, post.text.slice(0, 22))
                        records.push({category: category, city: city, fulltext: post.text, url_slug: post.slug
                            , 'possibility': p,'source_slug':username, 'media': 'insta'})
                    }
            }
            console.log("we've founded new posts: "+records.length)
            const {data, error} = await supabaseClient.from('posts').insert(records)
            await supabaseClient.from('sources').update({'last_scraped':datestamp, 'new_posts': records.length}).match({'id':id})
            console.log(error)

        } catch (error) {
            console.error('Error:', error);
            return [];
        } finally {
            await browser.close();
        }
    };

    const {data, error} = await supabaseClient
        .from('sources')
        .select('id, slug')
        .eq('media', 'insta')
        .eq('category', category)
        .eq('city', city)
        .order('last_scraped',{ascending: true})

    console.log(data, error)
    for (let user of data){
        await scrapeInstagramPosts(user.slug, user.id);
        await lib.sleep(9000, 8000)
    }

})();

async function preparePuppeteer(page) {
    // Увімкнення перехоплення запитів
    await page.setRequestInterception(true);

    // Обробка запитів
    page.on('request', (request) => {
        const resourceType = request.resourceType();

        // Відхилення непотрібних ресурсів
        if (['image', 'stylesheet', 'font'].includes(resourceType)) {
            request.abort();
        } else {
            request.continue();
        }
    });
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


