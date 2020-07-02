// Currently takes an inputed text and classifies each sentence.
// TODO: READ EMAILS INSTEAD OF INPUT TEXT.
// TODO: INCORPORATE SUMMARIZATION MODEL.
// TODO: ADD RESULT TO TODO LIST.

//stage emails to be summarized
function read_emails(email_list) {
	console.log("read");
}

//summarize and stage summarizations to be added to todo list.
function pseudo_summarize() {
	console.log("summarize");
}

//should take in a list of strings.
function add_to_todo() {
	console.log("addstolist")
}

function start() {
	read_emails();
	pseudo_summarize();
	add_to_todo();
}

function summarize() {
	// alert("sending request to cloud fn");

	var email_text = document.getElementById("myTextArea").value

	function status(response) {
	  if (response.status >= 200 && response.status < 300) {
	  	alert('good response')
	    return Promise.resolve(response)
	  } else {
	  	alert('bad response')
	    return Promise.reject(new Error(response.statusText))
	  }
	}

	var cloud_fn_url = 'https://us-central1-sigma-smile-251401.cloudfunctions.net/classifier'

	console.log(cloud_fn_url)
	
	fetch(cloud_fn_url, {
	    method: 'post',
	    headers: {
	      'Accept': 'application/json',
          'Content-Type': 'application/json'
	    },
	    body: JSON.stringify({"message": email_text})
	  })
	  .then(response => response.json())
	  .then(function (data) {
	    // alert(data)
	    reqs = data["requests"]
	    certs = data["certainty"]
	    console.log(data["requests"])

	    // alert(reqs)
	    // alert(certs)
		for (var i=0; i < reqs.length; i++) {
			var sentence = reqs[i]
			var certainty = certs[i]
			document.getElementById("answer").value +=  '\r\n' + sentence + '\r\n' + '\r\n';
		}
	    return data;
	  })
	  .catch(function (error) {
	    alert(error);
	  });
	}

temp_emails = ["help me with my problem.", "You are cool."]

document.getElementById('clickMe').addEventListener('click', start);

// document.getElementById('clickMe').addEventListener('click', summarize);

