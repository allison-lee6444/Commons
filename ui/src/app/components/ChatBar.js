import React, {useState, useEffect, useContext, createContext} from 'react'
import {getCookie} from "@/app/utils";
import {SelectedChatroomContext} from "./ChatContext";

const ChatBar = ({socket}, context) => {
  const [users, setUsers] = useState([])
  const [received_reply, set_received_reply] = useState(false);
  const [errorMessages, setErrorMessages] = useState({});
  const [chatroom_list, set_chatroom_list] = useState([]);
  const [selected_chatroom, set_selected_chatroom] = useContext(SelectedChatroomContext);
  let chatroom_data;

  const sessionid = getCookie('sessionid');
  if (sessionid === null) {
    return (
      <div>
        <p>Hey! You are not logged in. You will be redirected to the login page.</p>
        {window.location.replace('/login')}
      </div>
    )
  }

  useEffect(() => {
    socket.on("newUserResponse", data => setUsers(data))
  }, [socket, users])

  const fetchData = async () => {
    if (received_reply) {
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:8060/getChatroom/?sessionid=' + sessionid);
      chatroom_data = await response.json();
    } catch (error) {
      setErrorMessages({name: "server", message: "Server Error: " + error})
    }
  }

  fetchData().then(() => {
    if (received_reply) {
      return;
    }
    chatroom_data = {
      'chatrooms': [[1, "CS-UY 1234"], [2, "CS-UY 9999"]]
    } // temp fixture

    set_chatroom_list(chatroom_data.chatrooms);
    set_received_reply(true);
  })


  return (received_reply &&
    <div className='chat__sidebar'>
      <h2>Commons</h2>
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