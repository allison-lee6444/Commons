"use client"
// credit: https://richreact.com/react-examples/profile-with-data-and-skills#code-editor1
import React, {useEffect, useState} from 'react';
import './event.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import EventTable from "@/app/events/events_table";
import {getCookie} from "@/app/utils"

const ChatroomEvents = ({params}) => {
  const sessionid = getCookie('sessionid');
  const [data, set_data] = useState([]);

  if (sessionid === null) {
    return (
      <div>
        <p>Hey! You are not logged in. You will be redirected to the login page.</p>
        {window.location.replace('/login')}
      </div>
    )
  }

  useEffect(() => {
    fetch('http://127.0.0.1:8060/getChatroomEvents?chatroomID=' + params.chatroom_id,
      {method: 'GET'})
      .then((response) => response.json())
      .then((r_data) => {
        const events = JSON.parse(r_data.events);
        const transform_events = events.map((elem) => {
          const [event_name, fname, lname, email, descript, location_name, location_coordinates, start_time, end_time,
            event_id] = elem;
          return ({
            event_id: event_id,
            chatroom_id: params.chatroom_id,
            event_name: event_name,
            host_name: fname + ' ' + lname,
            host_email: email,
            loc_name: location_name,
            start_time: start_time,
            end_time: end_time,
            description: descript,
            details: (
              <button
                className="btn btn-default"
                onClick={() => window.location.replace('/event/'+event_id)}
              >
                Details
              </button>
            )
          });
        });
        set_data(transform_events);
      });
  }, [params.chatroom_id]);

  return ((
    <div>
      <div className="container">
        <div className="main-body">
          <nav aria-label="breadcrumb" className="main-breadcrumb">
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/chat">Chatroom</a></li>
              <li className="breadcrumb-item active" aria-current="page">Events</li>
            </ol>
          </nav>
        </div>
        <div className="col text-center">
          <button
            className="btn btn-primary"
            onClick={() => window.location.replace('/events/chatroom/' + params.chatroom_id + '/create')}
          >
            Create Event
          </button>
        </div>
        <EventTable rows={data}/>

      </div>
    </div>
  ));
}

export default ChatroomEvents;