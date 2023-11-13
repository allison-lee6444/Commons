/* credit: https://richreact.com/react-examples/Edit-profile-page#code-editor1 */
"use client"
import React, {useEffect, useState} from 'react';
import './EditProfile.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Dawning_of_a_New_Day } from 'next/font/google';

function EditProfile() {
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);
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
    const current_pw = document.forms[0][10]._valueTracker.getValue();
    const new_pw = document.forms[0][11]._valueTracker.getValue();
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

  // My attempt.
  const handleVerify = () => {
    window.location.replace('/profile/verify');
  }

  const getVerificationStatus = async (email) => {
    try {
      const response = await fetch('http://127.0.0.1:8060/getVerificationStatus/?email=' + email);
      data = await response.json();
      if (data.verified) {
        let status = document.getElementById("verification-status");
        status.style.color = "green";
        status.innerHTML = "Verified";
        document.getElementById("reqCodeGroup").style.display = "None";
      }
    } catch (error) {
      
    }
  }
  // My attempt.

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
    getVerificationStatus(email); // My attempt.
    localStorage.setItem('emailAddr',email); // My attempt.
  })


  // load when api reply received and variables populated
  return (received_reply && (
    <div className="container bootstrap snippets bootdeys">
      <div className="row">
        <div className="col-xs-12 col-sm-9">
          <form className="form-horizontal" onSubmit={handleSubmit} onReset={handleReset}>
            <div className="panel panel-default">
              <div className="panel-body text-center">
                <img src="/default_avatar.png" className="img-circle profile-avatar" alt="User avatar"/>
              </div>
            </div>
            {renderErrorMessage('server')}
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">User info</h4>
              </div>
              <div className="panel-body">
                <div className="form-group">
                  <label className="col-sm-2 control-label">First name</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" placeholder={profile_info.fname}/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Last name</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" placeholder={profile_info.lname}/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">School</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={profile_info.uni_id} disabled/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Student ID</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={profile_info.student_id} disabled/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Graduation year</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={profile_info.graduation_year} disabled/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Major</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={profile_info.major} disabled/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Email</label>
                  <div className="col-sm-10">
                    <input type="email" className="form-control" placeholder={profile_info.email} disabled={false}/>
                  </div>
                </div>
              </div>
            </div>

            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">More about myself</h4>
              </div>
              <div className="panel-body">
                <div className="form-group">
                  <label className="col-sm-2 control-label">Hobbies</label>
                  <div className="col-sm-10">
                    <textarea rows="3" className="form-control" placeholder={profile_info.hobbies}></textarea>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Interests</label>
                  <div className="col-sm-10">
                    <textarea rows="3" className="form-control" placeholder={profile_info.interests}></textarea>
                  </div>
                </div>
              </div>
            </div>

            {/* My attempt. */}
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Verify e-mail</h4>
              </div>
              <div className="panel-body">
                <div className='form-group'>
                  <label className="col-sm-2 control-label">Verification status</label>
                  <div className='col-sm-10'>
                    <p id="verification-status">Unverified</p>
                  </div>
                </div>
                <div id='reqCodeGroup' className='form-group'>
                  <label className="col-sm-2 control-label">Request verification code</label>
                  <div className='col-sm-10'>
                    <button type="button" className='btn btn-primary' onClick={handleVerify}>Request Code</button>
                  </div>
                </div>
                {renderErrorMessage("server")}
                {renderErrorMessage("password")}
            </div>   
            {/* My attempt. */}

            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Security</h4>
              </div>
              <div className="panel-body">
                <div className="form-group">
                  <label className="col-sm-2 control-label">Current password</label>
                  <div className="col-sm-10">
                    <input type="password" className="form-control"/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">New password</label>
                  <div className="col-sm-10">
                    <input type="password" className="form-control"/>
                  </div>
                </div>
                <div className="form-group">
                  <div className="col-sm-10 col-sm-offset-2">
                    <button type="submit" className="btn btn-primary">Submit</button>
                    <button type="reset" className="btn btn-default">Cancel</button>
                  </div>
                </div>
                {renderErrorMessage("server")}
                {renderErrorMessage("password")}

              </div>              
            </div>            
          </div>
          </form>
        </div>
      </div>
    </div>
  ));
}

export default EditProfile;