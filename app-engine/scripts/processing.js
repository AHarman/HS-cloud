
var stop = window.setInterval(checkStatus, 3000);

function checkStatus()
{
	var xhr = new XMLHttpRequest();
	console.log("Here")
	xhr.onreadystatechange = function(e) {
		if (xhr.readyState == XMLHttpRequest.DONE)
		{
			if (xhr.responseText == "0")
			{
				console.log("We're done here!");
				document.getElementById("waitingText").innerHTML = "<p>Processing complete!</p>";
				clearInterval(stop)
				window.location.href="/results"
			}
			else
			{
				console.log("More to go");
				console.log(xhr.responseText);
				text = "<p>Currently waiting for results. This should take less than a minute.</p>"
				text += "<br/></br>"
				text += "<p>" + xhr.responseText + " images still to process</p>";
				document.getElementById("waitingText").innerHTML = text
			}
		}
	}
	xhr.open("POST", "/processing", true);
	xhr.send();
}