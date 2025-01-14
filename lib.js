
export function getRandomElement(arr) {
    const randomIndex = Math.floor(Math.random() * arr.length);
    return arr[randomIndex];
}
export function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}

export const puppeteerArguments = [
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
export const androidSides = [
    { width: 600, height: 860 },
    { width: 1080, height: 1920 },
    { width: 1080, height: 2340 },
    { width: 1440, height: 2560 },
    { width: 1080, height: 2400 },
    { width: 750, height: 1334 },
    { width: 1440, height: 2960 },
    { width: 1080, height: 2340 },
    { width: 1440, height: 3040 },
    { width: 1080, height: 2220 },
    { width: 1440, height: 3088 },
    { width: 1125, height: 2436 },
    { width: 1440, height: 3200 },
    { width: 1080, height: 2400 },
    { width: 1080, height: 2280 },
    { width: 720, height: 1280 },
    { width: 1080, height: 2160 },
    { width: 1440, height: 3120 },
    { width: 1080, height: 2520 },
    { width: 1080, height: 1920 },
    { width: 720, height: 1440 },
    { width: 1080, height: 2312 },
    { width: 1080, height: 2408 },
    { width: 1200, height: 2000 },
    { width: 1080, height: 2220 },
    { width: 1440, height: 2560 },
    { width: 1080, height: 2340 },
    { width: 1080, height: 2280 },
    { width: 1366, height: 768 },
    { width: 1280, height: 800 },
    { width: 1080, height: 2100 },
    { width: 1440, height: 2800 },
    { width: 1080, height: 2040 },
    { width: 720, height: 1280 },
    { width: 1440, height: 2960 },
    { width: 1200, height: 1920 },
    { width: 1080, height: 2520 },
    { width: 720, height: 1440 },
    { width: 1080, height: 2330 },
    { width: 1440, height: 3120 }
];
export const userAgents =  [
    // Chrome (WebKit engine)
    'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Mi 9T Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A528B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',

    // Firefox (Gecko engine)
    'Mozilla/5.0 (Android 12; Mobile; rv:112.0) Gecko/112.0 Firefox/112.0',
    'Mozilla/5.0 (Android 10; Mobile; LG-H870; rv:109.0) Gecko/109.0 Firefox/109.0',
    'Mozilla/5.0 (Android 11; Mobile; SM-G973F; rv:110.0) Gecko/110.0 Firefox/110.0',
    'Mozilla/5.0 (Android 9; Mobile; Mi A2; rv:107.0) Gecko/107.0 Firefox/107.0',
    'Mozilla/5.0 (Android 13; Mobile; Pixel 7; rv:116.0) Gecko/116.0 Firefox/116.0',

    // Samsung Internet (Chromium-based)
    'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/18.0 Chrome/92.0.4515.166 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/17.0 Chrome/88.0.4324.152 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-T505) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/16.0 Chrome/83.0.4103.106 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/20.0 Chrome/95.0.4638.69 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; SM-N960F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/15.0 Chrome/75.0.3770.101 Mobile Safari/537.36',

    // Opera (Chromium-based)
    'Mozilla/5.0 (Linux; Android 12; CPH2201) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 OPR/66.2.2254.63896',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 OPR/65.1.2254.63854',
    'Mozilla/5.0 (Linux; Android 10; SM-G960U1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36 OPR/63.2.3214.58577',
    'Mozilla/5.0 (Linux; Android 9; Redmi Note 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36 OPR/62.0.2254.59977',
    'Mozilla/5.0 (Linux; Android 13; SM-F926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 OPR/67.3.2254.67845',

    // Edge (Chromium-based)
    'Mozilla/5.0 (Linux; Android 12; SM-G781B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36 EdgA/112.0.1722.58',
    'Mozilla/5.0 (Linux; Android 11; Mi 11 Lite 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 EdgA/111.0.1661.62',
    'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 EdgA/110.0.1654.59',
    'Mozilla/5.0 (Linux; Android 9; Redmi 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 EdgA/109.0.1518.61',
    'Mozilla/5.0 (Linux; Android 13; SM-F721B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 EdgA/114.0.1823.41',

    // DuckDuckGo Browser
    'Mozilla/5.0 (Linux; Android 12; SM-A326B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 DuckDuckGo/5',
    'Mozilla/5.0 (Linux; Android 11; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 DuckDuckGo/4',
    'Mozilla/5.0 (Linux; Android 10; OnePlus 6T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 DuckDuckGo/3',
    'Mozilla/5.0 (Linux; Android 9; Mi A3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 DuckDuckGo/2',
    'Mozilla/5.0 (Linux; Android 13; Galaxy S22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 DuckDuckGo/6',

    // Brave (Chromium-based)
    'Mozilla/5.0 (Linux; Android 12; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36 Brave/1.51.100',
    'Mozilla/5.0 (Linux; Android 11; OnePlus 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Brave/1.50.125',
    'Mozilla/5.0 (Linux; Android 10; SM-T510) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 Brave/1.49.88',
    'Mozilla/5.0 (Linux; Android 9; Redmi 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 Brave/1.48.99',
    'Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Brave/1.52.112',

    // Vivaldi (Chromium-based)
    'Mozilla/5.0 (Linux; Android 12; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36 Vivaldi/5.7.2921.60',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Vivaldi/5.6.2868.33',
    'Mozilla/5.0 (Linux; Android 10; Mi 10T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 Vivaldi/5.5.2805.32',
    'Mozilla/5.0 (Linux; Android 9; SM-J730F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 Vivaldi/5.4.2753.37',
    'Mozilla/5.0 (Linux; Android 13; Galaxy Z Fold 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Vivaldi/5.8.2990.50',
]
export const lynx = 'Lynx/2.8.9dev.16 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.0.2k'