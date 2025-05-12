const CACHE = 'securevoice-v1';
const FILES = [
  '/',
  '/static/script.js',
  '/static/crypto.js',
  '/static/service-worker.js',
  '/templates/index.html'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES)));
});

self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(resp => resp || fetch(e.request)));
});
