"use client"
import React, {useEffect, useState} from 'react';
import './Verify.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function Verify() {
    const [errorMessages, setErrorMessages] = useState({});
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

    const handleSubmit = (event) => {
        event.preventDefault();
        verifyUserClick();
    }

    const handleReset = (event) => {
        event.preventDefault();
        window.location.replace('/profile/edit');
    }

    const handleResend = async() => {
        try {
            // Replace with real endpoint later.
            const response = await fetch('http://127.0.0.1:8060/test/?data=2', {method: "GET"}); 
            let data = await response.json();
            if (data.result) {
                console.log("New verification e-mail sent!");
            }
        } catch (error) {
            console.log(error);
        }
    }

    const handleResendClick = () => {
        handleResend();
    }

    const verifyUser = async() => {
        const code = document.getElementById("code").value;
        try {
            // Replace with real endpoint later.
            const response = await fetch('http://127.0.0.1:8060/test/?data='+code, {method: "GET"});
            let data = await response.json();
            if (data.result) {
                //let email = localStorage.getItem("emailAddr");
                const email_response = await fetch('http://127.0.0.1:8060/getEmail/?sessionid=' + sessionid);
                let email_fetched = await email_response.json();
                let email = email_fetched.result;
                const profile = await fetch('http://127.0.0.1:8060/importStudentProfile/?email='+ email, {method: "GET"});
                let profileData = await profile.json();
                if (profileData.result) { 
                    const schedule = await fetch('http://127.0.0.1:8060/importStudentSchedule/?email=' + email, {method: "GET"});
                    let scheduleData = await schedule.json();
                    if (scheduleData.result) {
                        window.location.replace('/profile/edit');
                    }
                }
            }
            if (!data.result || profileData.result || scheduleData.result) {
                setErrorMessages({name: "verify", message: "Something went wrong. Try re-entering the verification code."})
            }
        } catch (error) {
            console.log(error);
        }
    }

    const verifyUserClick = () => {
        verifyUser();
    }

    const renderErrorMessage = (name) =>
        name === errorMessages.name && (
        <div className="error text-red-700">{errorMessages.message}</div>
    );

    return (
        <div className="container bootstrap snippets bootdeys">
      <div className="row">
        <div className="col-xs-12 col-sm-9">
          <form className="form-horizontal" onSubmit={handleSubmit} onReset={handleReset}>
            {/* My attempt. */}
            <div className="panel panel-default">
                <div className="panel-heading">
                <h4 className="panel-title">Verify e-mail</h4>
                </div>
                <div className="panel-body">
                    <div className='form-group'>
                        <label className="col-sm-2 control-label">Resend verification code</label>
                        <div className='col-sm-10'>
                        <button type="button" className='btn btn-primary' onClick={handleResendClick}>Resend Code</button>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="col-sm-2 control-label">Verification code</label>
                        <div className="col-sm-10">
                        <input id="code" type="text" className="form-control"/>
                        </div>
                    </div>
                    <div className="form-group">
                        <div className="col-sm-10 col-sm-offset-2">
                            <button type="submit" className="btn btn-primary">Submit</button>
                            <button type="reset" className="btn btn-default">Cancel</button>
                        </div>
                    </div>
                    {renderErrorMessage("verify")}
                </div>              
            </div>
            {/* My attempt. */}  
          </form>

          
        </div>
      </div>
    </div>
    );
}

export default Verify;