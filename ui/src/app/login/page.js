// credit: copied from https://larainfo.com/blogs/nextjs-with-tailwind-login-page-example
"use client"
import Image from "next/image";
import Link from "next/link";
import {useState} from "react";
import "./Login.css"
import { useRouter } from 'next/navigation'



export default function Login() {
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  const router = useRouter()

  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error text-red-600">{errorMessages.message}</div>
    );

  const input_error =  "Email or password is incorrect. Please try again.";

  const handleSubmit = (event) => {
    let data;
    // Prevent page reload
    event.preventDefault();
    const email = document.forms[0][0]._valueTracker.getValue();
    const password = document.forms[0][1]._valueTracker.getValue();

    // Find user login info
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8060/login/?email=' + encodeURIComponent(email) + '&password=' + encodeURIComponent(password));
        data = await response.json();
        localStorage.setItem("userName", email);
      } catch (error) {
        setErrorMessages({name: "server", message: "Server Error: "+error})
      }
    }

    const set_cookie = () => {
      if (data.result) {
        setIsSubmitted(true);
        document.cookie='sessionid='+data.sessionid;
        window.location.replace('/chat');
      } else {
        setErrorMessages({name: "input", message: input_error});
      }
    }

    fetchData().then(set_cookie);

  };


  return (
    <div className="flex flex-col items-center md:flex-row md:h-screen">
      <div className="flex items-center justify-center w-full md:w-1/2">
        <Image src="/nyu.png" alt="Washington Square Park" width={800} height={533}/>
      </div>
      <div className="flex flex-col items-center justify-center w-full md:w-1/4">
        <div className="w-full max-w-md space-y-8">
          <div>
            <h1 className="text-2xl font-bold text-black">Welcome back!</h1>
            <p className="mt-2 text-gray-500">
              Please sign in to your account.
            </p>
          </div>
          <form className="mt -8 space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email" className="block font-bold text-gray-500">
                Email address
              </label>
              <input
                id="email"
                type="email"
                placeholder="Enter your email"
                className="w-full px-4 py-3 mt-1 border-gray-300 rounded-md focus:border-indigo-500 focus:ring focus:ring-indigo-200 text-black"
                required
              />
            </div>
            <div>
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
              {renderErrorMessage("input")}
              {renderErrorMessage("server")}
            </div>
            <div>
              <button
                type="submit"
                className="w-full px-4 py-3 font-bold text-white bg-indigo-500 rounded-md hover:bg-indigo-600 focus:outline-none focus:shadow-outline-indigo focus:border-indigo-700"
              >
                Sign In
              </button>
            </div>
          </form>
        </div>
        <p className="mt-4 text-sm text-center text-gray-500">
          Don&apos;t have an account?{" "}
          <Link
            href="/signup"
            className="font-medium text-blue-600 hover:underline"
          >
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}