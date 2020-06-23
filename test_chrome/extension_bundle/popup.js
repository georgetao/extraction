// var x = document.getElementById("myTextArea").value;
var globalVariable={
       // x: document.getElementById("myTextArea").value
       x:document.getElementById("answer").value
    };

// document.getElementById("answer").value= "This should appear in the answer box.";
// document.getElementById("myTextArea").value= "This should appear in the TextArea box.";
console.log(document.getElementById("myTextArea").value);

function summarize() {
	// alert(document.getElementById("myTextArea").value);
	chrome.tabs.executeScript(null, { file: "jquery-2.2.js" }, function() {
	    chrome.tabs.executeScript(null, { file: "content.js" });
	    var textToSend = textToSend;
	});
};
document.getElementById('clickMe').addEventListener('click', summarize);
