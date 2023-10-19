// credit: slight modification from https://larainfo.com/blogs/react-with-tailwind-css-sign-up-page-example
"use client"
import Image from "next/image";
import {useState} from "react";
import "./Signup.css";

export default function Signup() {
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-600">{errorMessages.message}</div>
    );

  const input_error = "Input email has already been used by an account. Please log in.";

  const handleSubmit = (event) => {
    let data;
    // Prevent page reload
    event.preventDefault();
    const email = document.forms[0][0]._valueTracker.getValue();
    const password = document.forms[0][1]._valueTracker.getValue();

    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8060/registerNewUser/' + email + '?password=' + password);
        data = await response.json();
      } catch (error) {
        setErrorMessages({name: "server", message: "Server Error: " + error})
      }
    }
    // Find user login info
    // const userData = database.find((user) => user.username === email.value);
    // call some api like the above line

    // Compare user info
    const check_info = () => {
      if (!data.result) {
        setErrorMessages({name: "input", message: input_error});
      } else {
        setIsSubmitted(true);
        document.cookie='email='+email;
        // report to db using api
        window.location.replace('/profile/edit');
      }
    }
    fetchData().then(check_info);
  };


  return (
    <div className="flex flex-col items-center md:flex-row md:h-screen">
      <div className="flex items-center justify-center w-full md:w-1/2">
        <Image src="/nyu.png" alt="Washington Square Park" width={800} height={533}/>
      </div>
      <div className="flex flex-col items-center justify-center w-full md:w-1/4">
        <div className="w-full max-w-md space-y-8">

          <h1 className="text-2xl font-bold text-black">
            Create an account
          </h1>
          <form className="mt -8 space-y-6" onSubmit={handleSubmit}>
            <div className="mb-2">
              <label
                htmlFor="email"
                className="block font-bold text-gray-500"
              >
                Institution Email
              </label>
              <input
                id="email"
                type="email"
                placeholder="Enter your institution email"
                className="w-full px-4 py-3 mt-1 border-gray-300 rounded-md focus:border-indigo-500 focus:ring focus:ring-indigo-200 text-black"
                required
              />
              {renderErrorMessage("input")}
            </div>
            <div className="mb-2">
              <label
                htmlFor="password"
                className="block font-bold text-gray-500"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                placeholder="Enter your password"
                className="w-full px-4 py-3 mt-1 border-gray-300 rounded-md focus:border-indigo-500 focus:ring focus:ring-indigo-200 text-black"
                required
              />
              {renderErrorMessage("server")}
            </div>
            <div className="mt-6">
              <button type="submit"
                      className="w-full px-4 py-3 font-bold text-white bg-indigo-500 rounded-md hover:bg-indigo-600 focus:outline-none focus:shadow-outline-indigo focus:border-indigo-700">
                Sign up
              </button>
            </div>
          </form>
        </div>
        <p className="mt-2 text-sm text-center text-gray-500">
          {" "}
          Already a member?{" "}
          <a href="/login" className="font-medium text-blue-600 hover:underline">
            Sign in
          </a>
        </p>
      </div>
    </div>
  );
}
