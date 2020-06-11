chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({color: '#cccccc'}, function() {
      console.log('The color is black.');
    });
    chrome.storage.sync.set({color2: "transparent"}, function() {
      console.log('The color is transparent.');
    });
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {hostContains: '.'},
        })
        ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });