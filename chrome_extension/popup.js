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


function saveTextAsFile() {
  var textToWrite = document.getElementById('textArea').innerHTML;
  var textFileAsBlob = new Blob([ textToWrite ], { type: 'text/plain' });
  var fileNameToSaveAs = "/User/percivalchen/Documents/Github/capstone/chrome_extension/temp.txt";

  var downloadLink = document.createElement("a");
  downloadLink.download = fileNameToSaveAs;
  downloadLink.innerHTML = "Download File";
  if (window.webkitURL != null) {
    // Chrome allows the link to be clicked without actually adding it to the DOM.
    downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
  } else {
    // Firefox requires the link to be added to the DOM before it can be clicked.
    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
    downloadLink.onclick = destroyClickedElement;
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
  }

  downloadLink.click();
}

var button = document.getElementById('save');
if(button){
  button.addEventListener('click', saveTextAsFile);
}

function destroyClickedElement(event) {
  // remove the link from the DOM
  document.body.removeChild(event.target);
}