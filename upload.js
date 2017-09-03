var fileSelected = null;
var socket = null;
(function () {
	var uploadfiles = document.querySelector('#uploadfiles');
	uploadfiles.addEventListener('change', function () {
		fileSelected = this.files[0];
	}, false);
}());

function upload(){
	alert("업로드 시작");
	
	Uploader('ws://localhost:8082', fileSelected)
	
	var btn = document.getElementById("downbutton");
	btn.disabled = "disabled";
}
function download(){
	alert("다운로드 시작");
	
	Downloader('ws://localhost:8082')
	
	var btn = document.getElementById("upbutton");
	btn.disabled = "disabled";
}
function stop(){
	alert("중지");
	disconnect();
	var downbtn = document.getElementById("downbutton");
	var upbtn = document.getElementById("upbutton");
	downbtn.disabled = false;
	upbtn.disabled = false;
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
	var file = new File("recv.png");
	socket = new WebSocket(url);
	socket.binaryType = 'arraybuffer';
	
	socket.onopen = function() {
		socket.send("recive");
	}
	socket.onmessage = function(ms){
		if(ms.data=="ok"){
			alert("Receiving...");
		}
		else{
			file.open("wb");
			while(true){
				file.write(ms.data)
			}
			/**for(var i = 0; i < fs.slices; ++i) {
				socket.send(fs.getNextSlice());
			}*/
		}
	}
	socket.onclose = function() {
		file.close();
		alert("다운로드 종료");
		var upbtn = document.getElementById("upbutton");
		upbtn.disabled = false;
	};
}

function handleReceive(message) {
	// 受信したRAWデータをcanvasに
	var buffer = new Uint8Array(message.data);
	file.putImageData(imageData, 0, 0);
}


/**
function uploadFile(file){
	alert("1");
	socket = new WebSocket('ws://localhost:8082');
	socket.binaryType = 'arraybuffer';
	socket.onopen = function() {
		send(file);
	}
}
function downloadFile(file){
	socket = new WebSocket('ws://localhost:8082');
	socket.binaryType = 'arraybuffer';
	socket.onmessage = handleReceive;
}


function showFileInfo(file){
	alert("name : " + file.name);
	alert("size : " + file.size);
	alert("type : " + file.type);
	alert("date : " + file.lastModified);
}

<script>
  var wSocket = new WebSocket("ws:yourdomain/demo");
  
  wSocket.onmessage = function(e){	alert(e.data);	}  

  wSocket.onopen = function(e){ alert("서버 연결 완료"); } 
  wSocket.onclose = function(e){ alert("서버 연결 종료"); }  

  function send(){ //서버로 데이터를 전송하는 메서드
	wSocket.send("Hello");
  }
</script>*/