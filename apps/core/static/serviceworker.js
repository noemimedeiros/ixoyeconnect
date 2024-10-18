self.addEventListener('push', function(event) {
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: data.icon,
    };
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});
self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        // Serve o conteúdo do cache, ou busca na rede
        return response || fetch(event.request);
      })
    );
  });