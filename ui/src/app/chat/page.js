"use client"
import './page.css'
import {BrowserRouter, Routes, Route} from "react-router-dom"
import ChatPage from "../components/ChatPage";
import socketIO from "socket.io-client"
import React, {useEffect, useState} from "react";
import {getCookie} from "@/app/utils";


const socket = socketIO.connect("http://localhost:4000")

function chatRoom() {
  const sessionid = getCookie('sessionid');
  const [check_complete, set_check_complete] = useState(false);

  if (sessionid === null) {
    return (
      <html>
      <body>
      <p>Hey! You are not logged in. You will be redirected to the login page.</p>
      {window.location.replace('/login')}
      </body>
      </html>
    )
  }

  useEffect(() => {
    fetch('http://127.0.0.1:8060/getVerificationStatus/?sessionid=' + sessionid)
      .then((response) => response.json())
      .then((data) => {
        if (!data.verified) {
          if (confirm('You are unverified and not allowed to access the chats. Please verify first.')){
            window.location.replace('/profile/verify');
          } else{
            window.location.replace('/login');
          }
        }
        set_check_complete(true);
      });
  }, []);

  return ( check_complete &&
    <BrowserRouter>
      <div>
        <Routes>
          <Route path="/chat" element={<ChatPage socket={socket}/>}></Route>
        </Routes>
      </div>
    </BrowserRouter>

  );
}

export default chatRoom;