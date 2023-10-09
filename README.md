# Commons
CS4523 Design Project

You need to run the following to get the dependency working:

    pip install psycopg2-binary
    pip install TurboGears2

Note: In the future, we could move to a wheel to handle the dependency if we 
eventually have too many dependecies to manage

For UI, assuming a Linux environment:

    sudo apt install npm
    npm install -g n
    sudo n lts
    reboot