import React, {useState, useEffect, useContext} from 'react'
import {SelectedChatroomContext, ChatroomListContext} from "./ChatContext";

const ChatBar = ({socket}) => {
  const [users, setUsers] = useState([])
  const [selected_chatroom, set_selected_chatroom] = useContext(SelectedChatroomContext);
  const chatroom_list = useContext(ChatroomListContext);


  useEffect(() => {
    socket.on("newUserResponse", data => setUsers(data))
  }, [socket, users])


  return (
    <div className='chat__sidebar'>
      <h2 className="commons-logo">Commons</h2>
      <div>
        <h4 className='chat__header'>CHATROOMS</h4>
        <div className='chat__users'>
          {chatroom_list.map(t => <div>
            <button className={t[0] === selected_chatroom ? 'chat__selectedentry' : 'chat__entry'}
                    id={t[0]}
                    onClick={() => {
                      set_selected_chatroom(t[0])
                    }}> {t[1]}</button>
          </div>)}
        </div>
      </div>
    </div>
  )
}

export default ChatBar