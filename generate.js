module.exports = {
       /**
        * Before connection (optional, just for faye)
        * @param {client} client connection
        */
       beforeConnect : function(client) {
         // Example:
         // client.setHeader('Authorization', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NsYWltcyI6eyJ1c2VybmFtZSI6InRlc3R1c2VyIiwicm9sZSI6ImFkbWluIiwiZW1haWwiOiJhZmlmQGFmaWYuY29tIiwibmFtZSI6ImFmaWYifSwianRpIjoiYjRiMzJiYjctZjgyZi00YzkxLTk4NzMtNjVkYTJlYThkZGYwIiwiZXhwIjoxNTI4MTM3ODA4LCJmcmVzaCI6ZmFsc2UsImlhdCI6MTUyODA5NDYwOCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTUyODA5NDYwOCwiaWRlbnRpdHkiOiJmZTIyMTY0OC00NmI0LTRjZjctYTc1NC1kYWJhNTg3Nzk3YmIifQ.0myjJUhnb3Fa71uphqhSZjOP8F_5hca3lPfbFtdxFMs');
         // client.disable('websocket');
       },

       /**
        * On client connection (required)
        * @param {client} client connection
        * @param {done} callback function(err) {}
        */
       onConnect : function(client, done) {
         // Faye client
         // client.subscribe('/channel', function(message) { });

         // Socket.io client
         function uuid4() {
           var uuid = "", i, random;
           for (i = 0; i < 32; i++) {
             random = Math.random() * 16 | 0;

             if (i == 8 || i == 12 || i == 16 || i == 20) {
               uuid += "-"
             }
             uuid += (i == 12 ? 4 : (i == 16 ? (random & 3 | 8) : random)).toString(16);
           }
           return uuid;
         }

         var deviceid = ['3db4a9fc-54a2-4771-bfd2-da7882d6b5c9'];
         client.emit('startRabbit', {'data': deviceid, 'id': uuid4() });

         // Primus client
         // client.write('Sailing the seas of cheese');

         // WAMP session
         // client.subscribe('com.myapp.hello').then(function(args) { });

         done();
       },

       /**
        * Send a message (required)
        * @param {client} client connection
        * @param {done} callback function(err) {}
        */
       sendMessage : function(client, done) {
         // Example:
         // client.emit('test', { hello: 'world' });
         // client.publish('/test', { hello: 'world' });
         // client.call('com.myapp.add2', [2, 3]).then(function (res) { });
         // function uuid4() {
         //   var uuid = "", i, random;
         //   for (i = 0; i < 32; i++) {
         //     random = Math.random() * 16 | 0;
         //
         //     if (i == 8 || i == 12 || i == 16 || i == 20) {
         //       uuid += "-"
         //     }
         //     uuid += (i == 12 ? 4 : (i == 16 ? (random & 3 | 8) : random)).toString(16);
         //   }
         //   return uuid;
         // }
         //
         // var deviceid = ['3db4a9fc-54a2-4771-bfd2-da7882d6b5c9'];
         // client.emit('startRabbit', {'data': deviceid, 'id': uuid4() });
         done();
       },

       /**
        * WAMP connection options
        */
       options : {
         // realm: 'chat'
       }
    };
