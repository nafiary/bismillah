var amqp = require('amqp'),
    express = require('express'),
    app = express(),
    server = require('http').createServer(app);
    io = require('socket.io')(server),
    rabbitMq = amqp.createConnection({ host: 'rabbitmq-host.com' });

    // var app = require('express')();
    // var server = require('http').createServer(app);
    // var io = require('socket.io')(server);
    // var amqp = require('amqplib');

server.configure(function () {
   server.use(express.static(__dirname + '/public'));
   server.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
});

rabbitMq.on('ready', function () {
   io.sockets.on('connection', function (socket) {
      var queue = rabbitMq.queue('my-queue');

      queue.bind('#'); // all messages

      queue.subscribe(function (message) {
         socket.emit('message-name', message);
      });
   });
});

app.listen(8080);
