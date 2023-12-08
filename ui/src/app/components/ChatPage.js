import React, {useEffect, useState, useRef, createContext} from 'react'
import ChatBar from './ChatBar'
import ChatBody from './ChatBody'
import ChatFooter from './ChatFooter'
import {ChatroomListContext, NameContext, SelectedChatroomContext} from "./ChatContext";
import {getCookie} from "@/app/utils";

const ChatPage = ({socket}) => {
  const [messages, setMessages] = useState([])
  const [typingStatus, setTypingStatus] = useState("")
  const lastMessageRef = useRef(null);
  const [selected_chatroom, set_selected_chatroom] = useState(null);
  const [chatroom_list, set_chatroom_list] = useState([]);
  const [selected_chatroom_name, set_selected_chatroom_name] = useState('');
  const [received_reply, set_received_reply] = useState(false);
  const [my_name, set_my_name] = useState('');
  const [selected_chatroom_invitable, set_selected_chatroom_invitable] = useState(false);

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
    fetch('http://127.0.0.1:8060/getChatroom/?sessionid=' + sessionid)
      .then((response) => response.json())
      .then((data) => {
        set_chatroom_list(data.chatrooms);
        const [id, name, is_club_room] = data.chatrooms[0]; // preselect the first chatroom
        set_selected_chatroom(id);
        set_selected_chatroom_name(name);
        set_selected_chatroom_invitable(is_club_room);
      });
    fetch("http://127.0.0.1:8060/getName/?email=" + localStorage.getItem("userName"))
      .then((response) => response.json())
      .then((fetch_data) => {
        const [fname, lname] = fetch_data
        set_my_name(fname + ' ' + lname);
        set_received_reply(true);
      });
  }, []);

  useEffect(() => {
      if (selected_chatroom === null) {
        return;
      }
      const [id, name, is_club_room] = chatroom_list.find((elem) => elem[0] === selected_chatroom);
      set_selected_chatroom_name(name);
      set_selected_chatroom_invitable(is_club_room);

      fetch('http://127.0.0.1:8060/retrieveMessages/?chatroomID=' + selected_chatroom)
        .then((response) => response.json())
        .then((data) => {
          const m = JSON.parse(data.result).map((elem) => {
            const [student_id, chatroom_id, content, datetime, fname, lname, email] = elem;
            return ({
              text: content,
              username: email,
              name: fname + ' ' + lname,
              datetime: Date.parse(datetime),
              chatroom: chatroom_id,
              socketID: socket.id,
              id: null
            })
          });
          m.sort((a, b) => b.datetime < a.datetime ? 1 : -1)
          setMessages(m);
        });
    }, [socket, selected_chatroom]
  )
  ;

  useEffect(() => {
    socket.on("messageResponse", data => {
      setMessages([...messages, data]);
      if (data.username === localStorage.getItem("userName")) {
        fetch("http://127.0.0.1:8060/saveMessage/?sessionid=" + sessionid + "&chatroomID=" + data.chatroom +
          "&message_sent=" + data.text + '&message_id=' + data.id, {method: "PUT"});
      }
    })
  }, [socket, messages])

  useEffect(() => {
    socket.on("typingResponse", data => setTypingStatus(data))
  }, [socket])

  useEffect(() => {
    // 👇️ scroll to bottom every time messages change
    if (lastMessageRef === null) {
      return;
    }
    lastMessageRef.current?.scrollIntoView({behavior: "instant"});
  }, [messages]);


  return (received_reply &&
    <div className="chat">
      <SelectedChatroomContext.Provider
        value={[selected_chatroom, set_selected_chatroom, selected_chatroom_name, selected_chatroom_invitable]}
      >
        <ChatroomListContext.Provider value={[chatroom_list, set_chatroom_list]}>
          <ChatBar socket={socket}/>
        </ChatroomListContext.Provider>
        <div className='chat__main'>
          <ChatBody messages={messages} typingStatus={typingStatus} lastMessageRef={lastMessageRef}/>
          <NameContext.Provider value={my_name}>
            <ChatFooter socket={socket}/>
          </NameContext.Provider>
        </div>
      </SelectedChatroomContext.Provider>
    </div>
  )
}

export default ChatPage