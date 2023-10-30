using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CardDatabase : MonoBehaviour
{
    public static List<Card> Cards = new List<Card>();

    private void Awake()
    {
        Cards.Add(new Card(0, "None"));
    }
}
