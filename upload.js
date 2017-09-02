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
	uploadFile(fileSelected);
	
	var btn = document.getElementById("downbutton");
	btn.disabled = "disabled";
}
function download(){
	alert("다운로드 시작");
	downloadFile(fileSelected);
	
	var btn = document.getElementById("upbutton");
	btn.disabled = "disabled";
}
function stop(){
	alert("중지");
	
	var downbtn = document.getElementById("downbutton");
	var upbtn = document.getElementById("upbutton");
	downbtn.disabled = false;
	upbtn.disabled = false;
}

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

function send(file) {
	var file = document.getElementById('uploadfiles').files[0];
    var reader = new FileReader();
    var rawData = new ArrayBuffer();            

    reader.loadend = function() {
    }
    reader.onload = function(e) {
        rawData = e.target.result;
        ws.send(rawData);
        alert("파일 전송이 완료 되었습니다.")
        ws.send('end');
    }

    reader.readAsArrayBuffer(file);
	//var byteArray = new Uint8Array(file);
	//socket.send(byteArray.buffer);
}
function handleReceive(message) {
	// 受信したRAWデータをcanvasに
	var buffer = new Uint8Array(message.data);
	file.putImageData(imageData, 0, 0);
}



/**
function showFileInfo(file){
    alert("name : " + file.name);
    alert("size : " + file.size);
    alert("type : " + file.type);
    alert("date : " + file.lastModified);
}

<script>
  var wSocket = new WebSocket("ws:yourdomain/demo");
  
  wSocket.onmessage = function(e){  alert(e.data);  }  

  wSocket.onopen = function(e){ alert("서버 연결 완료"); } 
  wSocket.onclose = function(e){ alert("서버 연결 종료"); }  

  function send(){ //서버로 데이터를 전송하는 메서드
    wSocket.send("Hello");
  }
</script>*/