"use client"
import './page.css'
import {BrowserRouter, Routes, Route} from "react-router-dom"
import ChatPage from "../components/ChatPage";
import socketIO from "socket.io-client"


const socket = socketIO.connect("http://localhost:4000")
function chatRoom() {
  // My attempt - check if student is verified.
  const sessionid = getCookie('sessionid');
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

  function getCookie(name) {
      function escape(s) {
          return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1');
      }

      const match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
      return match ? match[1] : null;
  }

  const getVerificationStatus = async () => {
    try {
      const email_response = await fetch('http://127.0.0.1:8060/getEmail/?sessionid=' + sessionid);
      let email_fetched = await email_response.json();
      let email = email_fetched.result;
      const response = await fetch('http://127.0.0.1:8060/getVerificationStatus/?email=' + email);
      let data = await response.json();
      if (!data.verified) {
        return (
          <div>
            <p>Hey! You are not verified. You will be redirected to the verification page where you can request a verification code.</p>
            {window.location.replace('/profile/verify')}
          </div>
        )
      }
    } catch (error) {
      
    }
  }

  getVerificationStatus();
  // My attempt - check if student is verified.

  return (
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