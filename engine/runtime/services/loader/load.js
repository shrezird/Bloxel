console.log('SERVICE: load.js has been initialized successfully');

(function (global) {
  const dataNames = [
    'error'
  ];
  const baseDirectory = document.currentScript.src.replace(/[^/]+$/, '');
  const preloadCache = {};

  for (const name of dataNames) {
    const request = new XMLHttpRequest();
    request.open('GET', baseDirectory + 'data/' + name + '.json', false);
    request.send(null);
    preloadCache[name] = JSON.parse(request.responseText);
    global[name] = preloadCache[name];
  }

  global.__preloadCache = preloadCache;
})(window);

console.log('SERVICE: load.js has successfully preloaded and cached the following data: ' + Object.keys(__preloadCache).join(', '));