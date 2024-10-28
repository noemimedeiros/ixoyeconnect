var staticCacheName = 'ixoye-connect-v1';

var assetsToCache = [
  '/layouts/base',
  '/static/img/bottom-desktop-2.svg',
  '/static/img/bottom-desktop.svg',
  '/static/img/top-nav-mobile-2.svg',
  '/static/img/top-nav-mobile.svg',

];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      console.log('Caching static assets');
      return cache.addAll(assetsToCache);
    })
  );
});

self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);

  if (requestUrl.origin === location.origin) {
    if (requestUrl.pathname === '/') {
      event.respondWith(caches.match('/layouts/base'));
      return;
    }
  }

  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});

self.addEventListener('push', event => {
  const data = event.data.json();
  self.registration.showNotification(data.title, {
      body: data.body,
      icon: data.icon,
  });
});