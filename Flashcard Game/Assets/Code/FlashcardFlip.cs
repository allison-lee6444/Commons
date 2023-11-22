using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;


public class Question
{
    public string question;
    public string correctAnswer;

    public Question(string q, string c)
    {
        question = q;
        correctAnswer = c;
    }
}


public class FlashcardFlip : MonoBehaviour
{
    public RectTransform rect; // hold flashcard object scale, make it look like it's flipping
    public TextMeshProUGUI cardText;

    public Question[] ques = new Question[3];

    public float flipTime = 0.5f; // how much time it takes to get halfway through the flip of the card
    private int faceSide = 0; // 0 for front, 1 for back

    private int isShrinking = -1; // -1 = get smaller, 1 = get bigger, this is an int so that we can multiply by this value

    private bool isFlipping = false;

    private int cardNum = 0;

    private float distancePerTime; // velocity of flipping flashcard

    private float timeCount = 0;

    // Start is called before the first frame update
    void Start()
    {
        ques[0] = new Question("one", "1");
        ques[1] = new Question("two", "2");
        ques[2] = new Question("three", "3");

        distancePerTime = rect.localScale.x / flipTime;
        cardNum = 0;
        cardText.text = ques[cardNum].question;
    }

    // Update is called once per frame
    void Update()
    {
        if (isFlipping)
        {
            Vector3 v = rect.localScale;
            v.x += isShrinking * distancePerTime * Time.deltaTime;
            rect.localScale = v;

            timeCount += Time.deltaTime;
            if ((timeCount >= flipTime) && (isShrinking < 0))
            {
                isShrinking = 1; //make it grow back to og size
                timeCount = 0;
                if (faceSide == 0)
                {
                    faceSide = 1;
                    cardText.text = ques[cardNum].correctAnswer;
                }
                else
                {
                    faceSide = 0;
                    cardText.text = ques[cardNum].question;
                }
            }
            else if ((timeCount >= flipTime) && (isShrinking == 1))
            {
                isFlipping = false;
            }
        }
    }

    public void NextCard()
    {
        faceSide = 0;
        cardNum++;
        if (cardNum > ques.Length)
        {
            cardNum = 0;
        }
        cardText.text = ques[cardNum].question;
    }
    public void FlipCard()
    {
        timeCount = 0;
        isFlipping = true;
        isShrinking = -1;
    }
}

