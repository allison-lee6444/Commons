"use client"
import './page.css'
import {BrowserRouter, Routes, Route} from "react-router-dom"
import ChatPage from "../components/ChatPage";
import socketIO from "socket.io-client"


const socket = socketIO.connect("http://localhost:4000")
function chatRoom() {
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