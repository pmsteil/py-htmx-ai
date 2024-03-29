htmx.defineExtension('ai', {
    onEvent: function (name, evt) {
        if (name === 'htmx:beforeProcessNode') {
            evt.target.querySelectorAll('[hx-ai]').forEach(el => {
                const nextEndpoint = el.closest(['hx-ai-endpoint'])?.getAttribute('hx-ai-endpoint');
                el.setAttribute('hx-post', nextEndpoint ?? 'http://127.0.0.1:3333/generate');
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
