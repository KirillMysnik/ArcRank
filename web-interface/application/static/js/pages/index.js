document.title = "Index - ArcRank";

var ourNode = document.createElement('div');
var descNode = ourNode.appendChild(document.createElement('p'));
descNode.appendChild(document.createTextNode(APP['Langs'].get('INDEX_DESCRIPTION')));
descNode.classList.add('app-desc');

APP['Nodes'].get('main').appendChild(ourNode);
APP['PageLoader'].bindUnloadCallback('index.js', function () {
    APP['Nodes'].get('main').removeChild(ourNode);
});

APP['PageLoader'].setPageLoadedState('index.js');
