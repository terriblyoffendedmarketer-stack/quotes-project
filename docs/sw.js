// sw.js — Lightweight Service Worker for My Reading Corner PWA
const CACHE_NAME = 'mrc-cache-v13';

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
  if (event.request.method !== 'GET') return;

  // Never cache HTML pages or navigation requests — always fetch fresh from network
  if (event.request.mode === 'navigate' || event.request.destination === 'document') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }

  // Network-first for other assets, cache covers and static resources
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            if (event.request.url.includes('covers.openlibrary.org') || event.request.url.includes('cdn.tailwindcss.com')) {
              cache.put(event.request, clone);
            }
          });
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
