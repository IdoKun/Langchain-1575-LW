
# Import the required libraries
import random
import curses

# Initialize the screen
s = curses.initscr()

# Set the cursor state. The visibility of the cursor is set to 0 (invisible).
curses.curs_set(0)

# Get the height and width of the window
sh, sw = s.getmaxyx()

# Create a new window using the screen height and width, and starting at the top left corner (0, 0)
w = curses.newwin(sh, sw, 0, 0)

# Enable the keypad for the created window so that it can accept special keys (like the arrow keys)
w.keypad(1)

# Set the screen refresh rate. The screen will refresh every 100 milliseconds.
w.timeout(100)

# Create the initial snake body parts. The snake starts with three body parts.
# The snake head is at the center of the screen, and the two initial body parts trail behind it to the left.
snk_x = sw//4
snk_y = sh//2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Create the initial food piece at the center of the screen
food = [sh//2, sw//2]

# Add the food to the screen
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

# Initialize the snake's direction to move right
key = curses.KEY_RIGHT

# Game logic starts here
while True:
    # Get the next key. If no key is pressed, then the next key is -1.
    next_key = w.getch()

    # If no key is pressed, keep moving in the current direction. Otherwise, move in the direction of the key pressed.
    key = key if next_key == -1 else next_key

    # Check if the snake has run into the border or itself. If so, then end the game.
    if snake[0][0] in [0, sh] or snake[0][1]  in [0, sw] or snake[0] in snake[1:]:
        curses.endwin()
        quit()

    # Determine the new head of the snake based on the direction the snake is moving.
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Insert the new head of the snake.
    snake.insert(0, new_head)

    # Determine what happens when the snake runs into the food
    if snake[0] == food:
        # If the snake runs into the food, then a new piece of food is created.
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            # If the new piece of food is not part of the snake body, then add the new food to the screen.
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        # If the snake didn't run into the food, then it moves forward and its tail (the last body part) is removed.
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Add the new head of the snake to the screen.
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
