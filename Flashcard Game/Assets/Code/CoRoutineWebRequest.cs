using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class CoRoutineWebRequest : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        print("a");
        SendRequest("http://127.0.0.1:8060/getFlashcards/?chatroom_id=7");

        
        print("A");
    }
   
    IEnumerator SendRequest(string url) {
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();
        
        if (request.result == UnityWebRequest.Result.ConnectionError)
        {
            Debug.LogError(string.Format("Error: {0}", request.error));
        }
        else
        {
            Debug.Log("req: " + request.downloadHandler.text);
            Debug.Log(request);
        }
    }
}
