// This page is run in the background when the extension is active.

chrome.runtime.onInstalled.addListener(function() {

    // Here, the variable 'color' is stored to the color #cccccc (some gray). This is called upon in lines 6-8 of popup.js
    chrome.storage.sync.set({color: '#cccccc'}, function() {
      console.log('The color is gray.');
    });

    // Here, the variable 'color2' is stored to 'transparent'. This is called upon in lines 12-14 of popup.js
    chrome.storage.sync.set({color2: 'transparent'}, function() {
      console.log('The color is transparent.');
    });
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{

        // Sets the conditions to activate the extension. 
        conditions: [new chrome.declarativeContent.PageStateMatcher({

          // Notably, here if the host url contains a '.', the extension is active. This means that it is activated on the vast majority of web pages.
          pageUrl: {hostContains: '.'},
        })
        ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });