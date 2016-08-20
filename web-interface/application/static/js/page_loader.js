APP['PageLoaderClass'] = function () {
    if (!APP['ScriptLoader'])
        console.log("PageLoader should only be initialized after ScriptLoader initialization.");

    var pageLoader = this;
    var overlay;
    var currentUrl;

    this.currentPageId = undefined;

    this.openPage = function (pageId) {
        console.log("Opening '" + pageId + "'...");

        if (!overlay) {
            overlay = document.body.appendChild(document.createElement('div'));
            overlay.classList.add('page-loader-overlay');
        }

        if (currentUrl)
            APP['ScriptLoader'].unloadScript(currentUrl);

        pageLoader.currentPageId = pageId;
        currentUrl = "/static/js/pages/" + pageId;
        location.href = "/#!/" + pageId;
        APP['ScriptLoader'].loadScript(currentUrl);
    };

    this.scanAjaxUrls = function (node) {
        var links = node.getElementsByTagName('a');
        for (var i = 0; i < links.length; i++) {
            (function (link) {
                link.addEventListener('click', function (e) {
                    pageIdIndex = link.href.indexOf('/#!/');
                    if (pageIdIndex < 0)
                        return true;

                    pageId = link.href.slice(pageIdIndex + '/#!/'.length);
                    pageLoader.openPage(pageId);
                    e.preventDefault();
                    return false;
                });
            })(links[i]);
        }
    };

    this.bindUnloadCallback = function (pageId, callback) {
        APP['ScriptLoader'].bindUnloadCallback("/static/js/pages/" + pageId, callback);
    };

    this.setPageLoadedState = function (pageId) {
        APP['ScriptLoader'].setScriptLoadedState("/static/js/pages/" + pageId);

        if (overlay) {
            document.body.removeChild(overlay);
            overlay = undefined;
        }
    };
};

APP['PageLoader'] = new APP['PageLoaderClass']();
