"use client"
// credit: https://richreact.com/react-examples/profile-with-data-and-skills#code-editor1
import React, {useState} from 'react';
import './event.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function Event() {
  const API_KEY = process.env.NEXT_PUBLIC_API_KEY;
  const [received_reply, set_received_reply] = useState(false);
  const [errorMessages, setErrorMessages] = useState({});
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

  let data, email_fetched;

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

  function getCookie(name) {
    function escape(s) {
      return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1');
    }

    const match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
    return match ? match[1] : null;
  }

  const fetchData = async () => {
    if (received_reply) {
      return;
    }
    try {

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

  // load when api reply received and variables populated
  return (received_reply && (
    <div>
      <div className="container">
        <div className="main-body">


          <nav aria-label="breadcrumb" className="main-breadcrumb">
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/chatroom">Chatroom</a></li>
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
                      src={"https://www.google.com/maps/embed/v1/place?key="+API_KEY+"&q=40.694067025800905,-73.98662336197091"}>
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
                  {profile_info.email==="admin@admin.com"?// test condition
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