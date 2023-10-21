"use client"

import ChatPage from '../components/ChatPage';
import Link from "next/link";



export default function FirstPost() {
  return (
    <>
      <h1>First Post</h1>
      <h2>
        <Link href="/test">Back to home</Link>
      </h2>
    </>
  );
}





