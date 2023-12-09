import React, {useState, useEffect, useContext, useRef} from 'react'
import {SelectedChatroomContext, ChatroomListContext} from "./ChatContext";
import 'bootstrap/dist/css/bootstrap.min.css';
import {getCookie} from "@/app/utils";
import Popup from "reactjs-popup";

const ChatBar = ({socket}) => {
  const [users, setUsers] = useState([])
  const [selected_chatroom, set_selected_chatroom, a, b] = useContext(SelectedChatroomContext);
  const [chatroom_list, set_chatroom_list] = useContext(ChatroomListContext);
  const [adding_chatroom, set_adding_chatroom] = useState(false);
  const chatroom_name = useRef(null);
  const [accepting_invite, set_accepting_invite] = useState(false);
  const invite_id = useRef(null);
  const [errorMessages, setErrorMessages] = useState({});


  useEffect(() => {
    socket.on("newUserResponse", data => setUsers(data))
  }, [socket, users])

  const sessionid = getCookie('sessionid');

  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-700">{errorMessages.message}</div>
    );

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

  const handleSubmitAcceptInvite = (event) => {
    event.preventDefault();
    const input_id = invite_id.current.value;
    fetch('http://127.0.0.1:8060/acceptInvite?sessionid=' + sessionid + '&invite_id=' + input_id,
      {method: 'POST'})
      .then((response) => response.json())
      .then((data) => {
        if (data.detail === 'Database Error') {
          setErrorMessages({name: 'server', message: 'Invalid invite ID'});
          return;
        }
        set_chatroom_list([...chatroom_list, data.result]);
        set_selected_chatroom(data.result[0]);
        set_accepting_invite(false);
      })
      .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}));
  }

  return (
    <div className='chat__sidebar'>
      <h2 className="commons-logo">Commons</h2>
      <div>
        <h4 className='chat__header'>MENU</h4>
        <button type='button' className='menu_button' onClick={() => window.location.replace('/events')}>
          My Events
        </button>
        <button type='button' className='menu_button' onClick={() => window.location.replace('/profile')}>
          Profile
        </button>
        <button type='button' className='menu_button' onClick={() => set_adding_chatroom(true)}>
          Add Chatroom
        </button>
        <button type='button' className='menu_button' onClick={() => set_accepting_invite(true)}>
          Accept Invite
        </button>
        <Popup open={accepting_invite}
               closeOnDocumentClick
               onClose={() => set_accepting_invite(false)}
               position="right center"
        >
          <div className="col text-center">
            <label className="input_email_label">Input the invite ID you received.</label>
            <form>
              <input className="form-control" ref={invite_id}/>
            </form>
            {renderErrorMessage('server')}
            <br/>
            <button className="btn btn-primary" onClick={handleSubmitAcceptInvite}>Submit</button>
            <button className="btn btn-default" onClick={() => set_accepting_invite(false)}>
              Cancel
            </button>

          </div>
        </Popup>
      </div>
      <div>
        <h4 className='chat__header'>CHATROOMS</h4>
        <div className='chat__users'>
          {adding_chatroom ?
            (<div>
              <form>
                <input ref={chatroom_name} type="text" className='chat__entry' placeholder='Name of new chatroom'/>
              </form>
              {renderErrorMessage('server')}
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