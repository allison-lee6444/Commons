"use client"
// credit: https://richreact.com/react-examples/profile-with-data-and-skills#code-editor1
import React, {useState} from 'react';
import './event.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {getCookie} from "@/app/utils"

function Event({ params }) {
  const event_id = params.event_id;
  console.log(event_id);
  
  const API_KEY = process.env.NEXT_PUBLIC_API_KEY;
  const [errorMessages, setErrorMessages] = useState({});
  const [received_reply, set_received_reply] = useState(false);
  const [[latitude, longitude], set_coords] = useState([40.694067025800905, -73.98662336197091]);
  const [event_info, set_event_info] = useState({
    event_name: '',
    loc_name: '',
    description: '',
    fname: '',
    lname: '',
    email: ''
  });

  let data, returned_values;
  const [start_datetime, set_start] = useState(new Date());
  const [end_datetime, set_end] = useState(new Date());

  const sessionid = getCookie('sessionid');
  const chatroomid = 1; // debug
  const eventid = 1 //debug
  if (sessionid === null) {
    return (
      <div>
        <p>Hey! You are not logged in. You will be redirected to the login page.</p>
        {window.location.replace('/login')}
      </div>
    )
  }

  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-700">{errorMessages.message}</div>
    );

  const fetchData = async () => {
    if (received_reply) {
      return;
    }
    try {
      const chatroom_id = 1; // change after chatroom pushed
      if (sessionid === null) {
        window.location.replace('/login');
      }
      if (chatroom_id === null) {
        window.location.replace('/chat');
      }

      const response = await fetch('http://127.0.0.1:8060/getEvent/?sessionID=' + sessionid + '&eventID=' + eventid + '&chatroomID' + chatroom_id);
      data = await response.json();
    } catch (error) {
      setErrorMessages({name: "server", message: "Server Error: " + error})
    }
  }

  // fetchData().then(() => {
  //   if (received_reply) {
  //     return;
  //   }
  //   if (data.result.length === 0) {
  //     window.location.replace('/events');
  //   }
  //   const [event_name, fname, lname, email, descript, location_name, location_coordinates, start_time, end_time] = data.result[0];
  //   set_event_info(
  //     {event_name: event_name, loc_name: location_name, description: descript, fname: fname, lname: lname, email: email}
  //   );
  //   const [lat, lng]=location_coordinates.split(',')
  //   set_coords([lat,lng]);
  //   set_start(new Date(Date.parse(start_time)));
  //   set_end(new Date(Date.parse(end_time)));
  //   set_received_reply(true);
  // })

  // load when api reply received and variables populated
  // return (received_reply && (
  return ((
    <div>
      <div className="container">
        <div className="main-body">


          <nav aria-label="breadcrumb" className="main-breadcrumb">
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/chat">Chatroom</a></li>
              <li className="breadcrumb-item"><a href="/events">Events</a></li>
              <li className="breadcrumb-item active" aria-current="page">Event</li>
            </ol>
          </nav>


          <div className="row gutters-sm">
            <div className="col-md-12">
              <div className="card mb-3">
                <div className="card-body">
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Event Name</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {"event name"}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Start</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {"start"}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">End</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {"end"}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Host Email</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {"email"}
                    </div>
                  </div>
                  <hr/>
                   <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Host Name</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {"name"}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Location name / Room</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {"loc_name"}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Location</h6>
                    </div>

                    <iframe
                      width="800"
                      height="450"
                      loading="lazy"
                      allowFullScreen
                      referrerPolicy="no-referrer-when-downgrade"
                      src={"https://www.google.com/maps/embed/v1/place?key=" + API_KEY + "&q=40.694067025800905,-73.98662336197091"}>
                    </iframe>
                  </div>
                  <hr/>

                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Event Description</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {"description"}
                    </div>
                  </div>
                  <hr/>
                  {true ?// test condition
                    <div className="row">
                      <div className="col-sm-12">
                        <a className="btn btn-info "
                           href="/event/edit">Edit</a>
                      </div>
                    </div>
                    : <br/>}
                </div>
              </div>


            </div>
          </div>

        </div>
      </div>
    </div>
  ));
}

export default Event;