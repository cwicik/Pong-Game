# School Project
This project required us to use a socket connection between the server and the client

Main Instructions:
Title screen:
The title screen has three buttons - play offline, play online and exit.

# While not in game you can press the "escape" button to return to the previous screen.

Play offline:
When you click on play offline button a game will start that works like this:
One player (the left player) will move his bat upwards by pressing the "W" key and down with the "S" key.
A second player (the right player) will move his bat upwards by pressing the "↑" key and down with the "↓" key.
You can press the "escape" button to stop the game and another press will resume the game.
Each player must not allow the ball to touch their side of the screen and they will receive one point if they score a goal - meaning the ball will touch the other side of the screen.
When a player reaches five points he will be declared the winner. After 1.5 seconds it will be returned to the main screen.

Play online:
When you click on play online button, a new screen with two buttons will open:
The host game button which will open a server (socket) which listens at 0.0.0.0 at port 1717 and waits until a guest user connects.
Join game button which will open a new screen Let the user be given a typing ip address and when it is finished click on a button (join server) which will try to connect to the server at the given address. In case there is no server at the given address or there was a problem connecting to the server an error message will be displayed and the user will be returned to the main screen.
Once the guest manages to connect to the server the game begins. The rules are the same of an offline game while:
The player who created the game - the server owner (the left player) will move his bat upwards by pressing the "W" key and down with the "S" key.
Player entering the game - The guest (the right player) will move his bat upwards by pressing the "↑" key and down with the "↓" key.
If there is any failure in connection, both players will be returned to the main screen.
