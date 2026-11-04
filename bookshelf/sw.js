// sw.js — Lightweight Service Worker for My Reading Corner PWA
const CACHE_NAME = 'mrc-cache-v1';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Network-first strategy with cache fallback
  if (event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            // Only cache same-origin and image assets
            if (event.request.url.startsWith(self.location.origin) || event.request.url.includes('covers.openlibrary.org')) {
              cache.put(event.request, clone);
            }
          });
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
