var consoleBuffer = [];
function bufferConsoleMessage(args) {
    consoleBuffer.push(Array.prototype.slice.call(args).join(' '));
}
var original_log = console.log;
console.log = function() {
    bufferConsoleMessage(arguments);
};
window.addEventListener('pywebviewready', function() {
    consoleBuffer.forEach(function(msg) {
        window.pywebview.api.print_console(msg);
    });
    consoleBuffer = [];
    console.log = function() {
        window.pywebview.api.print_console(Array.prototype.slice.call(arguments).join(' '));
    };
});