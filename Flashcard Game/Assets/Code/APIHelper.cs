using UnityEngine;
using System.Net;
using System.IO;
using UnityEngine.Networking;

public static class APIHelper
{
    public static Question CreateNewQuestion()
    {
        UnityWebRequest www = UnityWebRequest.Post("http://localhost:3000/createFlashCard", "", "application/json");

        //placeholder
        return new Question("", "");
    }
}
