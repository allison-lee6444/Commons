using CommonsCardGame.Core;
using Riptide;
using Riptide.Utils;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkManager : Singleton<NetworkManager>
{
    protected override void Awake()
    {
        base.Awake();
        RiptideLogger.Initialize(Debug.Log, Debug.Log, Debug.LogWarning, Debug.LogError, true);
    }

    public Server Server;
    [SerializeField] private ushort port = 3000;
    [SerializeField] private ushort maxPlayers = 10;

    private void Start()
    {
        Server = new Server();
        Server.Start(port, maxPlayers);
    }

    private void FixedUpdate()
    {
        Server.Update();
    }
}
