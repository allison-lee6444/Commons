import React, {useContext, useEffect, useRef, useState} from 'react'
import {useNavigate} from "react-router-dom"
import {SelectedChatroomContext, ChatroomListContext} from "@/app/components/ChatContext";
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {getCookie} from "@/app/utils";

const ChatBody = ({messages, typingStatus, lastMessageRef}) => {
  const navigate = useNavigate()
  const [id, _, name, curr_is_invitable] = useContext(SelectedChatroomContext);
  const invite_button = useRef(null);
  const invite_email = useRef(null);
  const [show_popup, set_show_popup] = useState(false);
  const [errorMessages, setErrorMessages] = useState({});
  const [submit_success, set_submit_success] = useState(false);
  const [success_invitation_id, set_success_invitation_id] = useState('');
  const sessionid = getCookie('sessionid');

  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-700">{errorMessages.message}</div>
    );
  useEffect(() => {
    invite_button.current.disabled = !curr_is_invitable;
    invite_button.current.title = curr_is_invitable ? "Invite someone to this chatroom!" :
      "You cannot invite other people to this chatroom because this is a course chatroom. Only the system may add " +
      "students to this chatroom."
  }, [curr_is_invitable]);

  const handleLeaveChat = () => {
    localStorage.removeItem("userName")
    navigate("/")
    window.location.reload()
  }

  const handleSubmitEmail = (event) => {
    event.preventDefault();
    fetch('http://127.0.0.1:8060/generateInvite?session_id=' + sessionid + '&target_user_email='
      + invite_email.current.value + '&chatroom_id=' + id,
      {method: 'POST'})
      .then((response) => response.json())
      .then((data) => {
        if (data.detail === 'Database Error') {
          setErrorMessages({name: 'server', message: 'Invalid email'});
          return;
        }
        set_submit_success(true);
        set_success_invitation_id(data.result)
      })
      .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}));
  }

  return (
    <>
      <header className='chat__mainHeader'>
        <p className="curr-chatroom-name">{name}</p>

        <button
          className="invite_button"
          ref={invite_button}
          onClick={() => set_show_popup(true)}
        >
          Invite to Chatroom
        </button>

        <Popup open={show_popup}
               closeOnDocumentClick
               onClose={() => {
                 set_show_popup(false);
                 set_submit_success(false);
               }}
               position="right center"
        >
          <div className="col text-center">
            <label className="input_email_label">Input the email of the person you want to invite.</label>
            <form onSubmit={handleSubmitEmail}>
              <input className="form-control" type="email" disabled={submit_success} ref={invite_email}/>
              {renderErrorMessage('server')}
              <br/>
              {submit_success ?
                <label className="input_email_label">
                  Success! The invitation code is {success_invitation_id}. Send this code to your friend so they can accept your invitation!
                  You may close the window now.
                </label> :
                (<div>
                  <button className="btn btn-primary" type="submit">Submit</button>
                  <button className="btn btn-default" type="reset" onClick={() => set_show_popup(false)}>
                    Cancel
                  </button>
                </div>)
              }
            </form>

          </div>
        </Popup>

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
              <p>{message.name + ', ' + new Date(message.datetime).toLocaleString()}</p>
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