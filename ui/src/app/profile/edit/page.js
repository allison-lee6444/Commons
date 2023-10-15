/* credit: https://richreact.com/react-examples/Edit-profile-page#code-editor1 */
"use client"
import React, {useState} from 'react';
import './EditProfile.css';
import 'bootstrap/dist/css/bootstrap.min.css';
// including name, student ID, graduation year, major, hobbies, and interests.

function EditProfile() {
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-700">{errorMessages.message}</div>
    );

  const errors = {
    email: "Input email has already been used by an account. Please log in.",
    password: "Password error"
  };

  const handleSubmit = (event) => {
    // Prevent page reload
    event.preventDefault();
    const first_name = document.forms[0][0];
    const last_name = document.forms[0][1];
    const email = document.forms[0][6];
    const hobbies = document.forms[0][7];
    const interests = document.forms[0][8];
    const current_pw = document.forms[0][9];
    const new_pw = document.forms[0][10];


    // prints the input
    console.log(first_name._valueTracker.getValue());
    console.log(last_name._valueTracker.getValue());
    console.log(email._valueTracker.getValue());
    console.log(hobbies._valueTracker.getValue());
    console.log(interests._valueTracker.getValue());
    console.log(current_pw._valueTracker.getValue());
    console.log(new_pw._valueTracker.getValue());

    // Find user profile info

    // update user info
    window.location.replace('/profile');

  };

  const handleReset = (event) => {
    // Prevent page reload
    event.preventDefault();
    window.location.replace('/profile');
  }

  // status of api call, should set to false initially, but set as true for demo purposes
  const [received_reply, set_received_reply] = useState(true);

  // call api here
  // populate user info variables here

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
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">User info</h4>
              </div>
              <div className="panel-body">
                <div className="form-group">
                  <label className="col-sm-2 control-label">First name</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control"/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Last name</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control"/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">School</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={"get_school"} disabled/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Student ID</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={"get_id"} disabled/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Graduation year</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={"get_grad_yr"} disabled/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Major</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={"Major"} disabled/>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">E-mail address</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" value={"get_email"} disabled={false}/>
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
                    <textarea rows="3" className="form-control"></textarea>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Interests</label>
                  <div className="col-sm-10">
                    <textarea rows="3" className="form-control"></textarea>
                  </div>
                </div>
              </div>
            </div>

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
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  ));
}

export default EditProfile;