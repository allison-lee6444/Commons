"use client"
// credit: https://richreact.com/react-examples/profile-with-data-and-skills#code-editor1
import React, {useState} from 'react';
import './Profile.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function Profile() {

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

  let data;

  function getCookie(name) {
    function escape(s) {
      return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1');
    }

    const match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
    return match ? match[1] : null;
  }

    const fetchData = async () => {
    if(received_reply){return;}
    try {
      const email = getCookie('email');
      const response = await fetch('http://127.0.0.1:3000/getStudentProfileData/' + email);
      data = await response.json();
    } catch (error) {
      setErrorMessages({name: "server", message: "Server Error: " + error})
    }
  }

  fetchData().then(() => {
    if(received_reply){return;}
    if (data.length===0) {
      data.push(['','',getCookie('email'),'','','','','','']);
    }
    const [student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname] = data[0];
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
              <li className="breadcrumb-item"><a href="/chatroom">Chatrooms</a></li>
              <li className="breadcrumb-item active" aria-current="page">User Profile</li>
            </ol>
          </nav>


          <div className="row gutters-sm">
            <div className="col-md-4 mb-3">
              <div className="card">
                <div className="card-body">
                  <div className="d-flex flex-column align-items-center text-center">
                    <img src="/default_avatar.png" alt="User avatar" className="rounded-circle center"
                         width="150"/>
                    <div className="mt-3">
                      <h4>{profile_info.fname+' '+profile_info.lname}</h4>
                    </div>
                  </div>
                </div>
              </div>

            </div>
            <div className="col-md-8">
              <div className="card mb-3">
                <div className="card-body">
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Full Name</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {profile_info.fname+' '+profile_info.lname}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Email</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {profile_info.email}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Student ID</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {profile_info.student_id}
                    </div>
                  </div>
                  <hr />
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">School</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {profile_info.uni_id}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Major</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {profile_info.major}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Graduation Year</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {profile_info.graduation_year}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Hobbies</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {profile_info.hobbies}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Interests</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      {profile_info.interests}
                    </div>
                  </div>
                  <hr/>
                  <div className="row">
                    <div className="col-sm-12">
                      <a className="btn btn-info "
                         href="/profile/edit">Edit</a>
                    </div>
                  </div>
                </div>
              </div>


            </div>
          </div>

        </div>
      </div>
    </div>
  ));
}

export default Profile;