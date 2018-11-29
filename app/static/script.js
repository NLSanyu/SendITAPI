var d, dest, url = 'localhost:5000/api/v1';

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
	var fetchData = {
		'body': {
			'email': 'xtine@gmail.com',
			'password': 'xtine123',
			'username': 'Xtine'
		},
		'method': 'POST'
	};

	url = 'localhost:5000/api/v1/auth/signup';

	alert("Function signUp");

	fetch(url, fetchData)
	.then(function() {
		alert('User signed up');
	});
}


function logIn(){
	var fetchData = {
		'body': {
			'password': 'xtine123',
			'username': 'Xtine'
		},
		'method': 'POST'
	};

	url = 'http://localhost:5000/api/v1/auth/login';

	fetch(url, fetchData)
	.then(function() {
		alert('User logged in');
	});
}

function signOut(){

}


function changeDestination(){
	d = document.getElementById('st');
	if (d.innerHTML != "Delivered"){
		dest = document.getElementById('dest');
		dest.innerHTML = '<form> <textarea name="parcel_details" rows="2"> </textarea> <input type="submit" name="new_dest" value="Confirm" id="submit-dest"> </form>';
	}
	else{
		alert("Parcel already delivered");
	}
}

function cancelOrder(){
	alert("Order cancelled");
}

function changePresentLocation(){
	document.getElementById('pres-location').innerHTML = '<form name="change_pres_location"> <textarea name="parcel_details" rows="2"> </textarea> <input type="submit" name="new_pres_location" value="Confirm" id="submit-dest"> </form>';
}

function changeStatus(){
	document.getElementById('status').innerHTML = '<form name="change_status"> <textarea name="parcel_details" rows="2"> </textarea> <input type="submit" name="new_status" value="Confirm" id="submit-dest"> </form>';
}



