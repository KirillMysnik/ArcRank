APP['AJAXClass'] = function () {
    var ajax = this;

    this.post = function (url, data, successCallback, errorCallback) {
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState==4)
                if (xmlhttp.status==200)
                    successCallback(JSON.parse(xmlhttp.responseText));
                else
                    errorCallback();
        }

        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify(data, null, '\t'));
    };
};

APP['AJAX'] = new APP['AJAXClass']();
