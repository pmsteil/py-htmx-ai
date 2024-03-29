//
// This is a simple htmx extension that adds a new attribute `hx-ai` to htmx elements.
// This attribute is used to specify the prompt for the AI model.
// The extension also adds a new attribute `hx-ai-endpoint` to htmx elements.
// This attribute is used to specify the endpoint for the AI model.
// If the `hx-ai` attribute starts with `js:`, the extension will treat the value after `js:` as a JavaScript object.
// The extension will then set the `hx-vals` attribute to the JavaScript object.
// If the `hx-ai` attribute does not start with `js:`, the extension will set the `hx-vals` attribute to a JSON object with the prompt key set to the value of the `hx-ai` attribute.
// The extension will also set the `hx-post` attribute to the value of the `hx-ai-endpoint` attribute if it exists, otherwise it will set it to `http://
//
// Example:
// <button hx-ai="js:{prompt: 'Hello, world!'}" hx-ai-endpoint="http://sample.com/generate">
// <button hx-ai="Hello, world!" hx-ai-endpoint="http://sample.com/generate">
// <button hx-ai="js:{prompt: 'Hello, world!'}"
// <button hx-ai="Hello, world!"
//

htmx.defineExtension('ai', {
    onEvent: function (name, evt) {
        if (name === 'htmx:beforeProcessNode') {
            evt.target.querySelectorAll('[hx-ai]').forEach(el => {
                const nextEndpoint = el.closest(['hx-ai-endpoint'])?.getAttribute('hx-ai-endpoint');
                el.setAttribute('hx-get', nextEndpoint ?? 'http://127.0.0.1:3333/gen');
                el.setAttribute('hx-headers', '{"Content-Type": "application/json"}');
                if(el.getAttribute('hx-ai').startsWith('js:')){
                    el.setAttribute('hx-vals', 'js:{prompt: ' + el.getAttribute('hx-ai').replace('js:', '') + '}');
                }
                else {
                    el.setAttribute('hx-vals', '{"prompt": "' + el.getAttribute('hx-ai') + '"}');
                }
            });
        }
    }
})
