import pygame
import sys
import random

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

# initializing pygame
pygame.init()

# dimensions of the screen
dimensions = (800, 500)
scr = pygame.display.set_mode(dimensions)
pygame.display.set_caption("PONG GAME")

win = scr.get_rect()

# objects which will be displayed on the screen

ball = pygame.Rect(0, 0, 10, 10)
ball.center = win.center

left_paddle = pygame.Rect(0, 0, 10, 60)
left_paddle.midleft = win.midleft

right_paddle = pygame.Rect(0, 0, 10, 60)
right_paddle.midright = win.midright

# speed of the objects
vector_ball = [6, 6]
mv_left_pad = mv_right_pad = 25

# initial score
player_1_score = 0
player_2_score = 0

# line arguments
line_width = 2
half_width = dimensions[0] / 2


# function displays the middle line
def displaying_line():
    line = pygame.Rect(half_width, 0, line_width, dimensions[1])
    pygame.draw.rect(scr, WHITE, line)


# function displays text
def displaying_text():
    # message font
    myfont = pygame.font.Font('freesansbold.ttf', 50)
    msg = myfont.render("     PONG GAME !!!", True, RED)

    # placing text on the middle top
    msg_box = msg.get_rect()
    msg_box.midtop = win.midtop

    scr.blit(msg, msg_box)


# function puts the ball on the center line after scoring the point
def ball_return():
    # random position on the middle line (without extreme values)
    place_on_the_middle_line = random.randint(1, dimensions[1] - 1)
    ball.center = (half_width, place_on_the_middle_line)

    random_starting()


# function choosing the direction of the ball
def random_starting():
    # two options for calculating the direction of the ball
    range_of_choice = (-1, 1)
    vector_ball[0] *= random.choice(range_of_choice)
    vector_ball[1] *= random.choice(range_of_choice)


# function limits the range of movement of the ball
def detecting_limit():
    global player_1_score, player_2_score
    # change of the vector value depending on the position

    if ball.left < win.left:
        player_2_score += 1
        ball_return()
        random_starting()

    if ball.right > win.right:
        player_1_score += 1
        ball_return()
        random_starting()

    if ball.top < win.top or ball.bottom > win.bottom:
        vector_ball[1] = -vector_ball[1]


# function detects the collision between ball and two paddles
def detecting_collision():
    # the tolerance which will occur
    allowable_error = 10
    if ball.colliderect(left_paddle):
        # ball is colliding from the right of the paddle
        if ball.left < left_paddle.right:
            if abs(ball.centery - left_paddle.centery) \
                    < (ball.h + left_paddle.h) / 2:
                vector_ball[0] = -vector_ball[0]

        # ball is colliding from the top of the paddle
        if abs(ball.bottom - left_paddle.top) < allowable_error:
            if vector_ball[1] > 0:
                vector_ball[1] = -vector_ball[1]

        # ball is colliding from the bottom of the paddle
        if abs(ball.top - left_paddle.bottom) < allowable_error:
            if vector_ball[1] < 0:
                vector_ball[1] = -vector_ball[1]

    if ball.colliderect(right_paddle):
        # ball is colliding from the left of the paddle
        if ball.right > right_paddle.left:
            if abs(ball.centery - right_paddle.centery) \
                    < (ball.h + right_paddle.h) / 2:
                vector_ball[0] = -vector_ball[0]

        # ball is colliding from the top of the paddle
        if abs(ball.bottom - right_paddle.top) < allowable_error:
            if vector_ball[1] > 0:
                vector_ball[1] = -vector_ball[1]

        # ball is colliding from the bottom of the paddle
        if abs(ball.top - right_paddle.bottom) < allowable_error:
            if vector_ball[1] < 0:
                vector_ball[1] = -vector_ball[1]


# function detects the limit of movement of two paddles
def detecting_limit_of_paddles(paddle):
    if paddle.top < win.top:
        paddle.top = win.top

    if paddle.bottom > win.bottom:
        paddle.bottom = win.bottom


# function displays
def displaying_score():
    font = pygame.font.Font('freesansbold.ttf', 60)

    player_1_points = font.render(f"{player_1_score}", True, CYAN)
    player_2_points = font.render(f"{player_2_score}", True, CYAN)

    # creating score 1 on the screen
    player_1_points_box = player_1_points.get_rect()
    # coordinates of the score 1
    player_1_points_place = (dimensions[0] / 4, dimensions[1] / 2)
    player_1_points_box.center = player_1_points_place

    # creating score 2 on the screen
    player_2_points_box = player_2_points.get_rect()
    # coordinates of the score 2
    player_2_points_place = (dimensions[0] * 3 / 4, dimensions[1] / 2)
    player_2_points_box.center = player_2_points_place

    # drawing scores
    scr.blit(player_1_points, player_1_points_place)
    scr.blit(player_2_points, player_2_points_place)


# function creating the final text and result
def displaying_winner():
    # final font
    winner_font = pygame.font.Font('freesansbold.ttf', 50)
    global game_on

    # player 1 wins
    if player_1_score == 10:
        text = "PLAYER 1 WINS"
        name_of_the_winner = winner_font.render(text, True, RED)
        name_of_the_winner_box = name_of_the_winner.get_rect()
        name_of_the_winner_box.center = win.center

        scr.fill(BLACK)
        # displaying the winner
        scr.blit(name_of_the_winner, name_of_the_winner_box)
        pygame.display.flip()
        # display winner - time
        pygame.time.delay(5000)

        # the final result

        # shortcut of winner_font
        wf = winner_font
        # shortcut of player_1_score
        s1 = player_1_score
        # shortcut of player_2_score
        s2 = player_2_score
        result = wf.render(f"The result is {s1} : {s2}", True, RED)
        result_box = result.get_rect()
        result_box.center = win.center

        scr.fill(BLACK)
        # displaying the result
        scr.blit(result, result_box)
        pygame.display.flip()
        # display result - time
        pygame.time.delay(5000)

        game_on = False

    # player 2 wins
    elif player_2_score == 10:
        text = "PLAYER 2 WINS"
        name_of_the_winner = winner_font.render(text, True, RED)
        name_of_the_winner_box = name_of_the_winner.get_rect()
        name_of_the_winner_box.center = win.center

        scr.fill(BLACK)
        # displaying the winner
        scr.blit(name_of_the_winner, name_of_the_winner_box)
        pygame.display.flip()
        # display winner - time
        pygame.time.delay(5000)

        # the final result

        # shortcut of winner_font
        wf = winner_font
        # shortcut of player_1_score
        s1 = player_1_score
        # shortcut of player_2_score
        s2 = player_2_score
        result = wf.render(f"The result is {s1} : {s2}", True, RED)
        result_box = result.get_rect()
        result_box.center = win.center

        scr.fill(BLACK)
        # displaying the result
        scr.blit(result, result_box)
        pygame.display.flip()
        # display result - time
        pygame.time.delay(5000)

        game_on = False


# function displays welcome screen
def starting_game():
    # font and creating box with text
    welcome_font = pygame.font.Font('freesansbold.ttf', 50)
    welcome_text = welcome_font.render("THE GAME - PONG", True, RED)
    welcome_text_box = welcome_text.get_rect()
    welcome_text_box.center = win.center

    scr.blit(welcome_text, welcome_text_box)
    pygame.display.flip()

    # text display time
    pygame.time.delay(3000)

    counting_down()


# function counts down from 3 to 1
def counting_down():
    # counting down from 3 to 0
    for i in range(3, -1, -1):
        # font and number box
        countdown_font = pygame.font.Font('freesansbold.ttf', 50)
        countdown_text = countdown_font.render(str(i), True, RED)
        countdown_text_box = countdown_text.get_rect()
        countdown_text_box.center = win.center

        scr.fill(BLACK)
        scr.blit(countdown_text, countdown_text_box)
        pygame.display.flip()

        # each number display time
        pygame.time.delay(1000)


pygame.key.set_repeat(50, 50)
fps = pygame.time.Clock()

game_on = True

if __name__ == "__main__":
    starting_game()
    # main loop
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    left_paddle = left_paddle.move(0, -mv_left_pad)
                elif event.key == pygame.K_s:
                    left_paddle = left_paddle.move(0, mv_left_pad)
                elif event.key == pygame.K_UP:
                    right_paddle = right_paddle.move(0, -mv_right_pad)
                elif event.key == pygame.K_DOWN:
                    right_paddle = right_paddle.move(0, mv_right_pad)

        detecting_limit_of_paddles(left_paddle)
        detecting_limit_of_paddles(right_paddle)

        ball = ball.move(vector_ball)

        detecting_limit()
        detecting_collision()

        scr.fill(BLACK)
        displaying_line()
        displaying_text()
        displaying_score()

        pygame.draw.rect(scr, WHITE, ball)
        pygame.draw.rect(scr, WHITE, left_paddle)
        pygame.draw.rect(scr, WHITE, right_paddle)

        displaying_winner()

        pygame.display.flip()

        fps.tick(60)
