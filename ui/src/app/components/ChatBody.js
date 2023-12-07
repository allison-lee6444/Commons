import React, {useContext, useEffect, useState} from 'react'
import {useNavigate} from "react-router-dom"
import {SelectedChatroomContext, ChatroomListContext} from "@/app/components/ChatContext";

const ChatBody = ({messages, typingStatus, lastMessageRef}) => {
  const navigate = useNavigate()
  const [selected_chatroom, a, name] = useContext(SelectedChatroomContext);
  const chatroom_list = useContext(ChatroomListContext);

  const handleLeaveChat = () => {
    localStorage.removeItem("userName")
    navigate("/")
    window.location.reload()
  }


  return (
    <>
      <header className='chat__mainHeader'>
        <p className="curr-chatroom-name">{name}</p>
        <button className='leaveChat__btn' onClick={handleLeaveChat}>LOGOUT</button>
      </header>


      <div className='message__container'>
        {messages.map(message => (
          message.username === localStorage.getItem("userName") ? (
            <div className="message__chats" key={message.id}>
              <p className='sender__name'>{'You, ' + new Date(message.datetime).toLocaleString()}</p>
              <div className='message__sender'>
                <p>{message.text}</p>
              </div>
            </div>
          ) : (
            <div className="message__chats" key={message.id}>
              <p>{message.name+ ', ' + new Date(message.datetime).toLocaleString()}</p>
              <div className='message__recipient'>
                <p>{message.text}</p>
              </div>
            </div>
          )
        ))}

        <div className='message__status'>
          <p>{typingStatus}</p>
        </div>
        <div ref={lastMessageRef}/>
      </div>
    </>
  )
}

export default ChatBody