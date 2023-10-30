using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

//change MonoBehaviour to NetworkBehaviour later!!!
public class Card
{
    public int id;
    public string text;
    //[SerializeField] TMPro.TextMeshProUGUI m_TextMeshPro;

    private void Start()
    {
        //m_TextMeshPro.text = text;
    }

    public Card()
    {

    }

    public Card(int Id, string Text)
    {
        id = Id;
        text = Text;
    }
}
