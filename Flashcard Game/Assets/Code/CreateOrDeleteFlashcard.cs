using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class CreateOrDeleteFlashcard : MonoBehaviour
{
    [SerializeField] TextMeshProUGUI front_text;
    [SerializeField] TextMeshProUGUI back_text;

    public void CreateNewFlashcard()
    {
        Debug.Log(front_text.text);
        Debug.Log(back_text.text);
    }
}
