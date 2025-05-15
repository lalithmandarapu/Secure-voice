self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('securevoice-cache').then(function(cache) {
            return cache.addAll([
                '/',
                '/static/script.js',
                '/static/crypto.js',
                '/templates/index.html'
            ]);
        })
    );
});

self.addEventListener('fetch', function(e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
            return response || fetch(e.request);
        })
    );
});
