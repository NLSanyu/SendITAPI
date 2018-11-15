var d, dest, signedIn;

function signIn(){
	signedIn = true;
}

function signOut(){
	signedIn = false;
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



