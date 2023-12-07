import React, {useState, useEffect, useContext, useRef} from 'react'
import {SelectedChatroomContext, ChatroomListContext} from "./ChatContext";
import 'bootstrap/dist/css/bootstrap.min.css';
import {getCookie} from "@/app/utils";

const ChatBar = ({socket}) => {
  const [users, setUsers] = useState([])
  const [selected_chatroom, set_selected_chatroom, a] = useContext(SelectedChatroomContext);
  const [chatroom_list, set_chatroom_list] = useContext(ChatroomListContext);
  const [adding_chatroom, set_adding_chatroom] = useState(false);
  const chatroom_name = useRef(null);


  useEffect(() => {
    socket.on("newUserResponse", data => setUsers(data))
  }, [socket, users])

  const sessionid = getCookie('sessionid');

  const handleSubmitAddChatroom = (event) => {
    event.preventDefault();
    const name = chatroom_name.current.value;
    fetch('http://127.0.0.1:8060/createChatroom/?sessionid=' + sessionid + '&chatroom_name=' + name,
      {method: 'PUT'})
      .then((response) => response.json())
      .then((data) => {
        set_chatroom_list([...chatroom_list, [data.result, name]]);
        set_selected_chatroom(data.result);
      });
    set_adding_chatroom(false);
  }

  return (
    <div className='chat__sidebar'>
      <h2 className="commons-logo">Commons</h2>
      <div>
        <h4 className='chat__header'>MENU</h4>
        <button type='button' className='menu_button' onClick={() => window.location.replace('/events')}>
          Your Events
        </button>
        <button type='button' className='menu_button' onClick={() => window.location.replace('/profile')}>
          Profile
        </button>
        <button type='button' className='menu_button' onClick={() => set_adding_chatroom(true)}>
          Add Chatroom
        </button>
      </div>
      <div>
        <h4 className='chat__header'>CHATROOMS</h4>
        <div className='chat__users'>
          {adding_chatroom ?
            (<div>
              <form>
                <input ref={chatroom_name} type="text" className='chat__entry' placeholder='Name of new chatroom'/>
              </form>
              <br/>
              <div className="col text-center">
                <button className="btn btn-primary" onClick={handleSubmitAddChatroom}>Submit</button>
                <button className="btn btn-default" onClick={() => set_adding_chatroom(false)}>
                  Cancel
                </button>
              </div>
            </div>) : null}
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