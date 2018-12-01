var url, email, password, phoneNumber, username;

function getAllParcels(){
	fetch(url)
	.then(function() {
		// Your code for handling the data you get from the API
	})
	.catch(function() {
		alert("An error occured");
	});
}

function signUp(){
	//alert("......");
	email = document.getElementsById("email1").value;
	password = document.getElementsById("password1").value;
	phoneNumber = document.getElementsById("phone1").value;
	username = document.getElementsById("uname1").value;

	var fetchData = {
		'body': {
			'email': email,
			'password': password,
			'phone_number': phoneNumber,
			'username': username
		},
		'method': 'POST'
	};

	url = 'localhost:5000/api/v1/auth/signup';

	alert("Function signUp");

	fetch(url, fetchData)
	.then(function() {
		alert('User signed up');
	})
	.catch(function() {
		alert("An error occured");
	});

	document.location = "profile.html";
}

function signIn(){
	let url = 'http://127.0.0.1:5000/api/v1/auth/login';
	let username = document.getElementById('uname2').value;
	let password = document.getElementById('password2').value;

	let request_data = {
		"username": username,
		"password": password
	}

	let request_body = {
		method: 'POST',
            body: JSON.stringify(request_data),
            headers: {
                "Content-Type": "application/json"
			},
			mode: 'cors'
	}

	fetch(url, request_body)
	.then((res) => res.json())
	.then((data) => {
		reply = data["message"]
		if(reply){
			alert("Got msg")
			window.location.href = "app/templates/user/index.html";
		}
		else{
			alert("Did not get msg")
		}
	})
	.catch((err)=>console.log(err))
}


