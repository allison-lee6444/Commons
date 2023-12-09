"use client"
// credit: https://richreact.com/react-examples/profile-with-data-and-skills#code-editor1
import React, {useEffect, useState} from 'react';
import './event.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {getCookie} from "@/app/utils"

function Event({params}) {
  const event_id = params.event_id;
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
    email: '',
  });

  const [start_datetime, set_start] = useState(new Date());
  const [end_datetime, set_end] = useState(new Date());
  const [has_joined, set_has_joined] = useState(false);
  const [user_email, set_user_email] = useState('');

  const sessionid = getCookie('sessionid');
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


  useEffect(() => {
    fetch('http://127.0.0.1:8060/getEvent/?sessionid=' + sessionid + '&eventID=' + event_id)
      .then((response) => response.json())
      .then((data) => {
        if (data.detail === 'Database Error') {
          window.location.replace('/event/error')
        }
        if (data.result.length === 0) {
          window.location.replace('/events');
        }
        const [event_name, fname, lname, email, descript, location_name, location_coordinates, start_time, end_time, joined] =
          JSON.parse(data.result)[0];
        set_event_info(
          {
            event_name: event_name,
            loc_name: location_name,
            description: descript,
            fname: fname,
            lname: lname,
            email: email,
          }
        );
        set_has_joined(joined);
        const [lat, lng] = location_coordinates.split(',')
        set_coords([lat, lng]);
        set_start(new Date(Date.parse(start_time)));
        set_end(new Date(Date.parse(end_time)));
        set_received_reply(true);
      })
      .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}))

  }, []);

  useEffect(() => {
    fetch('http://127.0.0.1:8060/getEmail/?sessionid=' + sessionid)
      .then((response) => response.json())
      .then((data) => {
        set_user_email(data.result);
      })
      .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}));
  }, []);

  const handleJoinEvent = () => {
    fetch('http://127.0.0.1:8060/joinEvent/?sessionid=' + sessionid + '&eventID=' + event_id, {method: 'PUT'})
      .then((response) => response.json())
      .then((data) => {
        if (data.result) {
          set_has_joined(true);
          alert('Success! You have joined the event!');
        } else alert('Failed. Please try again.');
      })
      .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}));
  }

  const handleLeaveEvent = () => {
    fetch('http://127.0.0.1:8060/leaveEvent/?sessionid=' + sessionid + '&eventID=' + event_id, {method: 'PUT'})
      .then((response) => response.json())
      .then((data) => {
        if (data.result) {
          set_has_joined(false);
          alert('Success! You have left the event!');
        } else alert('Failed. Please try again.');
      })
      .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}));
  }

  const handleCancelEvent = () => {
    const reply = confirm("Are you sure you want to cancel this event?");
    if (!reply)
      return;
    fetch('http://127.0.0.1:8060/cancelEvent/?sessionid=' + sessionid + '&eventID=' + event_id, {method: 'DELETE'})
      .then((response) => response.json())
      .then((data) => {
        if (data.result) {
          alert("This event has been canceled.");
          window.location.replace('/chat');
        } else alert('Failed. Please try again.');
      })
      .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}));
  }

  return (
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
          {renderErrorMessage('server')}
          <div className="row gutters-sm">
            <div className="col-md-12">
              <div className="card mb-3">
                <div className="card-body">
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Event Name</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {event_info.event_name}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Start</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {start_datetime.toLocaleString()}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">End</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {end_datetime.toLocaleString()}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Host Email</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {event_info.email}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Host Name</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {event_info.fname + ' ' + event_info.lname}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Location name / Room</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {event_info.loc_name}
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
                      src={"https://www.google.com/maps/embed/v1/place?key=" + API_KEY + "&q=" + latitude + "," + longitude}>
                    </iframe>
                  </div>
                  <hr/>

                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Event Description</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {event_info.description}
                    </div>
                  </div>
                  <hr/>
                  {user_email === event_info.email ?
                    <div className="row">
                      <div className="col-sm-12">
                        <a className="btn btn-info "
                           href={"/event/edit/" + event_id}>Edit</a>
                        <hr/>
                        <button className="btn btn-danger "
                                onClick={handleCancelEvent}>Cancel Event
                        </button>
                      </div>
                    </div>
                    : (has_joined ?
                        <div className="row">
                          <div className="col-sm-12">
                            <button className="btn btn-info " onClick={handleLeaveEvent}
                            >Leave Event
                            </button>
                          </div>
                        </div> :
                        <div className="row">
                          <div className="col-sm-12">
                            <button className="btn btn-info " onClick={handleJoinEvent}
                            >Join Event
                            </button>
                          </div>
                        </div>

                    )}
                </div>
              </div>


            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default Event;
