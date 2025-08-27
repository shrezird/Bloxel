(function (global) {

  const dataNames = [
    'error'
  ];
  
  const baseDirectory = document.currentScript.src.replace(/[^/]+$/, '');
  const preloadCache = global.__preloadCache || {};

  for (const name of dataNames) {
    const storageKey = '__preload_' + name;
    sessionStorage.removeItem(storageKey);
    if (!preloadCache[name]) {
      let rawJson = sessionStorage.getItem(storageKey);
      if (!rawJson) {
        const request = new XMLHttpRequest();
        request.open('GET', baseDirectory + 'data/' + name + '.json', false);
        request.send(null);
        rawJson = request.responseText;
        sessionStorage.setItem(storageKey, rawJson);
      }
      preloadCache[name] = JSON.parse(rawJson);
    }
    global[name] = preloadCache[name];
  }

  global.__preloadCache = preloadCache;
})(window);