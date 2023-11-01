using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class DisplayCard : MonoBehaviour
{
    [SerializeField] TextMeshProUGUI text_display;
    [SerializeField] private Card cardToDisplay;
    // Start is called before the first frame update
    void Start()
    {
        text_display.text = cardToDisplay.text;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
