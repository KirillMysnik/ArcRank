new (function () {
    var config;

    var activeNavLink;
    var switchActiveNavLink = function (node) {
        if (activeNavLink)
            activeNavLink.classList.remove('active');

        activeNavLink = node;
        activeNavLink.classList.add('active');
    };

    var langRegisteredCallback = function () {
        pageIdIndex = location.href.indexOf('/#!/');
        if (pageIdIndex < 0)
            pageId = "index.js";
        else
            pageId = location.href.slice(pageIdIndex + '/#!/'.length);

        var mainNode = document.body.appendChild(document.createElement('div'));
        APP['Nodes'].register('main', mainNode);
        mainNode.classList.add('main');

        var logoNode = mainNode.appendChild(document.createElement('a'));
        logoNode.href = "/#!/index.js";
        logoNode.classList.add('logo');

        var logoNodeHoverImage = new Image();    // Pre-load hover image
        logoNodeHoverImage.src = "/static/img/logo_hover.png";

        var navWrapNode = mainNode.appendChild(document.createElement('div'));
        navWrapNode.classList.add('nav-container-wrap');

        var navNode = navWrapNode.appendChild(document.createElement('ul'));
        APP['Nodes'].register('nav', navNode);
        navNode.classList.add('nav-container');

        config['nav-links'].forEach(function (value, i, arr) {
            var liNode = navNode.appendChild(document.createElement('li'));
            var linkNode = liNode.appendChild(document.createElement('a'));
            if (value['external'])
                linkNode.href = value['url'];
            else {
                linkNode.href = "/#!/" + value['url'];

                if (value['url'] == pageId)
                    switchActiveNavLink(linkNode);
            }
            linkNode.appendChild(document.createTextNode(APP['Langs'].get(value['title'])));
            linkNode.addEventListener('click', function (e) {
                switchActiveNavLink(this);
            });
        });

        navNode.appendChild(document.createElement('div')).classList.add('clear');

        APP['PageLoader'].scanAjaxUrls(navNode);
        APP['PageLoader'].openPage(pageId);
    };

    var ajaxCallback = function (data) {
        config = data;

        APP['Langs'].objectRegisteredCallback = langRegisteredCallback;

        var language = APP['Langs'].language;
        if (config['languages'].indexOf(language) > -1)
            APP['ScriptLoader'].loadScript("/static/js/langs/" + language + ".js");
        else
            APP['ScriptLoader'].loadScript("/static/js/langs/" + config['default-language'] + ".js");
    };

    APP['AJAX'].post('/ajax-init', {}, ajaxCallback, function () {
        alert("AJAX ERROR");
    });
})();
