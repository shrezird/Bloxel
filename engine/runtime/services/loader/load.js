console.log("SERVICES: load.js started");

(function (global) {
  const data_names = [
    "error"
  ];
  const base_directory = document.currentScript.src.replace(/[^/]+$/, "");
  const preload_cache = {};

  for (const name of data_names) {
    const request = new XMLHttpRequest();
    request.open("GET", base_directory + "data/" + name + ".json", false);
    request.send(null);
    preload_cache[name] = JSON.parse(request.responseText);
    global[name] = new Proxy(preload_cache[name], {
      get(target, prop, receiver) {
        const requesting_file = window.location.pathname.split("/").pop();
        const requested_data = prop;
        const requested_file = name + ".json";
        if (prop in target) {
          console.log("SERVICES: load.js completed request from (" + requesting_file + ") for (" + requested_data + ") from (" + requested_file + ")");
          return Reflect.get(target, prop, receiver);
        } else {
          console.log("SERVICES: load.js received invalid request from (" + requesting_file + ") for (" + requested_data + ") from (" + requested_file + ")");
          if (preload_cache["error"] && preload_cache["error"].hasOwnProperty("invalid_request")) {
            return preload_cache["error"]["invalid_request"];
          }
          return undefined;
        }
      }
    });
  }
})(window);

console.log("SERVICES: load.js preloaded and cached the following data: " + Object.keys(preload_cache).join(", "));