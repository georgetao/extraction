function summarize() {
	// alert("sending request to cloud fn");

	var email_text = document.getElementById("myTextArea").value

	function status(response) {
	  if (response.status >= 200 && response.status < 300) {
	    return Promise.resolve(response)
	  } else {
	    return Promise.reject(new Error(response.statusText))
	  }
	}

	var cloud_fn_url = 'https://us-central1-sigma-smile-251401.cloudfunctions.net/classifier'
	
	fetch(cloud_fn_url, {
	    method: 'post',
	    headers: {
	      'Accept': 'application/json',
          'Content-Type': 'application/json'
	    },
	    body: JSON.stringify({"message": email_text})
	  })
	  .then(response => response.text())
	  .then(function (data) {
	    // alert("data request succeeded with json response");
	    // alert(data);
	    document.getElementById("answer").value = data;
	    return data;
	  })
	  .catch(function (error) {
	    alert(error);
	  });
	}


document.getElementById('clickMe').addEventListener('click', summarize);
