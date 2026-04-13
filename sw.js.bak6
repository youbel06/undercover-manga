const CACHE = 'uc-lelox-v21';

self.addEventListener('install', e => {
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.url.includes('images.json') ||
      e.request.url.includes('avatars.json')) {
    e.respondWith(
      caches.open(CACHE).then(cache =>
        cache.match(e.request).then(cached => {
          const fresh = fetch(e.request).then(resp => {
            if (resp.ok) cache.put(e.request, resp.clone());
            return resp;
          });
          return cached || fresh;
        })
      )
    );
  } else {
    e.respondWith(
      fetch(e.request)
        .then(resp => resp)
        .catch(() => caches.match(e.request))
    );
  }
});
