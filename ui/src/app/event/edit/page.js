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
import ReactLeafletSearch from "react-leaflet-search";

function EditEvent() {
  const [errorMessages, setErrorMessages] = useState({});
  const [received_reply, set_received_reply] = useState(false);
  const [profile_info, set_profile_info] = useState({
    student_id: '',
    uni_id: '',
    email: '',
    graduation_year: '',
    major: '',
    hobbies: '',
    interests: '',
    fname: '',
    lname: ''
  });

  let data, email_fetched, returned_values;
  const [start_datetime, set_start] = useState(new Date());
  const [end_datetime, set_end] = useState(new Date());

  const sessionid = getCookie('sessionid');
  if (sessionid === null) {
    return (
      <html>
      <body>
      <p>Hey! You are not logged in. You will be redirected to the login page.</p>
      {window.location.replace('/login')}
      </body>
      </html>
    )
  }

  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-700">{errorMessages.message}</div>
    );

  function getCookie(name) {
    function escape(s) {
      return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1');
    }

    const match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
    return match ? match[1] : null;
  }

  const handleSubmit = (event) => {
    // Prevent page reload
    event.preventDefault();
    let {student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname} = profile_info
    const new_fname = document.forms[0][0]._valueTracker.getValue();
    const new_lname = document.forms[0][1]._valueTracker.getValue();
    let new_email = document.forms[0][6]._valueTracker.getValue();
    const new_hobbies = document.forms[0][7]._valueTracker.getValue();
    const new_interests = document.forms[0][8]._valueTracker.getValue();
    const current_pw = document.forms[0][9]._valueTracker.getValue();
    const new_pw = document.forms[0][10]._valueTracker.getValue();
    fname = new_fname === '' ? fname : new_fname;
    lname = new_lname === '' ? lname : new_lname;
    new_email = new_email === '' ? email : new_email;
    hobbies = new_hobbies === '' ? hobbies : new_hobbies;
    interests = new_interests === '' ? interests : new_interests;

    set_profile_info({student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname});

    // update user profile
    const postProfileData = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:8060/editProfile/?sessionid=' + sessionid + '&hobbies=' +
          encodeURIComponent(hobbies) + '&interests=' + encodeURIComponent(interests) + '&fname=' +
          encodeURIComponent(fname) + '&lname=' + encodeURIComponent(lname) + '&new_email=' +
          encodeURIComponent(new_email), {method: "PUT"}
        );
        data = await response.json();
      } catch (error) {
        setErrorMessages({name: "server", message: "Server Error: " + error})
      }
    }
    const changePassword = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:8060/changePassword/?sessionid=' + sessionid + '&current_pw=' +
          encodeURIComponent(current_pw) + '&new_pw=' + encodeURIComponent(new_pw), {method: "PUT"}
        );
        data = await response.json();
      } catch (error) {
        setErrorMessages({name: "server", message: "Server Error: " + error})
      }
      if (!data.result) {
        setErrorMessages({name: "password", message: "Incorrect password."})
      }
    }

    postProfileData().then(() => {
      if (current_pw && new_pw) {
        if (current_pw === new_pw) {
          setErrorMessages({name: "password", message: "Current password and new password is the same."})
          return;
        }
        changePassword().then(() => {
          if (data.result) {
            window.location.replace('/profile')
          }
        })
      } else {
        window.location.replace('/profile')
      }
    });

  };

  const handleReset = (event) => {
    // Prevent page reload
    event.preventDefault();
    window.location.replace('/profile');
  }


  const fetchData = async () => {
    if (received_reply) {
      return;
    }
    try {
      const sessionid = getCookie('sessionid');
      if (sessionid === null) {
        window.location.replace('/login');
      }
      const response = await fetch('http://127.0.0.1:8060/getProfile/?sessionid=' + sessionid);
      data = await response.json();

      const email_response = await fetch('http://127.0.0.1:8060/getEmail/?sessionid=' + sessionid);
      email_fetched = await email_response.json();
    } catch (error) {
      setErrorMessages({name: "server", message: "Server Error: " + error})
    }
  }

  fetchData().then(() => {
    if (received_reply) {
      return;
    }
    if (data.result.length === 0) {
      data.result.push(['', '', email_fetched.result, '', '', '', '', '', '']);
    }
    const [student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname] = data.result[0];
    set_profile_info({student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname});
    set_received_reply(true);
  })

  const {
    register,
    handleSubmit1,
    watch,
    formState: {errors},
  } = useForm({
    values: returned_values,
  });


  // load when api reply received and variables populated
  return (received_reply && (
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
                <div>

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