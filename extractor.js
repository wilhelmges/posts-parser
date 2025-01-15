import { readFile } from 'fs/promises';
import * as cheerio from 'cheerio';

if (import.meta.url === `file://${process.argv[1]}`) {
    const filePath = './tmp/lcd.html';// Шлях до HTML-файлу
    try {
        const html = await readFile(filePath, 'utf8');// Зчитуємо HTML-файл
        iter_posts(html)
    } catch (error) {
        console.error('Помилка:', error);
    }
}

export default function iter_posts(html) {
    // Завантажуємо HTML у Cheerio
    const $ = cheerio.load(html);

    console.log('start parsing')
    let links = []
    $('article a').each((index, link) => {
        const href = $(link).attr('href');
        const slug = href.split('/').filter(Boolean).pop();
        links.push(slug)
    })
    let posts = []
    $('article span').each((index, cover) => {
        const text = $(cover).text()

        if (text.length>5){
            posts.push({'slug':links[index],'text':text})
            console.log(index, ' ',links[index],' - ',text.slice(0,20));
        }
    })
    return posts;
}

// const title = $('title').text(); // Текст у <title>
// const firstParagraph = $('.content p').first().text(); // Перший <p> у .content
// const highlightedText = $('.highlight').text(); // <p class="highlight">
