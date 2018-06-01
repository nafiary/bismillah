var app = require('express')();
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var amqp = require('amqplib');
var forEach = require('async-foreach').forEach;
// const { execSync } = require('child_process');
var fs = require('fs');

let rabbitMqConnection


retryRmqConnection = () =>{
  if (rabbitMqConnection!==null)console.log('retry connection to rabbitMq')
    rabbitMq = amqp.connect('amqp://guest:guest@localhost:5672').then((conn) => {
    rabbitMqConnection = conn
    console.log('readyrabbit')
    // io.emit('rabbitOn', 'rabbit')
    conn.on('close', function(err){
      setTimeout( function() {
              retryRmqConnection()
          }, 0 );
    })
  }).catch( (err) => {
    rabbitMqConnection = null
    setTimeout( function() {
            retryRmqConnection()
        }, 0 );
  })
}
var rabbitMq = amqp.connect('amqp://guest:guest@localhost:5672').then((conn) => {
  rabbitMqConnection = conn
  conn.on('close', function(err){
    retryRmqConnection()
  })
}).catch((err)=>{
  console.log(err)
  retryRmqConnection()
})

// rabbitMq.on('ready', function())
io.on('connection', function (socket) {
  var consumerChannel;
  var id;
  console.log(socket.id+' connected');

  socket.on('disconnect', function () {
    try {
      consumerChannel.deleteQueue(id).then(() => {
        console.log(socket.id+' disconnected');
        return consumerChannel.close();
      });
    } catch (e) {
      console.log(socket.id+' disconnected');
    }
  });

  socket.on('startRabbit', function(msg){
      console.log('startRabbit : ', msg)
      id = msg['id'];
      try {
        rabbitMqConnection.createChannel().then(function(ch) {
          consumerChannel = ch
          var q;
              function allDone(notAborted, arr) {
                var okok = ch.prefetch(1)
                okok = okok.then(() => {
                  return ch.consume(q, logMessage, {noAck: true})
                  .then(() => {
                    console.log(' [*] Waiting for '+msg['data']+'.');
                  })
                })
              }
              forEach(msg['data'], function (item, index, arr) {
                  var done = this.async()
                  var ok = ch.assertExchange(item, 'fanout', {durable: false});
                  ok = ok.then(function() {
                    return ch.assertQueue(msg['id'], {exclusive: false});
                  });
                  ok = ok.then(function(qok) {
                    return ch.bindQueue(qok.queue, item, '').then(function() {
                      q = qok.queue
                      return qok.queue;
                    });
                  });
                  ok = ok.then(function() {
                    done()
                  })
              }, allDone)

              function logMessage(msg) {
                // function writeDone(notAborted, arr) {
                //   fs.appendFile("/tmp/test", "-----\n", function(err) {
                //       if(err) {
                //           return console.log(err);
                //       }
                //   });
                // }
                // forEach(JSON.parse(msg.content.toString()), function (item, index, arr) {
                //     // console.log(item.sendtime);
                //     var done = this.async()
                //     var cmd = 'python -c "exec(\\"import time\\nprint time.time()\\")"'
                //     let stdout = execSync(cmd.toString());
                //     var ms = (stdout-item.sendtime)*1000
                //     fs.appendFile("/tmp/test", item.oidname+"  "+ms+"\n", function(err) {
                //         if(err) {
                //             return console.log(err);
                //         }
                //         done()
                //     });
                // }, writeDone)
                deviceid = JSON.parse(JSON.parse(msg.content.toString()).msg)[0].deviceid

                // var cmd = 'python -c "exec(\\"import time\\nprint time.time()\\")"'
                // let stdout = execSync(cmd.toString());
                var ms = parseInt(new Date().getTime())-parseInt(JSON.parse(msg.content.toString()).sendtime)*1000
                fs.appendFile("/tmp/test", deviceid+"  "+ms+"\n", function(err) {
                    if(err) {
                        return console.log(err);
                    };
                    fs.appendFile("/tmp/test", "-----\n", function(err) {
                        if(err) {
                            return console.log(err);
                        };
                    });
                });
                // console.log(deviceid);
                console.log("emitting : ", JSON.parse(msg.content.toString()).msg);
                console.log(socket.id)
                socket.emit('consume',  JSON.parse(msg.content.toString()).msg)
              }
          }).catch(console.warn);
      }
      catch(err){
        console.log(err)
      }
    })


});

server.listen(8000, function(){
  console.log('listening on *:8000');
});
