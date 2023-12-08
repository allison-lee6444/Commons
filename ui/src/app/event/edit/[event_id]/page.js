/* credit: https://richreact.com/react-examples/Edit-profile-page#code-editor1 */
"use client"
import React, {useState} from 'react';
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

function EditEvent({ params }) {
  const event_id = params.event_id;
  console.log(event_id);

  const API_KEY = process.env.NEXT_PUBLIC_API_KEY;
  const [errorMessages, setErrorMessages] = useState({});
  const [received_reply, set_received_reply] = useState(false);
  const [[latitude, longitude], set_coords] = useState([40.694067025800905, -73.98662336197091]);
  const [event_info, set_event_info] = useState({
    event_name: '',
    loc_name: '',
    description: ''
  });

  let data, returned_values, has_conflict;
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

  const handleSubmit = (event) => {
    // Prevent page reload

    event.preventDefault();
    const new_event = {
      event_name: getValues('event_name'),
      loc_name: getValues('loc_name'),
      description: getValues('description')
    };
    set_event_info(new_event);

    // update event

    const find_conflict = async () => {
      try {
        const conflict_response = await fetch(
          'http://127.0.0.1:8060/hasConflict/?sessionid=' + sessionid + '&startTime=' +
          encodeURIComponent(start_datetime) + '&endTime=' + encodeURIComponent(end_datetime), {method: "GET"}
        );
        has_conflict = await conflict_response.json();
      } catch (error) {
        setErrorMessages({name: "server", message: "Server Error: " + error})
      }
    }
    const postEventData = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:8060/editEvent/?sessionid=' + sessionid + '&chatroomID=' +
          encodeURIComponent(chatroomid) + '&eventName=' + encodeURIComponent(new_event.name) + '&description=' +
          encodeURIComponent(new_event.description) + '&locName=' + encodeURIComponent(new_event.loc_name) +
          '&locCoord=' + encodeURIComponent(latitude + ',' + longitude) + '&startTime=' +
          encodeURIComponent(start_datetime) + '&endTime=' + encodeURIComponent(end_datetime), {method: "PUT"}
        );
        data = await response.json();
      } catch (error) {
        setErrorMessages({name: "server", message: "Server Error: " + error})
      }
    }

    find_conflict().then(() => {
      let continuing = true;
      if (has_conflict.result) {
        continuing = confirm("We have detected a conflict between this event to at least one of your classes or events. Do you" +
          "wish to continue?") // TODO: when editing event, cannot show conflict within itself
        if (!continuing){
          return;
        }
      }
      // postEventData().then(() => {
      //   console.log('post');
      //   return;
      //   window.location.replace('/event')
      // });
    })

  };

  const handleReset = (event) => {
    // Prevent page reload
    event.preventDefault();
    console.log('reset');
    return;
    window.location.replace('/event');
  }


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
  //   set_event_info({event_name: event_name, loc_name: location_name, description: descript});
  //   const [lat, lng]=location_coordinates.split(',')
  //   set_coords([lat,lng]);
  //   set_start(new Date(Date.parse(start_time)));
  //   set_end(new Date(Date.parse(end_time)));
  //   set_received_reply(true);
  // })

  const {
    register,
    getValues,
  } = useForm({
    values: returned_values,
  });

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

    // comment to prevent api usage, costs $$$. just enable this when we demo or sth
    // everything works here
    //
    // fromAddress(address)
    //   .then(({results}) => {
    //     const {lat, lng} = results[0].geometry.location;
    //     set_coords([lat, lng]);
    //     setErrorMessages({name: "map", message: ""})
    //   })
    //   .catch((error) => {
    //     setErrorMessages({name: "map", message: "Try again! Map Error: " + error})
    //   })
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
                      defaultValue={'event_name'}
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
                      defaultValue={'loc_name'}
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
                      defaultValue={"description"}
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

export default EditEvent;
