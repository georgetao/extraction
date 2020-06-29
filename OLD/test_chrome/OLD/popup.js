// variable assignment; these variables are refering to the button elements in popup.html (id=<STRING>). Button elements are in quotes, new js variables are NOT.
let changeColor = document.getElementById('changeColor');
let reset = document.getElementById('reset');

// Obtaining the stored color (from background.js) called "color"
chrome.storage.sync.get('color', function(data) {
    changeColor.style.backgroundColor = data.color;
    changeColor.setAttribute('value', data.color);
});

// Obtaining the stored color (from background.js) called "color2"
chrome.storage.sync.get('color2', function(data) {
    reset.style.backgroundColor = data.color2;
    reset.setAttribute('value', data.color2);
});

// Programming what happens when you click on the particlar button element. Here, 'changeColor' is the js element instantiated in line 2. Upon clicking the element in the chrome pop-up:
changeColor.onclick = function(element) {

    // Instantiates the local variable color
    let color = element.target.value;

    // Not sure what this does exactly...
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {

        // Executes the scripe here, specifically it sets the color to the variable color instantiated at line 21
    	chrome.tabs.executeScript(
        	tabs[0].id,
        	{code: 'document.body.style.backgroundColor = "' + color + '";'});
    });
  };

// Same as above here, except this is refering to the 'reset' instatiated on line 3.
reset.onclick = function(element) {

    // Instantiates the local variable color and executes the script. Note, this is different from the local variable in line 21. Here, it's value is 'transparent' according to background.js
	let color = element.target.value;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	chrome.tabs.executeScript(
        	tabs[0].id,
        	{code: 'document.body.style.backgroundColor = "' + color + '";'});
    });
  };