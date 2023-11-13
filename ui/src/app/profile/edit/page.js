/* credit: https://richreact.com/react-examples/Edit-profile-page#code-editor1 */
"use client"
import React, {useState, useEffect} from 'react';
import './EditProfile.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {useForm} from "react-hook-form"
import {getCookie} from "@/app/utils"
import { Dawning_of_a_New_Day } from 'next/font/google';

function EditProfile() {
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

  const handleSubmit = async (event) => {
    // Prevent page reload
    event.preventDefault();

    let old_email = profile_info.email;

    const new_profile = {
      student_id: getValues('student_id'),
      uni_id: getValues('uni_id'),
      email: getValues('email') === '' ? old_email : getValues('email'),
      graduation_year: getValues('graduation_year'),
      major: getValues('major'),
      hobbies: getValues('hobbies'),
      interests: getValues('interests'),
      fname: getValues('fname'),
      lname: getValues('lname')
    };
    set_profile_info(profile_info);
    const current_pw = getValues('curr_pw');
    const new_pw = getValues('new_pw');

    // update user profile
    const postProfileData = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:8060/editProfile/?sessionid=' + sessionid + '&hobbies=' +
          encodeURIComponent(new_profile.hobbies) + '&interests=' + encodeURIComponent(new_profile.interests) + '&fname=' +
          encodeURIComponent(new_profile.fname) + '&lname=' + encodeURIComponent(new_profile.lname) + '&new_email=' +
          encodeURIComponent(new_profile.email), {method: "PUT"}
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

    await postProfileData();
    if (current_pw && new_pw) {
      if (current_pw === new_pw) {
        setErrorMessages({name: "password", message: "Current password and new password is the same."})
        return;
      }
      await changePassword();
      if (data.result) {
        window.location.replace('/profile')
      }

    } else {
      window.location.replace('/profile')
    }

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

  const {
    register,
    getValues
  } = useForm({
    values: returned_values,
  });


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
                  <label htmlFor="fname" className="col-sm-2 control-label">First Name</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      defaultValue={profile_info.fname}
                      required={true}
                      {...register("fname", {required: true})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="lname" className="col-sm-2 control-label">Last Name</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      defaultValue={profile_info.lname}
                      required={true}
                      {...register("lname")}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="uni_id" className="col-sm-2 control-label">School</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      defaultValue={profile_info.uni_id}
                      {...register("uni_id", {disabled: true})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="student_id" className="col-sm-2 control-label">Student ID</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      defaultValue={profile_info.student_id}
                      {...register("student_id", {disabled: true})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="graduation_year" className="col-sm-2 control-label">Graduation Year</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      defaultValue={profile_info.graduation_year}
                      {...register("graduation_year", {disabled: true})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="major" className="col-sm-2 control-label">Major</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      defaultValue={profile_info.major}
                      {...register("major", {disabled: true})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="email" className="col-sm-2 control-label">Email</label>
                  <div className="col-sm-10">
                    <input
                      type="email"
                      className="form-control"
                      defaultValue={profile_info.email}
                      required={true}
                      {...register("email")}
                    />
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
                  <label htmlFor="hobbies" className="col-sm-2 control-label">Hobbies</label>
                  <div className="col-sm-10">
                    <textarea
                      className="form-control"
                      defaultValue={profile_info.hobbies}
                      {...register("hobbies")}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="interests" className="col-sm-2 control-label">Interests</label>
                  <div className="col-sm-10">
                    <textarea
                      className="form-control"
                      defaultValue={profile_info.interests}
                      {...register("interests")}
                    />
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
                  <label htmlFor="curr_pw" className="col-sm-2 control-label">Current Password</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      type="password"
                      {...register("curr_pw")}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="new_pw" className="col-sm-2 control-label">New Password</label>
                  <div className="col-sm-10">
                    <input
                      className="form-control"
                      type="password"
                      {...register("new_pw")}
                    />
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