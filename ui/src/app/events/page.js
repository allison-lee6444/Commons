"use client"
// credit: https://richreact.com/react-examples/profile-with-data-and-skills#code-editor1
import React, {useState} from 'react';
import './event.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import EventTable, {useEventTable} from "./events_table";
import {getCookie} from "@/app/utils"

function Events() {
  const [received_reply, set_received_reply] = useState(false);
  const [errorMessages, setErrorMessages] = useState({});
  const [events, set_events] = useState([]);

  let data;

  const sessionid = getCookie('sessionid');
  if (sessionid === null) {
    return (
      <div>
        <p>Hey! You are not logged in. You will be redirected to the login page.</p>
        {window.location.replace('/login')}
      </div>
    )
  }

  const fetchData = async () => {
    if (received_reply) {
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:8060/getEvents/?sessionid=' + sessionid);
      data = await response.json();
    } catch (error) {
      setErrorMessages({name: "server", message: "Server Error: " + error})
    }
  }
  //
  // fetchData().then(() => {
  //   if (received_reply) {
  //     return;
  //   }
  //   set_events(data.result);
  //   set_received_reply(true);
  // })

  //test data
  data = [{
    event_id: 1,
    chatroom_id: 1,
    event_name: 'First',
    host_name: 'A BC',
    loc_name: 'loc1',
    start_time: '2023-11-15 12:18:37.138587',
    end_time: '2023-11-15 13:18:37.138587',
    description: 'desc 123'
  },
  {
    event_id: 2,
    chatroom_id: 1,
    event_name: 'Second',
    host_name: 'A BC',
    loc_name: 'loc2',
    start_time: '2023-11-16 21:18:37.138587',
    end_time: '2023-11-17 22:18:37.138587',
    description: 'desc 123'
  }
  ]

  // load when api reply received and variables populated
  // return (received_reply && (
  return ((
    <div>
      <div className="container">
        <div className="main-body">
          <nav aria-label="breadcrumb" className="main-breadcrumb">
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/chatroom">Chatroom</a></li>
              <li className="breadcrumb-item active" aria-current="page">Events</li>
            </ol>
          </nav>
        </div>
        <EventTable rows={data}/>

      </div>
    </div>
  ));
}

export default Events;