//stage emails to be summarized
function read_emails() {
	// alert("sending request to cloud fn");

	// var gmail_id = document.querySelector('[data-message-id]').getAttribute('data-legacy-message-id');
	// var user_id = 'me';

	// function getMessage(userId, messageId, callback) {
	//   var request = gapi.client.gmail.users.messages.get({
	//     'userId': userId,
	//     'id': messageId
	//   });
	//   request.execute(callback);
	// }
	// var email_text = getMessage(user_id, gmail_id)
	// console.log(email_text)
	return document.getElementById("myTextArea").value
}

var id_counter = 0;
//should take in list of strings
function add_to_todo(results) {
	if (results.length == 0) {
	  		alert('No tasks identified!')
	  	}
	// console.log(results.length)
	for (i in results) {
		id_counter += 1;
		//ALL OF THIS IS JUST SETTING UP THE ENVIRONMENT
		var col_div = document.createElement("div");
		var card_div = document.createElement("div");
		var tab_head_div = document.createElement("div");
		var tab_div = document.createElement("div");
		var card_body_div = document.createElement("div");

		col_div.appendChild(card_div);
		card_div.appendChild(tab_head_div);
		card_div.appendChild(tab_div);
		tab_div.append(card_body_div);

		col_div.className += "col-12";
		card_div.className += "card card-checklist";
		tab_head_div.setAttribute("role", "tab");
		tab_head_div.className += "tab-checklist";
		tab_div.className += "collapse";


		tab_div.setAttribute("id", "item".concat(id_counter));
		tab_div.setAttribute("data-parent", "#checklist");
		card_body_div.className += "card-body";

		//TEXT GOES HERE
		var inputText = document.createTextNode(results[i]);
		var header3 = document.createElement("h3");
		var itemText = document.createElement("a");
		var tabButton = document.createElement("a");
		
		tab_head_div.appendChild(header3);
		tab_head_div.appendChild(tabButton);
		header3.appendChild(itemText);

		header3.className += "mb-0";
		itemText.setAttribute("contenteditable", "true");
		itemText.setAttribute("name", "task");
		itemText.appendChild(inputText);

		tabButton.setAttribute("data-toggle", "collapse");
		tabButton.setAttribute("data-target", "#item".concat(id_counter))

		//DROPDOWN LINKS
		var option0 = document.createElement("span");
		option0.appendChild(document.createTextNode("Sender: EXTRACTION"));
		card_body_div.appendChild(option0);

		// var option1 = document.createElement("a");
		// option1.appendChild(document.createTextNode("Go to Original E-mail"));
		// card_body_div.appendChild(option1);

		var option2 = document.createElement("a");
		option2.appendChild(document.createTextNode("Remove"));
		card_body_div.appendChild(option2);

		option2.onclick = function() {
			col_div.style.display = "none"; 
		}

		var option3 = document.createElement("a");
		option3.appendChild(document.createTextNode("Move to Top"));
		card_body_div.appendChild(option3);

		option3.onclick = function() {
			var list = document.getElementById("checklist");
			list.insertBefore(col_div, list.childNodes[0]);
		}
	
		var element = document.getElementById("checklist");
		element.appendChild(col_div);
	}
}

function start () {
	var email_text = read_emails();
	summarize(email_text);
}

//Summarize also adds tasks to the to_do_list
function summarize(email_text) {

	function status(response) {
	  if (response.status >= 200 && response.status < 300) {
	  	alert('good response')
	    return Promise.resolve(response)
	  } else {
	  	alert('bad response')
	    return Promise.reject(new Error(response.statusText))
	  }
	}

	var cloud_fn_url = 'https://us-central1-sigma-smile-251401.cloudfunctions.net/classifier2'

	console.log(cloud_fn_url);
	
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
	  	var results = [];
	  	console.log("Checkpoint")
	    for (i in data) {
	    	results.push(data[i])
	    }
	 //    reqs = data["requests"]
	 //    certs = data["certainty"]

		// for (var i=0; i < reqs.length; i++) {
		// 	var sentence = reqs[i]
		// 	var certainty = certs[i]
		// 	document.getElementById("answer").value += sentence + '\r\n' + '\r\n';

		// 	results.push(sentence);
		// }
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

document.getElementById('add-item').addEventListener('click', function() {
	add_to_todo(['Text Here']);
})

document.getElementById('copy-clipboard').addEventListener('click', function() {
	var tasks = document.getElementsByName("task");
	var vals = [];
	for (var i=0; i<tasks.length; i++) {
		vals.push(tasks[i].childNodes[0].data);
	}
	var copyText = vals.join(", ");


	var dummy = document.createElement('textarea');
	document.body.appendChild(dummy);
	dummy.value = copyText;
	dummy.select();
	
	document.execCommand("copy");
	document.body.removeChild(dummy);
})

// document.getElementById('clickMe').addEventListener('click', summarize);


// ******** WORK IN PROGRESS ON GMAIL API ********

// gapi.load('client:auth2', () => {
//     gapi.client.load('gmail', 'v1', () => {
//       console.log('Loaded Gmail');
//     });
// })

// var request = gapi.client.gmail.users

// var gmail_id = document.querySelector('[data-message-id]').getAttribute('data-legacy-message-id');
// var user_id = 'me';

// function getMessage(userId, messageId, callback) {
//   var request = gapi.client.gmail.users.messages.get({
//     'userId': userId,
//     'id': messageId
//   });
//   request.execute(callback);
// }

// var email_text = getMessage(user_id,gmail_id);
// console.log(email_text);


// function getMessage() {
// 	var request = gapi.client.gmail.users.messages.get({
// 		'userId': 'me',
// 		'id': 'percivalchen@berkeley.edu'
// 	});

// 	request.execute(function(response) {
// 		$.each(response.m$.each(response.messages, function() {
//       var messageRequest = gapi.client.gmail.users.messages.get({
//         'userId': 'me',
//         'id': this.id
//     })
//       }));
// }
// );
// };
