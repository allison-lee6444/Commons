"use client"

import './page.css'
import Home from '../components/Home';
import ChatPage from '../components/ChatPage';
import Link from "next/link";
import socketIO from 'socket.io-client';


const socket = socketIO.connect('http://localhost:4000');
function chatRoom() {
  return (
      <div>
          <Link href="/login"></Link>
          <ChatPage socket={socket} />
      </div>
  );
}

export default chatRoom;


