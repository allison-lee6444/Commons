import React, {useState, useEffect, useContext} from 'react'
import {SelectedChatroomContext, ChatroomListContext} from "./ChatContext";
// My attempt - redirect.
import {useNavigate} from 'react-router-dom';
// My attempt - redirect.

const ChatBar = ({socket}) => {
  const [users, setUsers] = useState([])
  const [selected_chatroom, set_selected_chatroom] = useContext(SelectedChatroomContext);
  const chatroom_list = useContext(ChatroomListContext);

  useEffect(() => {
    socket.on("newUserResponse", data => setUsers(data))
  }, [socket, users])

  // My attempt - redirect.
  const navigate = useNavigate();
  const eventClick = () => {
    navigate('/events');
  }
  const profileClick = () => {
    navigate('/profile');
  }
  // My attempt - redirect.

  return (
    <div className='chat__sidebar'>
      <h2 className="commons-logo">Commons</h2>
      {/* My Attempt */}
      <div>
        <h4 className='chat__header'>MENU</h4>
        <button type="button" className='menu_button' onClick={eventClick}>Events</button>
        <button type="button" className='menu_button'onClick={profileClick}>Profile</button>
      </div>
      {/* My Attempt */}
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