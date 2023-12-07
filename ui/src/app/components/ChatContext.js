import {createContext} from "react";

export const SelectedChatroomContext = createContext([null, null, null]);
export const ChatroomListContext = createContext([]);

export const NameContext = createContext('');