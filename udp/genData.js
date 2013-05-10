var fs = require('fs');
var dgram = require('dgram');


var message = new Buffer(654);
var client = dgram.createSocket("udp4");

stdin = process.openStdin();
stdin.setEncoding("utf-8");

var fpBin = fs.openSync('test.bin', 'r');

var start = new Date();
tid = setInterval(function () {
  fs.read(fpBin, message, 0, 654, null, function (err, bytesRead, buffer) {
    //fs.read(fd, buffer, offset, length, position, callback)
    //position 为 0 则是从文件当前位置读取，因此实现了顺序读取文件内容的结果
    if (err == null) {
      sendUDPData();
    }else{
      clearInterval(tid);
      var stop = new Date()
      console.log('finished data sending , cost time : ' + ( stop - start ) + 'ms');
    }
  });
}, 200);
function sendUDPData() {
  client.send(message, 0, message.length, 31500, "localhost");
}



