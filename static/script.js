var timeoutID;
// var timeout = 25000; //change to 1000

function setupchatroom() {
	timeoutID = window.setTimeout(poller, 1000);
}

function signin() {
    var httpRequest = new XMLHttpRequest();
    if (!httpRequest) {
        alert('Giving up :( Cannot create an XMLHTTP instance');
        return false;
    }
    var username = document.getElementById("login_username").value;
    var password = document.getElementById("login_password").value;

    httpRequest.onload = function() {
        if (httpRequest.status === 200) {
            if (httpRequest.responseText === "ok") {
                window.location.href = "/chatroom";
            } else {
                alert(httpRequest.responseText);
                document.getElementById("login_username").value = "";
                document.getElementById("login_password").value = "";
            }
        } else {
            alert("Error with the request. Please try again.");
        }
    };

    httpRequest.onerror = function() {
        alert("Request failed. Please check your internet connection and try again.");
    };

    httpRequest.open("POST", "/login");
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    var data = "username=" + encodeURIComponent(username) + "&password=" + encodeURIComponent(password);
    httpRequest.send(data);
}


function register_submit() {
	var httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	var username = document.getElementById("new_username").value;
	var password = document.getElementById("new_pw").value;
	var password2 = document.getElementById("new_pw_2").value;

	httpRequest.onreadystatechange = function() {
		if(httpRequest.readyState === XMLHttpRequest.DONE) {
			if (httpRequest.status === 200) {
				if (httpRequest.responseText == "ok") {
					//window.location.href = "/"; //back to login page
					//alert("Created new account!");
				} else {
					alert(httpRequest.responseText);
				}
			}
		}
	};
	httpRequest.open("POST", "/newaccount");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "username=" + username + "&password=" + password + "&password2=" + password2;
	httpRequest.send(data);
	httpRequest.onload = function () {
		if (httpRequest.responseText == "ok") {
			alert('created new account');
		}
		//alert(httpRequest.responseText);
	}
}

function create_chatroom() {
	var httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	var roomname = document.getElementById("roomname").value;

	httpRequest.onreadystatechange = function() {
		if (httpRequest.readyState === XMLHttpRequest.DONE && httpRequest.status === 200) {
			//alert(httpRequest.responseText);
			document.getElementById("roomname").value = "";
		}
	};
	httpRequest.open("POST", "/newroom");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "roomname=" + roomname;
	httpRequest.send(data);
	httpRequest.onload = function () {
		alert(httpRequest.responseText);
		window.location.href = "/chatroom";
	}
}

function addDeleteButton(roomname) {
	//when clicked call delete_room

	var btn = document.createElement("button");
	btn.innerText = "delete";
	btn.className = "btnDelete";
	btn.onclick = function() { delete_room(roomname); };
	var parentId = "room" + roomname;
	document.getElementById(parentId).appendChild(btn);
}


function delete_room(roomname) {
	var httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	httpRequest.open("POST", "/deleteroom");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "roomname=" + roomname;
	httpRequest.send(data);
	httpRequest.onload = function () {
		alert(httpRequest.responseText);
		location.reload();
	}
}

function new_message() {
	var httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	httpRequest.onreadystatechange = function() {
		if (httpRequest.readyState === XMLHttpRequest.DONE && httpRequest.status === 200) {
			document.getElementById('newMessage').value = "";
		}
	};
	var msg = document.getElementById('newMessage').value;
	httpRequest.open("POST", "/newmsg");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "msg=" + msg;
	httpRequest.send(data);
	httpRequest.onload = function () {
		// alert(httpRequest.responseText);
	}
}

function poller() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	httpRequest.onreadystatechange = function() { handlePoll(httpRequest) };
	httpRequest.open("GET", "/updatemsg");
	httpRequest.send();
}

function handlePoll(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			// alert("polling")
			var newMsg = JSON.parse(httpRequest.responseText);

			if(newMsg == "roomdeleted") {
				alert("The room you were in was deleted.  Redirecting to navigation page.");
				window.location.href = "/chatroom";
			} else {
				for (var i = 0; i < newMsg.length; i++) {
					addNewMessage(newMsg[i]);
				}
				timeoutID = window.setTimeout(poller, 1000);
			}


		} else {
			alert("There was a problem with the poll request.  you'll need to refresh the page to receive updates again!");
		}
	}
}

function addNewMessage(msg) {
	var nm = document.getElementById('nomessage');
	if (nm) {
		nm.textContent = "";
	}

	var msgDiv = document.getElementById('messagediv');

	var hr = document.createElement("hr");
	hr.style.backgroundColor = '#645252';

	var h4 = document.createElement("h4");
	h4.style.textDecoration = "underline";
	h4.style.display = "inline";
	h4.textContent = msg.author;

	var span = document.createElement('span');
	span.style.width = "20px";

	var p = document.createElement('p');
	p.style.display = "inline";
	p.textContent = "  Published: " + msg.pub_date;

	var p2 = document.createElement('p');
	p2.style.margin = "5px 0px";
	p2.textContent = msg.text;

	msgDiv.appendChild(hr);
	msgDiv.appendChild(h4);
	msgDiv.appendChild(span);
	msgDiv.appendChild(p);
	msgDiv.appendChild(p2);
}


// window.addEventListener("load", setup, true);
