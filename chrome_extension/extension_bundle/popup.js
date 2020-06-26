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


document.getElementById('clickMe').addEventListener('click', summarize);
