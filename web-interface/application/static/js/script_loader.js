APP['ScriptLoaderClass'] = function () {
    var scriptLoader = this;

    var Script = function (url) {
        var script = this;
        var node;

        var fullyLoaded = false, pendingUnload = false;

        this.unloadCallback = null;

        this.load = function () {
            if (node) {
                console.log("Script: Attempt to load '" + url + "' twice without unloading.");
                return;
            }
            node = document.createElement('script');
            node.type = "application/javascript";
            node.src = url;
            document.head.appendChild(node);
        };

        this.unload = function () {
            if (!node) {
                console.log("Script: Attempt to unload '" + url + "' which is not loaded.");
                return;
            }

            if (fullyLoaded) {
                if (script.unloadCallback)
                    script.unloadCallback();

                document.head.removeChild(node);
                node = undefined;
            }
            else
                pendingUnload = true;
        };

        this.setLoadedState = function () {
            fullyLoaded = true;
            if (pendingUnload)
                script.unload();
        };
    };

    var loadedScripts = {};

    this.loadScript = function (url) {
        if (loadedScripts[url])
            loadedScripts[url].unload();

        loadedScripts[url] = new Script(url);
        loadedScripts[url].load();
    };

    this.unloadScript = function (url) {
        if (!loadedScripts[url]) {
            console.log("ScriptLoaderClass: Attempt to unload '" + url + "' which is not loaded.")
        }
        loadedScripts[url].unload();
        loadedScripts[url] = undefined;
    };

    this.isScriptLoaded = function (url) {
        return loadedScripts[url] != undefined;
    };

    this.bindUnloadCallback = function (url, callback) {
        if (!loadedScripts[url]) {
            console.log("ScriptLoaderClass: Attempt to bind unload callback to a script '" + url + "' which is not loaded.");
            return;
        }
        loadedScripts[url].unloadCallback = callback;
    };

    this.setScriptLoadedState = function (url) {
        if (!loadedScripts[url]) {
            console.log("ScriptLoaderClass: Attempt to set script's loaded state on '" + url + "' which is not loaded.");
            return;
        }
        loadedScripts[url].setLoadedState();
    };
};

APP['ScriptLoader'] = new APP['ScriptLoaderClass']();
