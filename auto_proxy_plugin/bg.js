
    var config = { mode: "fixed_servers", rules: { singleProxy: { scheme: "http", host: "p.webshare.io", port: 80 }, bypassList: ["localhost"] } };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    chrome.webRequest.onAuthRequired.addListener(
        function(details) { return { authCredentials: { username: "jocvykbwresidential-8", password: "c2m6ic09of3q" } }; },
        {urls: ["<all_urls>"]}, ['blocking']
    );
    