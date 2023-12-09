/* credit: https://richreact.com/react-examples/Edit-profile-page#code-editor1 */
"use client"
import React, {useEffect, useState} from 'react';
import './eventedit.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {useForm} from "react-hook-form"
import DateTimePicker from "react-datetime-picker";
import 'react-datetime-picker/dist/DateTimePicker.css';
import 'react-calendar/dist/Calendar.css';
import 'react-clock/dist/Clock.css';
import {
  setDefaults,
  fromAddress,
} from "react-geocode";
import {getCookie} from "@/app/utils";

function CreateEvent({params}) {
  const chatroom_id = params.chatroom_id;
  const API_KEY = process.env.NEXT_PUBLIC_API_KEY;
  const [errorMessages, setErrorMessages] = useState({});
  const [[latitude, longitude], set_coords] = useState([40.694067025800905, -73.98662336197091]);
  const [event_info, set_event_info] = useState({
    event_name: '',
    loc_name: '',
    description: ''
  });

  const [start_datetime, set_start] = useState(new Date());
  const [end_datetime, set_end] = useState(new Date());

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

  const handleSubmit = (event) => {
    // Prevent page reload
    event.preventDefault();
    const new_event = {
      event_name: getFieldState('event_name').isDirty ? getValues('event_name') : event_info.event_name,
      loc_name: getFieldState('loc_name').isDirty ? getValues('loc_name') : event_info.loc_name,
      description: getFieldState('description').isDirty ? getValues('description') : event_info.description
    };
    set_event_info(new_event);
    // 999999999 meaning do not exclude any events
    fetch('http://127.0.0.1:8060/hasConflict/?sessionid=' + sessionid + '&startTime=' +
      start_datetime + '&endTime=' + end_datetime + '&event_id=' + 999999999, {method: "GET"})
      .then((response) => response.json())
      .then((data) => {
          const has_conflict = data.result;
          let continuing = true;
          if (has_conflict) {
            continuing = confirm("We have detected a conflict between this event to at least one of your classes or events. Do you" +
              "wish to continue?")
          }
          if (continuing)
            postEventData();
        }
      )
      .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}));

    const postEventData = () => {
      fetch('http://127.0.0.1:8060/createEvent/?sessionid=' + sessionid + '&chatroomID=' +
        chatroom_id + '&eventName=' + encodeURIComponent(new_event.event_name) + '&description=' +
        encodeURIComponent(new_event.description) + '&locName=' + encodeURIComponent(new_event.loc_name) +
        '&locCoord=' + latitude + ',' + longitude + '&startTime=' +
        start_datetime + '&endTime=' + end_datetime, {method: "POST"})
        .then((response) => response.json())
        .then((data1) => {
          if (data1) {
            window.location.replace('/event/' + data1.result);
          }
        })
        .catch((error) => setErrorMessages({name: "server", message: "Server Error: " + error}));
    }
  }

  const handleReset = (event) => {
    // Prevent page reload
    event.preventDefault();
    window.location.replace('/event/' + params.event_id);
  }

  const {
    register,
    getValues,
    getFieldState
  } = useForm();

  setDefaults({
    key: API_KEY, // Your API key here.
    language: "en", // Default language for responses.
    region: "us", // Default region for responses.
  });

  function onClickAddress() {
    let address = getValues('address')
    if (address === '') {
      return;
    }

    fromAddress(address)
      .then(({results}) => {
        const {lat, lng} = results[0].geometry.location;
        set_coords([lat, lng]);
        setErrorMessages({name: "map", message: ""})
      })
      .catch((error) => {
        setErrorMessages({name: "map", message: "Try again! Map Error: " + error})
      })
  }


// load when api reply received and variables populated
// return (received_reply && (
  return ((
    <div className="container bootstrap snippets bootdeys">
      <div className="row">
        <div className="col-xs-12 col-sm-9">
          <hr/>
          <hr/>
          <form className="form-horizontal" onSubmit={handleSubmit} onReset={handleReset}>
            {renderErrorMessage('server')}
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Basic information</h4>
              </div>
              <div className="panel-body">
                <div className="form-group">
                  <label htmlFor="name" className="col-sm-2 control-label">Event Name</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      {...register("event_name", {required: true})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="start" className="col-sm-2 control-label">Start</label>
                  <div className="col-sm-10">
                    <DateTimePicker onChange={set_start} value={start_datetime}/>
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="end" className="col-sm-2 control-label">End</label>
                  <div className="col-sm-10">
                    <DateTimePicker onChange={set_end} value={end_datetime}/>
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="loc_name" className="col-sm-2 control-label">Location Name / Room</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      {...register("loc_name", {required: true})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="location" className="col-sm-2 control-label">Location</label>
                  <div className="col-sm-8">
                    <input
                      className="form-control"
                      placeholder="Input address here"
                      {...register('address')}
                    />
                    <button className="btn btn-default" type="button" onClick={onClickAddress}>Enter</button>
                    {renderErrorMessage("map")}
                    <iframe
                      width="600"
                      height="450"
                      loading="lazy"
                      allowFullScreen
                      referrerPolicy="no-referrer-when-downgrade"
                      src={"https://www.google.com/maps/embed/v1/place?key=" + API_KEY + "&q=" + latitude + "," + longitude}>
                    </iframe>
                  </div>

                </div>
              </div>
            </div>

            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Description</h4>
              </div>
              <div className="panel-body">
                <div className="form-group">
                  <label htmlFor="description" className="col-sm-2 control-label">Event description</label>
                  <div className="col-sm-10">
                    <textarea
                      className="form-control"
                      {...register("description")}
                    />
                  </div>
                </div>

              </div>
            </div>


            <div className="form-group">
              <div className="col-sm-10 col-sm-offset-5">
                <button type="submit" className="btn btn-primary">Submit</button>
                <button type="reset" className="btn btn-default">Cancel</button>
              </div>
            </div>
            {renderErrorMessage("server")}
            {renderErrorMessage("password")}
          </form>
        </div>
      </div>
    </div>
  ));
}

export default CreateEvent;
