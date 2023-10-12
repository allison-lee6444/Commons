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
After reboot, in the ui/commons directory,
    
    npm install
    npm run dev

A page will open in your browser (should show it is unavailable),
you can refresh it after a while after it finishes compiling. Then, you can add whatever 
changes to the code (currently ui/src/app/page.js) and it will reflect 
in the page automatically.