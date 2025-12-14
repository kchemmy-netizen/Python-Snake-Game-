import turtle 
import time 
import random 
from typing import List

# --- Constants ---
WIDTH, HEIGHT = 600, 600
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
BORDER_X = WIDTH // 2 - 10
BORDER_Y = HEIGHT // 2 - 10
SNAKE_MOVE_DISTANCE = 20
FOOD_COLLISION_DISTANCE = 20
SEGMENT_COLLISION_DISTANCE = 20




# Menu Buttons 
buttons = [] 

def create_button(text, y_pos): 
    # Use one turtle for both button and label for better layering
    btn = turtle.Turtle() 
    btn.hideturtle()
    btn.penup() 
    btn.color('white') 
    
    # Draw the button rectangle manually
    btn.goto(-100, y_pos - 20)
    btn.begin_fill()
    for _ in range(2):
        btn.forward(200) # width
        btn.left(90)
        btn.forward(40)  # height
        btn.left(90)
    btn.end_fill()

    # Write the text on top
    # CRITICAL FIX: Change pen color for the text AFTER drawing the button
    btn.color('black')
    btn.goto(0, y_pos - 10)
    btn.write(text, align='center', font=('Arial', 16, 'bold'))
    buttons.append((btn, text))
    return btn 


# Create Buttons 
start_btn = create_button('Start Game', 50) 
options_btn = create_button('Options', 0) 
quit_btn = create_button('Quit', -50) 

# Game Start Flag 
game_started = False 
running = True

# Click Handling 
def check_click(x, y): 
        global game_started 


        for btn, text in buttons: 
            # The button's y-range is from y_pos-20 to y_pos+20
            # btn.ycor() is y_pos-10, so the button's center is at btn.ycor()+10
            button_center_y = btn.ycor() + 10

            # Button Hitbox - check if click is within the button's drawn area
            if -100 < x < 100 and button_center_y - 20 < y < button_center_y + 20:

                if text == 'Start Game': 
                    game_started = True 

                    # Remove Menu 
                    for b, _ in buttons: 
                        b.clear() # Clear the turtle that drew the button and text
                    
                    # Game objects are now created after 'Start' is clicked
                    start_game_objects()
                    return 
                
                elif text == 'Options': 
                    print('Options Clicked') 
                elif text == 'Quit': 
                    turtle.bye() 


class Snake:
    def __init__(self):
        self.segments: List[turtle.Turtle] = []
        self.create_snake()
        self.head = self.segments[0]
        self.head.direction = "stop"

    def create_snake(self):
        # Create the initial snake body
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        new_segment = turtle.Turtle("square")
        new_segment.color("black")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def extend(self):
        # Add a new segment to the snake
        self.add_segment(self.segments[-1].position())

    def move(self):
        # Move tail segments to the position of the one in front
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        
        # Move the head
        if self.head.direction == 'up':
            self.head.sety(self.head.ycor() + SNAKE_MOVE_DISTANCE)
        if self.head.direction == 'down':
            self.head.sety(self.head.ycor() - SNAKE_MOVE_DISTANCE)
        if self.head.direction == 'left':
            self.head.setx(self.head.xcor() - SNAKE_MOVE_DISTANCE)
        if self.head.direction == 'right':
            self.head.setx(self.head.xcor() + SNAKE_MOVE_DISTANCE)

    def reset(self):
        for seg in self.segments:
            seg.goto(1000, 1000) # Move off-screen
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]
        self.head.direction = "stop"

    def up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.7, stretch_wid=0.7)
        self.color("red")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        random_x = random.randint(-BORDER_X + 20, BORDER_X - 20)
        random_y = random.randint(-BORDER_Y + 20, BORDER_Y - 20)
        self.goto(random_x, random_y)

class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align="center", font=("Courier", 24, "normal"))

    def increase_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_scoreboard()

    def reset(self):
        self.score = 0
        self.update_scoreboard()

# --- Game Setup ---
wn = turtle.Screen()
wn.title('Chemmy\'s Awesome Game') 
wn.bgcolor('green') 
wn.setup(width=WIDTH, height=HEIGHT) 
wn.tracer(0) 

# Listen for clicks 
wn.onclick(check_click) 

# --- Main Game Logic ---
snake = None
food = None
scoreboard = None

def start_game_objects():
    global snake, food, scoreboard
    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()
    
    # Controls - now they talk to the snake object
    wn.listen()
    wn.onkeypress(snake.up, "w")
    wn.onkeypress(snake.down, "s")
    wn.onkeypress(snake.left, "a")
    wn.onkeypress(snake.right, "d")

delay = 0.1
try: 
    while running: 
        if not game_started: 
            wn.update() 
            continue 


        wn.update()
        time.sleep(delay)
        snake.move() 

        # Border Collision 
        if (snake.head.xcor() > BORDER_X or snake.head.xcor() < -BORDER_X or
                snake.head.ycor() > BORDER_Y or snake.head.ycor() < -BORDER_Y):
            time.sleep(1)
            scoreboard.reset()
            snake.reset()
            delay = 0.1

        # Food Collision 
        if snake.head.distance(food) < FOOD_COLLISION_DISTANCE:
            food.refresh()
            snake.extend()
            scoreboard.increase_score()
            delay = max(0.003, delay - 0.003) 

        # Body Collision 
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < SEGMENT_COLLISION_DISTANCE:
                time.sleep(1)
                scoreboard.reset()
                snake.reset()
                delay = 0.1

except turtle.Terminator: 
    running = False
    print('Window Closed') 