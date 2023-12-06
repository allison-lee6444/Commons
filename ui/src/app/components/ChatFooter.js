import React, {useContext, useState} from 'react'
import {SelectedChatroomContext} from "@/app/components/ChatContext";

const ChatFooter = ({socket}) => {
    const [message, setMessage] = useState("")
    const handleTyping = () => socket.emit("typing",`${localStorage.getItem("userName")} is typing`)
    const [selected_chatroom, _] = useContext(SelectedChatroomContext)
    const handleSendMessage = (e) => {
        e.preventDefault()
        if(message.trim() && localStorage.getItem("userName")) {
        socket.emit("message",
            {
            text: message, 
            name: localStorage.getItem("userName"),
            datetime: new Date(),
            chatroom: selected_chatroom,
            socketID: socket.id,
            acked: false
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
            onKeyDown={handleTyping}
            />
            <button className="sendBtn">SEND</button>
        </form>
     </div>
  )
}

export default ChatFooter