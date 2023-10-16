'use client'

import "react-chat-elements/dist/main.css"
import {useState} from "react"; // needed because window would be undefined otherwise

export default function Home() {
  window.location.replace('/login');
}



