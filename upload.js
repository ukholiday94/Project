var fileSelected = null;
var socket = null;
(function () {
	var uploadfiles = document.querySelector('#uploadfiles');
	uploadfiles.addEventListener('change', function () {
		if(this.files[0].size > 4294967296){
			alert("4GB보다 작은 크기만 전송가능합니다.");
		}
		else{
			fileSelected = this.files[0];
		}
	}, false);
}());

function upload(){
	if(fileSelected != null)
	{
		alert("업로드 시작");
		
		Uploader('ws://localhost:8082', fileSelected)
		
		var btn = document.getElementById("downbutton");
		btn.disabled = "disabled";
	}
	else{
		alert("4GB보다 작은 크기만 전송가능합니다.");
	}
}
function download(){
	alert("다운로드 시작");
	
	Downloader('ws://localhost:8082')
	
	var btn = document.getElementById("upbutton");
	btn.disabled = "disabled";
}


function disconnect() {
 if (socket != 0) {
  socket.close();
 }
}
function FileSlicer(file) {
	this.sliceSize = 1024;	
	this.slices = Math.ceil(file.size / this.sliceSize);

	this.currentSlice = 0;

	this.getNextSlice = function() {
		var start = this.currentSlice * this.sliceSize;
		var end = Math.min((this.currentSlice+1) * this.sliceSize, file.size);
		++this.currentSlice;

		return file.slice(start, end);
	}
}
function Uploader(url, file) {
	var fs = new FileSlicer(file);
	socket = new WebSocket(url);
	socket.binaryType = 'arraybuffer'

	socket.onopen = function() {
		socket.send("send");
		socket.send(file.name);
		socket.send(file.size);
	}
	socket.onmessage = function(ms){
		if(ms.data=="ok"){
			alert("Sending...");
			for(var i = 0; i < fs.slices; ++i) {
				socket.send(fs.getNextSlice());
			}
			disconnect()
		}
	}
	socket.onclose = function() {
		alert("업로드 종료");
		var downbtn = document.getElementById("downbutton");
		downbtn.disabled = false;
	};
}
function Downloader(url) {
	socket = new WebSocket(url);
	socket.binaryType = 'blob';
	var i = 2;
	var filename = null;
	var filesize = null;
	var data = "";
	
	socket.onopen = function() {
		socket.send("recive");
	}
	socket.onmessage = function(ms){
		if(ms.data=="ok"){
			alert("Receiving...");
		}
		else if(i==2){
			filename = ms.data;
			i--;
		}
		else if(i==1){
			filesize = ms.data;
			i--;
		}
		else{
			tmp = ms.data;
			data = new Blob([data,tmp], {type: "application/octet-stream"}); //text/plain
		}
	}
	socket.onclose = function() {
		var SaveAsURL = window.URL.createObjectURL(data);
		var downloadLink = document.createElement("a");
		downloadLink.download = filename;
		downloadLink.innerHTML = "Download File";
		downloadLink.href = SaveAsURL;
		downloadLink.onclick = destroyClickedElement;
		downloadLink.style.display = "none";
		document.body.appendChild(downloadLink);
		downloadLink.click();
		
		alert("다운로드 종료");
		var upbtn = document.getElementById("upbutton");
		upbtn.disabled = false;
	};
}
function destroyClickedElement(event)
{
    document.body.removeChild(event.target);
}


/**
function stop(){
	alert("중지");
	disconnect();
	var downbtn = document.getElementById("downbutton");
	var upbtn = document.getElementById("upbutton");
	downbtn.disabled = false;
	upbtn.disabled = false;
}
&nbsp; &nbsp; &nbsp; &nbsp;
<input type="button" value="중지" onclick="stop()" id="stopbutton">
*/