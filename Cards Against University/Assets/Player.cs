using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    public List<ResponseCard> deck = new List<ResponseCard>();
    public bool isJudge;

    public void BuildDeck(List<ResponseCard> cardSelection)
    {
        List<ResponseCard> card = GameManager.responseCards;
        for (int i = 0; i < cardSelection.Count; i++) 
        {
            deck.Add(cardSelection[i]);
        }
    }


    // Start is called before the first frame update
    void Start()
    {
        /*
        foreach (Card card in deck)
        {
            print(card.text);
        } */
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
