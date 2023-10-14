// credit: slight modification from https://larainfo.com/blogs/react-with-tailwind-css-sign-up-page-example
"use client"
import Image from "next/image";
import {useState} from "react";

export default function Signup() {
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
    const name = document.forms[0][0];
    const email = document.forms[0][1];
    const password = document.forms[0][2];

    // prints the input name, email, and pw
    console.log(name._valueTracker.getValue());
    console.log(email._valueTracker.getValue());
    console.log(password._valueTracker.getValue());

    // Find user login info
    // const userData = database.find((user) => user.username === email.value);
    // call some api like the above line

    // Compare user info
    // if (!userData) {
    //   if (!userData.password) {
    //     // No password
    //     setErrorMessages({ name: "password", message: errors.password });
    //   } else {
    //     setIsSubmitted(true);
    //     report to db using api
    //     window.location.replace('/profile/creation');
    //   }
    // } else {
    //   // Username not found
    //   setErrorMessages({ name: "email", message: errors.email });
    // }
  };

  return (
    <div className="flex flex-col items-center md:flex-row md:h-screen">
        <div className="flex items-center justify-center w-full md:w-1/2">
          <Image src="/nyu.png" alt="Washington Square Park" width={800} height={533} />
        </div>
        <div className="flex flex-col items-center justify-center w-full md:w-1/4">
          <div className="w-full max-w-md space-y-8">

          <h1 className="text-2xl font-bold">
            Create an account
          </h1>
          <form className="mt -8 space-y-6" onSubmit={handleSubmit}>
            <div className="mb-2">
              <label
                htmlFor="name"
                className="block font-bold text-gray-500"
              >
                Name
              </label>
              <input
                id="email"
                type="text"
                placeholder="Enter your name"
                className="w-full px-4 py-3 mt-1 border-gray-300 rounded-md focus:border-indigo-500 focus:ring focus:ring-indigo-200 text-black"
                required
              />
            </div>
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
              {renderErrorMessage("email")}
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
              {renderErrorMessage("password")}
            </div>
            <div className="mt-6">
              <button type="submit" className="w-full px-4 py-3 font-bold text-white bg-indigo-500 rounded-md hover:bg-indigo-600 focus:outline-none focus:shadow-outline-indigo focus:border-indigo-700">
                Sign up
              </button>
            </div>
          </form>
          </div>
          <p className="mt-2 text-xs text-center text-gray-500">
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
