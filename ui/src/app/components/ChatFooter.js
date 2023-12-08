import React, {useContext, useState} from 'react'
import {NameContext, SelectedChatroomContext} from "@/app/components/ChatContext";

const ChatFooter = ({socket}) => {
  const [message, setMessage] = useState("");
  const [selected_chatroom, a, b, c] = useContext(SelectedChatroomContext);
  const my_name = useContext(NameContext);

  const handleSendMessage = (e) => {
    e.preventDefault()
    if (message.trim() && localStorage.getItem("userName")) {
      socket.emit("message",
        {
          text: message,
          name: my_name,
          username: localStorage.getItem("userName"),
          datetime: new Date(),
          chatroom: selected_chatroom,
          socketID: socket.id,
          id: `${socket.id}${Math.random()}`
        }
      )
    }
    setMessage("")
  }
  return (
    <div className='chat__footer'>
      <form className='form' onSubmit={handleSendMessage}>
        <input
          type="text"
          placeholder='Write message'
          className='message'
          value={message}
          onChange={e => setMessage(e.target.value)}
        />
        <button className="sendBtn">SEND</button>
      </form>
    </div>
  )
}

export default ChatFooter