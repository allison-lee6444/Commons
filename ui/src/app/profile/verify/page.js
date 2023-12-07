"use client"
import React, {useState} from 'react';
import './Verify.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {getCookie} from "@/app/utils";
import {useForm} from "react-hook-form";
import Countdown from 'react-countdown';

function Verify() {
  const [errorMessages, setErrorMessages] = useState({});
  const [received_data, set_received_data] = useState(false);
  const [disable_btn, set_disable_btn] = useState(true);
  const [cd_time, set_cd_time] = useState(Date.now);
  const sessionid = getCookie('sessionid');
  let verification_status, verification_response;
  const CountdownWrapper = () => <Countdown date={cd_time + 120 * 1000} renderer={countdown_renderer}/>;
  const MemoCountdown = React.memo(CountdownWrapper);

  if (sessionid === null) {
    return (
      <div>
        <p>Hey! You are not logged in. You will be redirected to the login page.</p>
        {window.location.replace('/login')}
      </div>
    )
  }

  const fetch_data = async () => {
    if (received_data) {
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:8060/getVerificationStatus/?sessionid=' + sessionid);
      verification_status = await response.json();

    } catch (error) {
      setErrorMessages({name: "verify", message: "Server Error: " + error})
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const verifyUser = async () => {
      const token = getValues('token');
      try {
        // Replace with real endpoint later.
        const response = await fetch('http://127.0.0.1:8060/checkVerificationCode/?sessionid='
          + sessionid + '&token=' + token, {method: "GET"});
        verification_response = await response.json();
      } catch (error) {
        setErrorMessages({name: 'verify', message: 'Server error: ' + error})
      }
    }
    verifyUser().then(() => {
      if (verification_response.result) {
        window.location.replace('/profile/edit');
      } else {
        console.log('wrong')
        setErrorMessages({name: "verify", message: "Something went wrong. Try re-entering the verification code."})
      }
    })
  }

  const handleReset = (event) => {
    event.preventDefault();
    window.location.replace('/profile/edit');
  }

  const handleResend = async () => {
    try {
      set_disable_btn(true);
      set_cd_time(Date.now);

      const response = await fetch('http://127.0.0.1:8060/verifyIdentity/?sessionid=' + sessionid, {method: "POST"});
      let data = await response.json();
    } catch (error) {
      setErrorMessages({name: 'verify', message: 'Server error: ' + error})
    }
  }

  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-700">{errorMessages.message}</div>
    );

  const {
    register,
    getValues
  } = useForm();

  fetch_data().then(async () => {
    if (received_data) {
      return;
    }
    if (verification_status.verified) {
      return (
        <div>
          <p>Hey! You are verified. You will be redirected to the profile edit page.</p>
          {window.location.replace('/profile/edit')}
        </div>
      )
    }
    set_received_data(true);
    await handleResend();
  });

  const countdown_renderer = ({minutes, seconds, completed}) => {
    if (seconds < 10) {
      seconds = '0' + seconds
    }
    if (completed) {
      set_disable_btn(false);
      return <text>{minutes}:{seconds}</text>;
    } else {
      return <text>{minutes}:{seconds}</text>;
    }
  };
  return (received_data &&
    <div className="container bootstrap snippets bootdeys">
      <div className="row">
        <div id="centerPage" className="col-xs-12 col-sm-9">
          <form className="form-horizontal" onSubmit={handleSubmit} onReset={handleReset}>
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Verify e-mail</h4>
              </div>
              <div className="panel-body">
                <div className='form-group'>
                  <label className="col-sm-2 control-label">Resend verification code</label>
                  <div className='col-sm-10'>
                    <button type="button" className='btn btn-primary' disabled={disable_btn}
                            onClick={handleResend}>Resend Code
                    </button>
                    <div>
                      <text>Please check your email inbox! You have </text>
                      <MemoCountdown/>
                      <text> until we can resend the code to your email.</text>
                    </div>
                  </div>
                </div>
                <div className="form-group">
                  <label className="col-sm-2 control-label">Verification code</label>
                  <div className="col-sm-10">
                    <input id="code" type="text" className="form-control"
                           required={true}
                           {...register("token")}
                    />
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
          </form>


        </div>
      </div>
    </div>
  );
}

export default Verify;