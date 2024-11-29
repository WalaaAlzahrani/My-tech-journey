name = input("type your name: ")
print("Welcome ", name, " to this adventure!")
answer = input("You are on a dirt road, it has come to an end. Which way would like to go, left or right? ").lower()

if answer == "left":
    ans2 = input("You have come to a river, you can either walk around or swim accross. Type 'walk' for walking around or 'swim' for swimming accross. ").lower()
    if ans2 == "walk":
        ans3 = input("You walked around the river and found a small cave. Inside the cave you found a caveman. What do you think is the best desicion to make right now? 'go back' to where you were or 'face' the caveman? ").lower()
        if ans3 == "go back":
            print("You went back to the river, swam across and got eaten by an alligator")
        elif ans3 == "face":
            print("You faced the caveman and he was wary of you so he killed you at the spot with his weapon")
        else:
            print("Not a valid option, You lose!")
    elif ans2 == "swim":
        print("You swam across and got a cramp. You drowned.")
    else:
        print("Not a valid option, You lose!")

elif answer == "right":
    ans2 = input("You come to a bridge, it looks wobbly, do you want to 'cross' it or 'head back'? ").lower()
    if ans2 == "cross":
        ans3 = input("You cross the bridge and meet a stranger, do you talk to them or no? 'yes/no'").lower()
        if ans3 == "yes":
            print("You talked to the stranger and they gave you a map that leads to a treasure that you ended up owning")
        elif ans3 == "no":
            print("You ignored the stranger and they cursed you. You got lost in the woods and died")
    elif ans2 == "head back":
        print("You went back to the dirt road and missed the opportuinity to find a treasure")
    else:
        print("Not a valid option, You lose!")
else:
    print("Not a valid option, You lose!")

print("Thak you for trying ", name)