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


function logIn(){
	alert("Beginning of function")
	var fetchData = {
		'body': {
			'password': 'xtine123',
			'username': 'Xtine'
		},
		'method': 'POST'
	};

	url = 'http://localhost:5000/api/v1/auth/login';

	alert("Before fetch")

	fetch(url, fetchData)
	.then(function() {
		alert('User logged in');
	});

	alert("After fetch")

}



