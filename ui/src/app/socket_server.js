const express = require("express")
const app = express()
const cors = require("cors")
const http = require('http').Server(app);
const PORT = 4000
const socketIO = require('socket.io')(http, {
    cors: {
        origin: "http://localhost:3000"
    }
});

app.use(cors())
let users = []

function get(item) {
		const request = new Promise((resolve, reject) => {
			let data = localStorage.getItem(item);
      console.log(`Start of promise`);
			(data) ? resolve(data) : reject();
		});

		request.then((data) => {
      console.log(`promise resolved`);
			console.log(JSON.parse(data));
		});

		request.catch((error) => {
      console.log(`Promise rejected`);
			console.log(error);
		});
	}


socketIO.on('connection', (socket) => {
    console.log(`⚡: ${socket.id} user just connected!`);

    const user_name = ""

    if (typeof window !== 'undefined') {
      user_name = get("userName");
      console.log(user_name)
      return user_name
    }

    if(!users.includes(user_name)){
      socketIO.emit("newUser", user_name);
      console.log("nw user", users)
    }

    socket.on("message", data => {
      socketIO.emit("messageResponse", data)
    })

    socket.on("typing", data => (
      socket.broadcast.emit("typingResponse", data)
    ))

    socket.on("newUser", data => {
      console.log("push data")
      users.push(data)
      socketIO.emit("newUserResponse", users)
    })
 
    socket.on('disconnect', () => {
      console.log('🔥: A user disconnected');
      users = users.filter(user => user.socketID !== socket.id)
      socketIO.emit("newUserResponse", users)
      socket.disconnect()
    });
});

app.get("/api", (req, res) => {
  res.json({message: "Hello"})
});

   
http.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});