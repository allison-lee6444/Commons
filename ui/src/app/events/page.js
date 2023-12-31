"use client"
// credit: https://richreact.com/react-examples/profile-with-data-and-skills#code-editor1
import React, {useState, useEffect} from 'react';
import './event.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import EventTable from "./events_table";
import {getCookie} from "@/app/utils"

function Events() {
  const [received_reply, set_received_reply] = useState(false);
  const [errorMessages, setErrorMessages] = useState({});
  const [events, set_events] = useState([]);

  const [data, set_data] = useState([]);

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
    fetch('http://127.0.0.1:8060/getEvents/?sessionid=' + sessionid,
      {method: 'GET'})
      .then((response) => response.json())
      .then((r_data) => {
        console.log(JSON.parse(r_data.result))
        const events = JSON.parse(r_data.result);
        const transform_events = events.map((elem) => {
          const [event_id, chatroom_id, event_name, fname, lname, email, descript, location_name, start_time, end_time]
            = elem;
          return ({
            event_id: event_id,
            chatroom_id: chatroom_id,
            event_name: event_name,
            host_name: fname + ' ' + lname,
            host_email: email,
            loc_name: location_name,
            start_time: new Date(start_time).toLocaleString(),
            end_time: new Date(end_time).toLocaleString(),
            description: descript,
            details: (
              <button
                className="btn btn-default"
                onClick={() => window.location.replace('/event/' + event_id)}
              >
                Details
              </button>
            )
          });
        });
        set_data(transform_events);
      });
  }, []);

  // load when api reply received and variables populated
  return (
    <div>
      <div className="container">
        <div className="main-body">
          <nav aria-label="breadcrumb" className="main-breadcrumb">
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/chat">Chatroom</a></li>
              <li className="breadcrumb-item active" aria-current="page">Events</li>
            </ol>
          </nav>
          <EventTable rows={data}/>
        </div>

      </div>
    </div>
  );
}

export default Events;