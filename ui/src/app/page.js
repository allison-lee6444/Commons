'use client'

import "react-chat-elements/dist/main.css"
import {useState} from "react"; // needed because window would be undefined otherwise

export default function Home() {
  window.location.replace('/login');
}

/* 
const fetchData = async () => {
    try {
      console.log("Testing ...");
      const response = await fetch('http://127.0.0.1:8060/registerNewUser/4?password=12');
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error('The error:',error);
    }
  }

fetchData();
*/
 
