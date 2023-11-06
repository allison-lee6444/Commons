'use client'

import "react-chat-elements/dist/main.css"
import {useState} from "react"; // needed because window would be undefined otherwise

export default function Home() {
  // remove sessionid cookies whenever user goes back to home page
  document.cookie = 'sessionid' +'=; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  window.location.replace('/login');
}



