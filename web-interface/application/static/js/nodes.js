APP['NodesClass'] = function () {
    var nodes = this;
    var storage = {};

    this.get = function (id) {
        return storage[id];
    };

    this.findAndRegister = function (id) {
        storage[id] = document.getElementById(id);
    };

    this.register = function (id, node) {
        storage[id] = node;
    };

    this.unregister = function (id) {
        storage[id] = undefined;
    };
};

APP['Nodes'] = new APP['NodesClass']();
