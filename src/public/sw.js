const CACHE_NAME = 'credit-oracle-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/index.css',
  '/app.js',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap',
  'https://unpkg.com/lucide@latest'
];

// Install Event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('Caching shell assets...');
      return cache.addAll(ASSETS);
    })
  );
});

// Activate Event
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            console.log('Clearing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
});

// Fetch Event
self.addEventListener('fetch', event => {
  // Only cache GET requests
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      return cachedResponse || fetch(event.request).catch(() => {
        // Fallback for offline if requesting HTML
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match('/index.html');
        }
      });
    })
  );
});
