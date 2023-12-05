import React, {useEffect, useState, useRef, createContext} from 'react'
import ChatBar from './ChatBar'
import ChatBody from './ChatBody'
import ChatFooter from './ChatFooter'
import {ChatroomListContext, SelectedChatroomContext} from "./ChatContext";
import {getCookie} from "@/app/utils";

const ChatPage = ({socket}) => {
  const [messages, setMessages] = useState([])
  const [typingStatus, setTypingStatus] = useState("")
  const lastMessageRef = useRef(null);
  const [selected_chatroom, set_selected_chatroom] = useState(null);
  const [received_reply, set_received_reply] = useState(false);
  const [errorMessages, setErrorMessages] = useState({});
  const [chatroom_list, set_chatroom_list] = useState([])

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

  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-700">{errorMessages.message}</div>
    );

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

  const fetchData = async () => {
    if (received_reply) {
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:8060/getChatroom/?sessionid=' + sessionid);
      chatroom_data = await response.json();
      setErrorMessages({name: 'server', message: 'test'})
    } catch (error) {
      setErrorMessages({name: "server", message: "Server Error: " + error})
    }
  }

  fetchData().then(() => {
    if (received_reply) {
      return;
    }
    chatroom_data = {
      'chatrooms': [[1, "CS-UY 1234"], [2, "CS-UY 9999"], [3, "CS Club"]
      ]
    } // temp fixture

    set_chatroom_list(chatroom_data.chatrooms);
    set_selected_chatroom(chatroom_data.chatrooms[0][0])
    set_received_reply(true);
  })

  return (received_reply &&
    <div className="chat">
      <SelectedChatroomContext.Provider value={[selected_chatroom, set_selected_chatroom]}>
        <ChatroomListContext.Provider value={chatroom_list}>
          <ChatBar socket={socket}/>

          <div className='chat__main'>
            <ChatBody messages={messages} typingStatus={typingStatus} lastMessageRef={lastMessageRef}/>
            <ChatFooter socket={socket}/>
          </div>
        </ChatroomListContext.Provider>

      </SelectedChatroomContext.Provider>
    </div>
  )
}

export default ChatPage