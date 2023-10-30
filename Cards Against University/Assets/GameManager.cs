using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    //when there are multiple players, randomize a player to be the judge (DO THIS LATER)

    //maybe delete CardDatabase code?????
    public static List<PromptCard> promptCards = new List<PromptCard>();
    public static PromptCard currentPrompt;
    [SerializeField] List<Player> players = new List<Player>();
    public static List<ResponseCard> responseCards = new List<ResponseCard>();
    PromptCard pickRandomPrompt()
    {
        int prompt_num = Random.Range(0, promptCards.Count);
        PromptCard prompt = promptCards[prompt_num];
        promptCards.Remove(prompt);

        //DELETE LATER
        //print(prompt.text);


        return prompt;
    }

    //run during start
    void giveCardsToPlayers()
    {
        foreach (Player player in players)
        {
            List<ResponseCard> selection = new List<ResponseCard>();
            for (int i = 0; i < 6; i++)
            {
                int randIdx = Random.Range(0, responseCards.Count);
                selection.Add(responseCards[randIdx]);
                responseCards.Remove(responseCards[randIdx]);
            }
            player.BuildDeck(selection);
        }
    }

    void buildCardSelections()
    {
        
        promptCards.Add(new PromptCard(0, "This university would be nothing without ______"));
        promptCards.Add(new PromptCard(1, "The best part of university life is ________"));
        promptCards.Add(new PromptCard(2, "The worst part of university life is _________"));
        promptCards.Add(new PromptCard(3, "I could not survive university without _______"));
        promptCards.Add(new PromptCard(4, "The best breakfast meal at the dining hall is ______"));
        promptCards.Add(new PromptCard(5, "If I could change my major to something else, it would be _______"));
        promptCards.Add(new PromptCard(6, "Forget coffee, what truly wakes me up every morning is __________"));
        promptCards.Add(new PromptCard(7, "A new major in ________ has been announced"));
        promptCards.Add(new PromptCard(8, "A new course called __________ has been announced"));
        promptCards.Add(new PromptCard(9, "A common experience among all university students is _______"));
        promptCards.Add(new PromptCard(10, "University is not what it seems. Wait until you find out about ______"));
        promptCards.Add(new PromptCard(11, "_______ has forever altered my brain chemistry"));

        responseCards.Add(new ResponseCard(0, "modern fashion"));
        responseCards.Add(new ResponseCard(1, "8:00 AM classes"));
        responseCards.Add(new ResponseCard(2, "this course"));
        responseCards.Add(new ResponseCard(3, "online classes"));
        responseCards.Add(new ResponseCard(4, "this university's printers"));
        responseCards.Add(new ResponseCard(5, "this university's library"));
        responseCards.Add(new ResponseCard(6, "energy drinks"));
        responseCards.Add(new ResponseCard(7, "the dining hall food"));
        responseCards.Add(new ResponseCard(8, "mint flavored gum"));
        responseCards.Add(new ResponseCard(9, "this university's secret passageway"));
        responseCards.Add(new ResponseCard(10, "mobile games"));
        responseCards.Add(new ResponseCard(11, "my least favorite course"));
        

    }

    // Start is called before the first frame update
    void Start()
    {
        buildCardSelections();
        giveCardsToPlayers();
        pickRandomPrompt();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
