var isPushEnabled = false,
registration,
subBtn;

window.addEventListener('load', function() {
  subBtn = document.getElementById('webpush-subscribe-button');

  subBtn.textContent = 'Habilitar Notificações Push';

  subBtn.addEventListener('click',
    function() {
      subBtn.disabled = true;
      if (isPushEnabled) {
        return unsubscribe(registration);
      }
      return subscribe(registration);
    }
  );

  if ('serviceWorker' in navigator) {
    const serviceWorker = document.querySelector('meta[name="service-worker-js"]').content;
    navigator.serviceWorker.register(serviceWorker).then(
      function(reg) {
        registration = reg;
        initialiseState(reg);
      });
  } else {
    showMessage('Service workers não são suportados no seu navegador.');
  }

  function initialiseState(reg) {
    if (!(reg.showNotification)) {
        showMessage('Exibição de notificações não é suportada no seu navegador.');
        return;
    }

    if (Notification.permission === 'denied') {
      subBtn.disabled = false;
      showMessage('Notificações push estão bloqueadas pelo seu navegador.');
      return;
    }

    if (!('PushManager' in window)) {
      subBtn.disabled = false;
      showMessage('Notificações push não estão disponíveis no seu navegador.');
      return;
    }

    reg.pushManager.getSubscription().then(
      function(subscription) {
        if (subscription){
          postSubscribeObj('subscribe', subscription,
            function(response) {
              if (response.status === 201) {
                subBtn.textContent = 'Desabilitar Notificações Push';
                subBtn.disabled = false;
                isPushEnabled = true;
                showMessage('Notificações push habilitadas com sucesso.');
              }
            });
        }
      });
  }
}
);

function showMessage(message) {
  const messageBox = document.getElementById('webpush-message');
  if (messageBox) {
    messageBox.textContent = message;
    messageBox.style.display = 'block';
  }
}

function subscribe(reg) {
  reg.pushManager.getSubscription().then(
    function(subscription) {
      var metaObj, applicationServerKey, options;
      if (subscription) {
        return subscription;
      }

      metaObj = document.querySelector('meta[name="django-webpush-vapid-key"]');
      applicationServerKey = metaObj.content;
      options = {
        userVisibleOnly: true
      };
      if (applicationServerKey){
        options.applicationServerKey = urlB64ToUint8Array(applicationServerKey)
      }
      reg.pushManager.subscribe(options)
        .then(
          function(subscription) {
            postSubscribeObj('subscribe', subscription,
              function(response) {
                if (response.status === 201) {
                  subBtn.textContent = 'Desabilitar Notificações Push';
                  subBtn.disabled = false;
                  isPushEnabled = true;
                  showMessage('Notificações push habilitadas com sucesso.');
                }
              });
          })
        .catch(
          function() {
            console.log('Erro ao se inscrever nas notificações push.', arguments)
          })
    }
  );
}

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (var i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function unsubscribe(reg) {
  reg.pushManager.getSubscription()
    .then(
      function(subscription) {
        if (!subscription) {
          subBtn.disabled = false;
          showMessage('Inscrição não está disponível.');
          return;
        }
        postSubscribeObj('unsubscribe', subscription,
          function(response) {
            if (response.status === 202) {
              subscription.unsubscribe()
                .then(
                  function(successful) {
                    subBtn.textContent = 'Habilitar Notificações Push';
                    showMessage('Notificações push desabilitadas com sucesso.');
                    isPushEnabled = false;
                    subBtn.disabled = false;
                  }
                )
                .catch(
                  function(error) {
                    subBtn.textContent = 'Desabilitar Notificações Push';
                    showMessage('Erro ao cancelar a inscrição das notificações push.');
                    subBtn.disabled = false;
                  }
                );
            }
          });
      }
    )
}

function postSubscribeObj(statusType, subscription, callback) {
  var browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase(),
    user_agent = navigator.userAgent,
    data = {  status_type: statusType,
              subscription: subscription.toJSON(),
              browser: browser,
              user_agent: user_agent,
              group: subBtn.dataset.group
           };

  fetch(subBtn.dataset.url, {
    method: 'post',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data),
    credentials: 'include'
  }).then(callback);
}
