'use client'

import "react-chat-elements/dist/main.css"
import { ChatList } from "react-chat-elements";

export default function Home() {
  return (
<ChatList
  className='chat-list'
  dataSource={[
    {
      avatar: 'https://avatars.githubusercontent.com/u/80540635?v=4',
      alt: 'kursat_avatar',
      title: 'Kursat',
      subtitle: "Why don't we go to the No Way Home movie this weekend ?",
      date: new Date(),
      unread: 3,
    }
]} />
  )
}
