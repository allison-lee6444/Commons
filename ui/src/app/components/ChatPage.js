import React, {useEffect, useState, useRef, createContext} from 'react'
import ChatBar from './ChatBar'
import ChatBody from './ChatBody'
import ChatFooter from './ChatFooter'
import {SelectedChatroomContext} from "./ChatContext";

const ChatPage = ({socket}) => {
  const [messages, setMessages] = useState([])
  const [typingStatus, setTypingStatus] = useState("")
  const lastMessageRef = useRef(null);
  const [selected_chatroom, set_selected_chatroom] = useState(null);


  useEffect(() => {
    socket.on("messageResponse", data => setMessages([...messages, data]))
  }, [socket, messages])

  useEffect(() => {
    socket.on("typingResponse", data => setTypingStatus(data))
  }, [socket])

  useEffect(() => {
    // 👇️ scroll to bottom every time messages change
    lastMessageRef.current?.scrollIntoView({behavior: 'smooth'});
  }, [messages]);

  return (
    <div className="chat">
      <SelectedChatroomContext.Provider value={[selected_chatroom, set_selected_chatroom]}>
        <ChatBar socket={socket}/>
      </SelectedChatroomContext.Provider>
      <div className='chat__main'>
        <ChatBody messages={messages} typingStatus={typingStatus} lastMessageRef={lastMessageRef}/>
        <ChatFooter socket={socket}/>
      </div>
    </div>
  )
}

export default ChatPage