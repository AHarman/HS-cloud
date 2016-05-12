imagesUploaded = 0; 
imagesToUpload = 0;

// Number of uploads to do at once
// Set to 1 so we can easily reattempt uploads
simulUploadLimit = 1

function getLinks()
{
	linkTags = document.getElementsByClassName("uploadLink");
	links = [];
	for (i = 0; i < linkTags.length; i++)
	{
		links.push(linkTags[i].getAttribute("upload"));
	}
	return links
}

function successMessage()
{
	console.log("All images uploaded");
	document.getElementById("uploadStatus").innerHTML = "All images uploaded";
	window.location.href="/processing"
}

function updateUploadStatus()
{
	console.log(imagesUploaded + " uploaded");
	document.getElementById("uploadStatus").innerHTML = "Uploaded " + imagesUploaded + " images of " + imagesToUpload;
}

function transferComplete(evt)
{
	console.log("success");
	imagesUploaded += 1;
	if (imagesUploaded == imagesToUpload)
	{
		successMessage();
	}
	else if (imagesUploaded % simulUploadLimit == 0)
	{
		updateUploadStatus(imagesUploaded, imagesToUpload);
		nUploads(simulUploadLimit);
	}
	else
	{
		updateUploadStatus(imagesUploaded, imagesToUpload);
	}
}

function transferFailed(evt) {
	console.log("File did not upload, retrying file");
	nUploads(1);
}


function nUploads(n)
{
	var file = document.getElementById('files');
	links = getLinks();
	cap = Math.min(imagesUploaded + n, imagesToUpload)
	var xhrs = []
	for (var i = imagesUploaded; i < cap; i++)
	{
		var formData = new FormData();
		formData.append("screenshot", file.files[i]);
		formData.append("index", i + imagesUploaded);
		var xhr = new XMLHttpRequest();
		xhrs.push(xhr);
		xhr.addEventListener("load", transferComplete);
		xhr.addEventListener("error", transferFailed);
		xhr.open('POST', links[i], true);
		xhr.send(formData);
	}
}

function upload()
{
	var file = document.getElementById('files');

	if(file.files.length)
	{
		imagesToUpload = file.files.length;
		updateUploadStatus()
		nUploads(simulUploadLimit);
	}
}