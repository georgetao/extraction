
// // Load GAPI?
// var head = document.getElementsByTagName('head')[0];
// var script = document.createElement('script');
// script.type = 'text/javascript';
// script.src = "https://apis.google.com/js/client.js?onload=onGAPILoad";
// head.appendChild(script);


// var API_KEY = 'foo'
// var DISCOVERY_DOCS = 'bar'

// function onGAPILoad() {
//   alert('gapi loaded')

//   gapi.client.init({
//     // Don't pass client nor scope as these will init auth2, which we don't want
//     apiKey: API_KEY,
//     discoveryDocs: DISCOVERY_DOCS,
//   }).then(function () {
//     console.log('gapi initialized')
//   }, function(error) {
//     console.log('error', error)
//   });
// }


// //oauth2 auth
// chrome.identity.getAuthToken(
//   {'interactive': true},
//   function(){
//     //load Google's javascript client libraries
//     window.gapi_onload = authorize;
//     // loadScript('https://apis.google.com/js/client.js');

//   }
// );

// function loadScript(url){
//   var request = new XMLHttpRequest();

//   request.onreadystatechange = function(){
//     if(request.readyState !== 4) {
//       return;
//     }

//     if(request.status !== 200){
//       return;
//     }

//     eval(request.responseText);
//   };

//   request.open('GET', url);
//   request.send();
// }

// function authorize(){
//   gapi.auth.authorize(
//     {
//       client_id: '633127998444-nkn7phogkfbod133ej0k2vucm76l13kl.apps.googleusercontent.com',
//       immediate: true,
//       scope: 'https://www.googleapis.com/auth/gmail.readonly'
//     },
//     function(){
//       gapi.client.load('gmail', 'v1', gmailAPILoaded);
//     }
//   );
// }

// function gmailAPILoaded(){
//     //do stuff here
// }


//  here are some utility functions for making common gmail requests 
// function getThreads(query, labels){
//   return gapi.client.gmail.users.threads.list({
//     userId: 'me',
//     q: query, //optional query
//     labelIds: labels //optional labels
//   }); //returns a promise
// }

// //takes in an array of threads from the getThreads response
// function getThreadDetails(threads){
//   var batch = new gapi.client.newBatch();

//   for(var ii=0; ii<threads.length; ii++){
//     batch.add(gapi.client.gmail.users.threads.get({
//       userId: 'me',
//       id: threads[ii].id
//     }));
//   }

//   return batch;
// }

// function getThreadHTML(threadDetails){
//   var body = threadDetails.result.messages[0].payload.parts[1].body.data;
//   return B64.decode(body);
// }

// function archiveThread(id){
//   var request = gapi.client.request(
//     {
//       path: '/gmail/v1/users/me/threads/' + id + '/modify',
//       method: 'POST',
//       body: {
//         removeLabelIds: ['INBOX']
//       }
//     }
//   );

//   request.execute();
// }