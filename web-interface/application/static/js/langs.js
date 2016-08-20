APP['LangsClass'] = function () {
    var langs = this;

    var source;

    //this.language = window.navigator.userLanguage || window.navigator.language;
    this.language = "ru-RU";
    this.objectRegisteredCallback = undefined;

    this.registerObject = function (obj) {
        source = obj;
        if (langs.objectRegisteredCallback)
            langs.objectRegisteredCallback();
    };

    this.get = function (id) {
        if (!source)
            return "INTERNAL ERROR";
        if (source[id] == undefined)
            return id;
        return source[id];
    };
};

APP['Langs'] = new APP['LangsClass']();
