"""
Name: Daniel Gladkov
Date: 27/05/2020
"""
import socket
import pygame
import time
from Button import Button
from Player import Player
from Ball import Ball
pygame.font.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
REFRESH_RATE = 60
LEFT = 1

# Initializing Vars
clock = pygame.time.Clock()
screens = []
single_player_game = False
host_play = False
guest_play = False
get_input = False
new_game = True
server_listen = False
action = 'nup'
player_text = ''
font = pygame.font.SysFont('Comic Sans MS', 75)
title_font = pygame.font.SysFont('Comic Sans MS', 100)

# Init screen
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
WINDOW_WIDTH = screen.get_width()
WINDOW_HEIGHT = screen.get_height()
pygame.display.set_caption("Pong")


def left_win():
    """The function announces that the left player has won, resets all game components and goes back to the main menu
    """
    global guest_play
    global host_play
    global single_player_game
    ball.respawn()
    players[0].reset()
    players[1].reset()
    text = title_font.render("Left Player Won!", False, WHITE)
    single_player_game = False
    host_play = False
    guest_play = False
    screen.fill(BLACK)
    screen.blit(text, ((WINDOW_WIDTH - text.get_width()) / 2, 0))
    pygame.display.flip()
    time.sleep(1.5)
    title_screen()


def right_win():
    """The function announces that the right player has won, resets all game components and goes back to the main menu
    """
    global guest_play
    global host_play
    global single_player_game
    ball.respawn()
    players[0].reset()
    players[1].reset()
    text = title_font.render("Right Player Won!", False, WHITE)
    single_player_game = False
    host_play = False
    guest_play = False
    screen.fill(BLACK)
    screen.blit(text, ((WINDOW_WIDTH - text.get_width()) / 2, 0))
    pygame.display.flip()
    time.sleep(1.5)
    title_screen()


def single_player():
    """The function starts a new game of single player
    """
    global single_player_game
    global new_game
    if new_game:
        ball.respawn()
        players[0].reset()
        players[1].reset()
    pygame.mouse.set_visible(False)
    single_player_game = True
    screens.append(paused)
    for button in title_screen_buttons:
        button.deactivate()
    new_game = False


def paused():
    """The function pauses a singe player game
    """
    screens.append(single_player)
    pygame.mouse.set_visible(True)
    global single_player_game
    single_player_game = False
    for button in pause_buttons:
        button.activate()
    for player in players:
        player.stop()


def multi_player_menu():
    """The function opens a menu for multi player game ( join or host )
    """
    screen.fill(BLACK)
    screens.append(title_screen)
    for button in title_screen_buttons:
        button.deactivate()
    for button in multi_player_buttons:
        button.activate()
    pygame.display.flip()


def create_server():
    """A function that creates a server socket
    :return: A server socket that listens to all at port 1717
    :rtype: socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1717))
    return server_socket


def join_server():
    """A function that creates a client socket and tries to connect to a server socket
    ip is from user input at port 1717
    """
    global my_socket
    global action
    global player_text
    global guest_play
    global get_input
    get_input = False
    screen.fill(BLACK)
    screens.append(multi_player_menu)
    pygame.display.flip()
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((player_text, 1717))
        action = 'nup'
        guest_play = True
    except:
        message = font.render('Cant connect to server', False, WHITE)
        screen.blit(message, ((WINDOW_WIDTH - message.get_width()) / 2, 0))
        pygame.display.flip()
        time.sleep(2)
        title_screen()


def host_game():
    """A function that opens a server socket and waits for a client socket to connect
    """
    global client_socket
    global server_socket
    global screens
    global host_play
    for category in buttons:
        for button in category:
            button.deactivate()
    screen.fill(BLACK)
    screens.append(multi_player_menu)
    message = font.render('Waiting for player', False, WHITE)
    screen.blit(message, ((WINDOW_WIDTH - message.get_width()) / 2, 0))
    pygame.display.flip()
    server_socket = create_server()
    server_socket.setblocking(False)
    try:
        # Server listening freezes program until a guest is found
        server_socket.listen(1)
        print('waiting for guest...')
        client_socket, address = server_socket.accept()
        print('found guest!')
        host_play = True
        ball.respawn()
    except:
        message = font.render('An error has accured', False, WHITE)
        screen.blit(message, ((WINDOW_WIDTH - message.get_width()) / 2, 0))
        pygame.display.flip()
        time.sleep(2)
        title_screen()


def join_game():
    """A function that allows to get user input and prints it on the screen
    user input will be used as ip and will try to connect to server
    """
    global screens
    screen.fill(BLACK)
    pygame.display.flip()
    screens.append(multi_player_menu)
    global get_input
    global player_text
    player_text = ''
    get_input = True
    for category in buttons:
        for button in category:
            button.deactivate()
    Join_Server_button.activate()


def title_screen():
    """A function that resets all vars and displays the main menu of the game
    """
    try:
        client_socket.close()
        server_socket.close()
        my_socket.close()
    except:
        pass
    global screens
    for button in pause_buttons:
        button.deactivate()
    screens = []
    pygame.mouse.set_visible(True)
    screen.fill(BLACK)
    pygame.display.flip()
    global new_game
    new_game = True
    game_name = title_font.render('Pong!', False, WHITE)
    screen.blit(game_name, ((WINDOW_WIDTH - game_name.get_width()) / 2, 0))
    for button in title_screen_buttons:
        button.activate()
    pygame.display.flip()


def go_back():
    """A function that goes back to the previous screen, if none found, will exit the game
    """
    if len(screens) != 0:
        global guest_play
        global host_play
        global single_player_game
        global get_input
        single_player_game = False
        guest_play = False
        host_play = False
        get_input = False
        for category in buttons:
            for button in category:
                button.deactivate()
        screens.pop()()
    else:
        exit()


# Creating all components
LH_button = Button(screen, WINDOW_WIDTH / 2 - 120, WINDOW_HEIGHT - 3 * WINDOW_HEIGHT / 4, 'Play Offline', single_player)
OG_button = Button(screen, WINDOW_WIDTH / 2 - 110, WINDOW_HEIGHT - 2 * WINDOW_HEIGHT / 4, 'Play Online', multi_player_menu)
Exit_button = Button(screen, WINDOW_WIDTH / 2 - 40, WINDOW_HEIGHT - WINDOW_HEIGHT / 4, 'Exit', exit)
Host_button = Button(screen, WINDOW_WIDTH / 2 - 120, WINDOW_HEIGHT - 3 * WINDOW_HEIGHT / 4, 'Host game', host_game)
Join_button = Button(screen, WINDOW_WIDTH / 2 - 110, WINDOW_HEIGHT - 2 * WINDOW_HEIGHT / 4, 'Join game', join_game)
multi_player_buttons = (Host_button, Join_button)
title_screen_buttons = (Exit_button, LH_button, OG_button)
Resume_button = Button(screen, WINDOW_WIDTH / 2 - 80, WINDOW_HEIGHT - 3 * WINDOW_HEIGHT / 4, 'Resume', single_player)
MM_button = Button(screen, WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT - 2 * WINDOW_HEIGHT / 4, 'Main Menu', title_screen)
Join_Server_button = Button(screen, WINDOW_WIDTH / 2  - 110, WINDOW_HEIGHT - 2 * WINDOW_HEIGHT / 3, 'Join Server', join_server)
pause_buttons = (Resume_button, MM_button, Exit_button)
buttons = (multi_player_buttons, title_screen_buttons, pause_buttons, (Join_Server_button,))
player_1 = Player(screen, 100, "Left Player", left_win)
player_2 = Player(screen, WINDOW_WIDTH - 100, "Right Player", right_win)
players = (player_1, player_2)
ball = Ball(screen)
screen.fill(BLACK)
pygame.display.flip()


def main():
    global client_socket
    global server_socket
    global get_input
    global player_text
    global action
    title_screen()
    while True:
        if single_player_game:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        go_back()
                    if event.key == pygame.K_w:
                        player_1.up()
                    if event.key == pygame.K_s:
                        player_1.down()
                    if event.key == pygame.K_UP:
                        player_2.up()
                    if event.key == pygame.K_DOWN:
                        player_2.down()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        player_1.stopup()
                    if event.key == pygame.K_s:
                        player_1.stopdown()
                    if event.key == pygame.K_UP:
                        player_2.stopup()
                    if event.key == pygame.K_DOWN:
                        player_2.stopdown()

            screen.fill(BLACK)
            for i in range(WINDOW_HEIGHT // 100 + 1):
                pygame.draw.line(screen, WHITE, (WINDOW_WIDTH / 2, i * 100), (WINDOW_WIDTH / 2, i * 100 + 50), 10)
            for player in players:
                player.move()
                player.draw_self()
            ball.move(players[0], players[1])
            pygame.display.flip()
            for player in players:
                if player.check_win():
                    player.win()

        elif host_play:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player_1.up()
                    if event.key == pygame.K_s:
                        player_1.down()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        player_1.stopup()
                    if event.key == pygame.K_s:
                        player_1.stopdown()

            data = client_socket.recv(3).decode()
            print('data recv:', data)
            if data == 'upp':
                player_2.up()
            elif data == 'dwn':
                player_2.down()
            elif data == 'nup':
                player_2.stopup()
            elif data == 'ndw':
                player_2.stopdown()

            client_socket.send(str.encode(player_1.data()))
            print(player_1.data(), 'sent')
            client_socket.send(str.encode(player_2.data()))
            print(player_2.data(), 'sent')
            client_socket.send(str.encode(ball.data()))
            print(ball.data(), 'sent')

            screen.fill(BLACK)
            for i in range(WINDOW_HEIGHT // 100 + 1):
                pygame.draw.line(screen, WHITE, (WINDOW_WIDTH / 2, i * 100), (WINDOW_WIDTH / 2, i * 100 + 50), 10)
            for player in players:
                player.move()
                player.draw_self()
            ball.move(players[0], players[1])
            pygame.display.flip()
            for player in players:
                if player.check_win():
                    print('winner!')
                    data = client_socket.recv(3).decode()

                    client_socket.send(str.encode(player_1.data()))
                    print(player_1.data(), 'sent')
                    client_socket.send(str.encode(player_2.data()))
                    print(player_2.data(), 'sent')
                    client_socket.send(str.encode(ball.data()))
                    print(ball.data(), 'sent')
                    player.win()

        elif guest_play:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        action = 'upp'
                    if event.key == pygame.K_DOWN:
                        action = 'dwn'
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        action = 'nup'
                    if event.key == pygame.K_DOWN:
                        action = 'ndw'

            if players[0].check_win():
                print('winner!')
                players[0].win()
                continue

            if players[1].check_win():
                print('winner!')
                players[1].win()
                continue

            print('sending', action)
            my_socket.send(str.encode(action))

            player_1_data = my_socket.recv(10).decode()
            print('player 1 data:', player_1_data)
            player_2_data = my_socket.recv(10).decode()
            print('player 2 data:', player_2_data)
            ball_data = my_socket.recv(10).decode()
            print('ball data:', ball_data)

            player_1.move_to(player_1_data)
            player_2.move_to(player_2_data)
            ball.move_to(ball_data)

            screen.fill(BLACK)
            for i in range(WINDOW_HEIGHT // 100 + 1):
                pygame.draw.line(screen, WHITE, (WINDOW_WIDTH / 2, i * 100), (WINDOW_WIDTH / 2, i * 100 + 50), 10)
            for player in players:
                player.draw_self()
            ball.move(players[0], players[1])
            pygame.display.flip()

        else:
            if not get_input:
                for category in buttons:
                    for button in category:
                        button.hovered_over()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        go_back()
                    if get_input:
                        if pygame.key.name(event.key) == 'backspace':
                            player_text = player_text[:-1]
                        if (pygame.key.name(event.key).isdigit() or
                           pygame.key.name(event.key) == '.') and len(player_text) < 15:
                            player_text += pygame.key.name(event.key)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == LEFT:
                        for category in buttons:
                            for button in category:
                                button.pressed()
            if get_input:
                screen.fill(BLACK)
                ip_adress = font.render(player_text, False, WHITE)
                enter_ip = font.render('Enter IP:', False, WHITE)
                screen.blit(enter_ip, ((WINDOW_WIDTH - enter_ip.get_width()) / 2, 0))
                screen.blit(ip_adress, ((WINDOW_WIDTH - ip_adress.get_width()) / 2, 100))
                Join_Server_button.hovered_over()
                pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main()
