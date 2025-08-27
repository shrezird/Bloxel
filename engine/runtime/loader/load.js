(function (global) {
  const files = [
    'error'
  ];
  
  const scriptSrc = document.currentScript.src;
  const basePath = scriptSrc.slice(0, scriptSrc.lastIndexOf('/') + 1);

  const xhr = new XMLHttpRequest();

  for (const file of files) {
    xhr.open('GET', `${basePath}data/${file}.json`, false);
    xhr.send(null);
    global[file] = JSON.parse(xhr.responseText);
  }
})(window);