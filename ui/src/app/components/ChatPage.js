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
  const [errorMessages, setErrorMessages] = useState({});
  const [chatroom_list, set_chatroom_list] = useState([]);
  const [received_reply, set_received_reply] = useState(false);

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
    fetch('http://127.0.0.1:8060/getChatroom/?sessionid=' + sessionid)
      .then((response) => response.json())
      .then((data) => {
        set_chatroom_list(data.chatrooms);
        set_selected_chatroom(data.chatrooms[0][0])
        set_received_reply(true);
      });
  }, []);

  useEffect(() => {
    if (selected_chatroom === null) {
      return;
    }

    fetch('http://127.0.0.1:8060/retrieveMessages/?chatroomID=' + selected_chatroom)
      .then((response) => response.json())
      .then((data) => {
        const m = JSON.parse(data.result).map((elem) => {
          const [student_id, chatroom_id, content, datetime] = elem;
          return ({
            text: content,
            name: student_id,
            datetime: Date.parse(datetime),
            chatroom: chatroom_id,
            socketID: socket.id,
            acked: true
          })
        });
        setMessages(m);
      });
}, [socket, selected_chatroom]
)
;

useEffect(() => {
  socket.on("messageResponse", data => {
    setMessages([...messages, data]);
    fetch("http://127.0.0.1:8060/saveMessage/?sessionid=" + sessionid + "&chatroomID=" + data.chatroom +
      "&message_sent=" + data.text, {method: "PUT"});
  })
}, [socket, messages])

useEffect(() => {
  socket.on("typingResponse", data => setTypingStatus(data))
}, [socket])

useEffect(() => {
  // 👇️ scroll to bottom every time messages change
  lastMessageRef.current?.scrollIntoView({behavior: 'smooth'});
}, [messages]);


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