using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    //when there are multiple players, randomize a player to be the judge (DO THIS LATER)

    //maybe delete CardDatabase code?????
    public List<PromptCard> promptCards = new List<PromptCard>();
    public PromptCard currentPrompt;

    PromptCard pickRandomPrompt()
    {
        int prompt_num = Random.Range(0, promptCards.Count);
        PromptCard prompt = promptCards[prompt_num];
        promptCards.Remove(prompt);
        return prompt;
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
