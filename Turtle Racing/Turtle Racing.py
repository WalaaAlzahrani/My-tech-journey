import turtle
import time
import random

WIDTH, HEIGHT = 500, 500
COLORS = ["red", "green", "blue", "orange", "yellow", "black", "purple", "pink", "brown", "cyan"] # A list of colors for the racers. This will determine the appearance of each turtle.

#Function to get a valid number of racers from the user within the range of 2 to 10.
def get_number_of_racers():
    racers = 0  #The variable racers is initialized to 0. This variable will eventually hold the valid number of racers entered by the user.
    
    while True:
        racers = input("Enter the number of racers (2 - 10): ")
        #The isdigit() method checks if the input string consists only of digits. 
        #If it does, the string is converted to an integer.
        if racers.isdigit(): 
            racers = int(racers)
        else:
            print("Invalid input. Please enter a number.")
            continue

        if 2 <= racers <= 10: # Validates that the number is within the allowed range.
            return racers
        else:
            print("Invalid number of racers. Please enter a number between 2 and 10.")

#Function that simulates the race and determines the winner.
def race(colors):
    turtles = create_turtles(colors) #Creates turtle racers with the provided colors.

    while True:
        for racer in turtles:
            distance = random.randrange(1, 20)
            racer.forward(distance)

            x, y = racer.pos() #Gets the turtle's current position.
            if y >= HEIGHT // 2 - 10: #Checks if the turtle has crossed the finish line (top of the screen)
                return colors[turtles.index(racer)] #Returns the color of the winning turtle.

#The function create_turtles() creates a list of turtle objects with different colors and speeds.
def create_turtles(colors):
    turtles = []
    spacingx = WIDTH // (len(colors) + 1) #Calculates horizontal spacing between turtles.
    for i, color in enumerate(colors):
        racer =turtle.Turtle()
        racer.color(color)
        racer.shape("turtle")
        racer.left(90) # Rotates the turtle to face upward.
        racer.penup() # Lifts the pen to avoid drawing while positioning.
        racer.setpos(-WIDTH//2 + (i + 1) * spacingx, -HEIGHT//2 + 20) # Positions the turtle at the starting line.
        racer.pendown() # Puts the pen down to start drawing during the race.
        turtles.append(racer) # Adds the turtle to the list.
    return turtles # Returns the list of turtles.

#Sets up the turtle graphics window.
def init_turtle():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Turtle Racing!")

racers = get_number_of_racers()
init_turtle() #Initializes the turtle graphics screen.

random.shuffle(COLORS) #Randomly shuffles the colors to assign them to turtles.
colors = COLORS[:racers] #Selects the required number of colors based on the number of racers.
winner = race(colors) #Simulates the race and determines the winner.
print("The winner is the ", winner, " turtle!") #Announces the winning turtle.
time.sleep(3) #Waits for 3 seconds before closing the program.
