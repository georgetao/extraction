// alert("Generating summary highlights. This may take up to 30 seconds depending on length of article.");

// document.getElementById("clickMe").onclick = doFunction;

console.log(6)


// capture all text
var path = window.location.pathname;
var page = path.split("/").pop();
// var page = window.location.href;
console.log(page);

if (document.getElementById("myTextArea") == null) {
	console.log("This value is null unfortunately!!");
};

var textToSend = document.getElementByName("myTextArea");
// var textToSend = "This is a HARDCODED string";
// alert(globalVariable.x);
console.log(textToSend)

// summarize and send back
var api_url = 'https://us-central1-sigma-smile-251401.cloudfunctions.net/SummarLight-1';

fetch(api_url, {
  method: 'POST',
  body: JSON.stringify(textToSend),
  headers:{
    'Content-Type': 'application/json'
  } })
.then(res => res.text())
.then(res => console.log(res))
.catch(error => console.error('Error:', error));

// document.getElementById('clickme').addEventListener('click', call(doFunction));
// var textToSend = document.getElementById("myTextArea");
// console.log(textToSend);
// document.getElementById("clickMe").onclick = doFunction;

