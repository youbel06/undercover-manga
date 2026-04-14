const CACHE = 'lelox-v25';
const PRECACHE = [
  './',
  'index.html',
  'undercover.html',
  'loupgarou.html',
  'lelox_logo.png',
  'lelox_banner4.png',
  'manifest.json'
];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(c =>
      Promise.all(PRECACHE.map(u => c.add(u).catch(() => null)))
    )
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url;
  try { url = new URL(req.url); } catch { return; }

  // Externes toujours live : Supabase, ElevenLabs, QR server, CDN JS
  if (/supabase\.co|elevenlabs\.io|api\.qrserver\.com|cdn\.jsdelivr\.net/.test(url.hostname)) return;

  // Audio MP3 : cache-first (immuables)
  if (url.pathname.includes('/audio/')) {
    e.respondWith(
      caches.match(req).then(c => c || fetch(req).then(r => {
        if (r.ok) { const cl = r.clone(); caches.open(CACHE).then(ca => ca.put(req, cl)); }
        return r;
      }).catch(() => c))
    );
    return;
  }

  // images.json / avatars.json : stale-while-revalidate
  if (url.pathname.endsWith('images.json') || url.pathname.endsWith('avatars.json')) {
    e.respondWith(
      caches.open(CACHE).then(cache =>
        cache.match(req).then(cached => {
          const fresh = fetch(req).then(r => { if (r.ok) cache.put(req, r.clone()); return r; }).catch(() => cached);
          return cached || fresh;
        })
      )
    );
    return;
  }

  // HTML : network-first avec fallback cache (offline)
  if (req.destination === 'document' || url.pathname.endsWith('.html') || url.pathname.endsWith('/')) {
    e.respondWith(
      fetch(req).then(r => {
        if (r.ok) { const cl = r.clone(); caches.open(CACHE).then(ca => ca.put(req, cl)); }
        return r;
      }).catch(() => caches.match(req).then(c => c || caches.match('index.html')))
    );
    return;
  }

  // Reste (images, js, css) : network-first
  e.respondWith(
    fetch(req).then(r => {
      if (r.ok) { const cl = r.clone(); caches.open(CACHE).then(ca => ca.put(req, cl)); }
      return r;
    }).catch(() => caches.match(req))
  );
});

self.addEventListener('push', e => {
  try {
    const data = e.data ? e.data.json() : {};
    e.waitUntil(self.registration.showNotification(data.title || 'LELOX', {
      body: data.body || 'Nouvelle activité',
      icon: 'lelox_logo.png',
      badge: 'lelox_logo.png',
      vibrate: [200, 100, 200]
    }));
  } catch {}
});
