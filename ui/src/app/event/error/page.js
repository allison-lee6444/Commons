import React from "react";

const ErrorPage = () => {
  return (
    <>
      <p>
        You are unauthorized to see the page you requested because you are not a member of the chatroom that this
        event is associated to.
      </p>
      <a href="/chat">Click me to return to chatroom</a>
    </>
  )
}

export default ErrorPage;
