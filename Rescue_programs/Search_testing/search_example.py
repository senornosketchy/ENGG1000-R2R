def main(past_moves, steps):
    maze = input("Are you still in the maze y/n: ").lower()
    while maze == "y":
        print(past_moves)
        print(steps)
        junction = input("Is there a junction y/n: ").lower()
        if junction == "y":
            path = input("Is the path marked y/n: ").lower()
            if path == "n":
                sub_alg(steps)
            else:
                print("you go backwards")
        else:
            sub_alg(steps)
        steps += 1


def sub_alg(steps):
    print(past_moves)
    forward = input("can you go forward y/n: ").lower()
    if forward == "y":
        print("you go forward")
        past_moves.append("forward")
        main(past_moves, steps)
    else:
        right = input("can you go right y/n: ").lower()
        if right == "y":
            print("you turn right")
            past_moves.append("right")
            main(past_moves, steps)
        else:
            left = input("can you go left y/n: ").lower()
            if left == "y":
                print("you turn left")
                past_moves.append("left")
                main(past_moves, steps)
            else:
                go_back(past_moves)
                print("you go backwards")
                past_moves.append("backwards")
                main(past_moves, steps)
steps = 0
past_moves = []
main(past_moves, steps)