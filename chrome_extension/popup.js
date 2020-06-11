let changeColor = document.getElementById('changeColor');
let reset = document.getElementById('reset');

chrome.storage.sync.get('color', function(data) {
    changeColor.style.backgroundColor = data.color;
    changeColor.setAttribute('value', data.color);
});

chrome.storage.sync.get('color2', function(data) {
    changeColor.style.backgroundColor = data.color;
    changeColor.setAttribute('value2', data.color);
});

changeColor.onclick = function(element) {
    let color = element.target.value;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	chrome.tabs.executeScript(
        	tabs[0].id,
        	{code: 'document.body.style.backgroundColor = "' + color + '";'});
    });
  };

reset.onclick = function(element) {
	let color = element.target.value;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	chrome.tabs.executeScript(
        	tabs[0].id,
        	{code: 'document.body.style.backgroundColor = "' + color + '";'});
    });
  };