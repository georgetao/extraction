// Currently takes an inputed text and classifies each sentence.
// TODO: READ EMAILS INSTEAD OF INPUT TEXT.
// TODO: INCORPORATE SUMMARIZATION MODEL.
// TODO: ADD RESULT TO TODO LIST.

//stage emails to be summarized
function read_emails() {
	console.log("read");
}

//summarize and stage summarizations to be added to todo list.
function pseudo_summarize() {
	console.log("summarize");
}

//should take in string
function add_to_todo(results) {
	for (i in results) {
		//ALL OF THIS IS JUST SETTING UP THE ENVIRONMENT
		var row_div = document.createElement("div");
		var col1_div = document.createElement("div");
		var col2_div = document.createElement("div");
		var dropdown_div = document.createElement("div");
		var dropdown_menu_div = document.createElement("div");

		row_div.appendChild(col1_div);
		row_div.appendChild(col2_div);
		col2_div.appendChild(dropdown_div);

		row_div.className += "row";
		col1_div.className += "col-10";
		col2_div.className += "col-2";
		dropdown_div.className += "dropdown";
		dropdown_menu_div.className += "dropdown-menu"
		dropdown_menu_div.setAttribute("aria-labelledby", "dropdownMenuButton");

		//TEXT GOES HERE
		var text = document.createTextNode(results[i]);
		col1_div.appendChild(text);

		var button = document.createElement("button");
		button.className += "btn btn-secondary dropdown-toggle";
		button.setAttribute("type", "button");
		button.setAttribute("id", "dropdownMenuButton");
		button.setAttribute("data-toggle", "dropdown");
		button.setAttribute("aria-has-popup", "true");
		button.setAttribute("aria-expanded", "false");
		dropdown_div.appendChild(button);
		dropdown_div.appendChild(dropdown_menu_div);

		var buttonImg = document.createElement("img");
		buttonImg.src = "img/settings.png";
		buttonImg.alt = "Settings";
		button.appendChild(buttonImg);


		//DROPDOWN LINKS
		var options = ["Sender: George Tao", "Go to Original E-mail", "Mark as Read", "Mark as Spam"];
		var links =["#", "#", "#", "#"];
		for (var i=0; i<options.length; i++){
			var option = document.createElement("a");
			option.className = "dropdown-item";
			option.setAttribute("href", links[i]);
			option.appendChild(document.createTextNode(options[i]));
			dropdown_menu_div.appendChild(option);
		}
		
		var element = document.getElementById("checklist");
		element.appendChild(row_div);
	}
}

function start () {
	read_emails();
	pseudo_summarize();

	summarize();
	// add_to_todo(results);
}

function summarize() {
	// alert("sending request to cloud fn");

	var gmail_id = document.querySelector('[data-message-id]').getAttribute('data-legacy-message-id');
	var user_id = 'me';

	function getMessage(userId, messageId, callback) {
	  var request = gapi.client.gmail.users.messages.get({
	    'userId': userId,
	    'id': messageId
	  });
	  request.execute(callback);
	}

	// var email_text = document.getElementById("myTextArea").value
	var email_text = getMessage(user_id, gmail_id)
	console.log(email_text)

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
	
	return fetch(cloud_fn_url, {
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
	    var results = [];


	    // alert(reqs)
	    // alert(certs)
		for (var i=0; i < reqs.length; i++) {
			var sentence = reqs[i]
			var certainty = certs[i]
			// document.getElementById("answer").value += sentence + '\r\n' + '\r\n';

			results.push(sentence);
		}
	    return results;
	  })
	  .then(function(data) {
	  	add_to_todo(data);
	  })
	  .catch(function (error) {
	    alert(error);
	  });
	}

document.getElementById('clickMe').addEventListener('click', start);

// document.getElementById('clickMe').addEventListener('click', summarize);


gapi.load('client:auth2', () => {
    gapi.client.load('gmail', 'v1', () => {
      console.log('Loaded Gmail');
    });
})

var gmail_id = document.querySelector('[data-message-id]').getAttribute('data-legacy-message-id');
var user_id = 'me';

function getMessage(userId, messageId, callback) {
  var request = gapi.client.gmail.users.messages.get({
    'userId': userId,
    'id': messageId
  });
  request.execute(callback);
}

var email_text = getMessage(user_id,gmail_id);
console.log(email_text);