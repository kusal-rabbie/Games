import random
"""
This script provides users to play a tower blaster game against a simple algorithm
"""
MAXIMUM_MAIN_PILE_SIZE = 60
MAIN_PILE_SIZE = 0
PLAYER_PILE_SIZE = 10
DISCARD_PILE_SIZE = 40 - MAIN_PILE_SIZE


def validate_number(value):
    """
    Checks whether the input is a number
    """
    try:
        int(value)
        return True
    except ValueError:
        return False

def use_brick(top_brick, user_pile, discard):
    """
    A wrapper function for the find_and_replace functions with user input validation
    """
    done = False
    while not done:
        print("\nInsert the brick you want to replace")
        brick = input("> ")
        if validate_number(brick):
            brick = int(brick)
            done = find_and_replace(top_brick, brick, user_pile, discard)

def truncate_pile(tower):
    """
    Pops the first element off the given tower
    """
    for i in range(len(tower)-1):
        tower[i] = tower[i+1]
    tower.pop()


def shuffle(bricks):
    """
    Shuffles the given pile in place
    """
    random.shuffle(bricks)


def check_bricks(main_pile, discard):
    """
    Checks whether the main pile is empy, if so shuffles the discard pile and deals to main pile
    """
    if len(main_pile) == 0:
        shuffle(discard)
        for i in range(len(discard)-1):
            main_pile.append(discard.pop())


def check_tower_blaster(tower):
    """
    Checks whether the provided tower has achieved stability
    """
    return tower == sorted(tower)


def get_top_brick(brick_pile):
    """
    Allows to take a sneak peak at the top of the given pile
    """
    return brick_pile[0]


def deal_initial_bricks(main_pile):
    """
    Deals the two players two piles of bricks from the main pile
    """
    user_pile, pc_pile = [], []
    for i in range(PLAYER_PILE_SIZE*2):
        brick = get_top_brick(main_pile)
        if i%2==0:
            pc_pile.append(brick)
        else:
            user_pile.append(brick)
        for i in range(len(main_pile)-1):
            main_pile[i] = main_pile[i+1]
        main_pile.pop()
    return pc_pile, user_pile


def add_brick_to_discard(brick, discard):
    """
    This function adds the given brick to the begining of the discard pile
    """
    if discard == []: #Initial discard pile
        discard.append(brick)
    else:
        discard.append(discard[-1]) #Increase the size of the list by 1
        index = len(discard) - 2
        for i in range(index): #Loops through the elements in the discard pile and shifts every element one position right
            discard[index-i] = discard[index-1-i]
        discard[0] = brick #Assigns the given brick as the first element of the pile


def find_and_replace(new_brick, brick_to_be_replaced, tower, discard):
    """
    Replaces the brick_to_be_replaced with the new_brick in the pile tower. Returns true if the operation is succesfull
    """
    replaced = False
    if brick_to_be_replaced in tower: #Checks whether the given value is in the current user pile
        tower[tower.index(brick_to_be_replaced)] = new_brick #Replaces the selected brick with the new brick
        add_brick_to_discard(brick_to_be_replaced, discard)
        replaced = True
    return replaced

def computer_play(tower, main_pile, discard):
    """
    Playing logic of the computer
    """
    top_brick_discard = get_top_brick(discard)

    slot            = top_brick_discard//6
    if top_brick_discard%6 == 0:
        slot -= 1    
    slot_high       = 6*(slot+1)
    slot_low        = 6*(slot)
    current_brick   = tower[slot]

    if current_brick > slot_high or current_brick < slot_low :
        truncate_pile(discard)
        add_brick_to_discard(current_brick, discard)
        tower[slot] = top_brick_discard
    else:
        top_brick_main    = get_top_brick(main_pile)
        truncate_pile(main_pile)

        slot            = top_brick_main//6
        if top_brick_main%6 == 0:
            slot -= 1
        slot_high       = 6*(slot+1)
        slot_low        = 6*(slot)
        current_brick   = tower[slot]

        if current_brick > slot_high or current_brick < slot_low :
            add_brick_to_discard(current_brick, discard)
            tower[slot] = top_brick_main
        else:
            add_brick_to_discard(top_brick_main, discard)
    return tower


def main():
    """
    Main method where all the functions are chained together
    """
    # Initiates the game main pile
    main_pile = [i+1 for i in range(60)]
    shuffle(main_pile) 
    print("===========================================\nHi! Welcome to Blasting Towers!\n===========================================\nDealing cards")
    # Deals two piles of bricks for two players
    pc_pile, user_pile = deal_initial_bricks(main_pile)
    # Initiates the discard pile with the top brick of the main pile
    discard = []
    discard_top_brick = get_top_brick(main_pile)
    add_brick_to_discard(discard_top_brick, discard)
    main_pile = main_pile[1:]

    # Starts the game loop
    i = 1
    while True:
        if check_tower_blaster(pc_pile):
            print("\nHurray! PC wins!\n")
            break
        elif check_tower_blaster(user_pile):
            print("\nCongratulations! You win!!!\n")
            break
        else:
            print("Turn: ", i)
            check_bricks(main_pile, discard)
            discard_top_brick = get_top_brick(discard)
            print("Top Brick of discard pile :\t", discard_top_brick)
            if i%2 == 0: # First chance to play goes to the computer
                pc_pile = computer_play(pc_pile, main_pile, discard)
                i += 1
                continue
            while True: # User's chance to play
                print("\nYour tower :\t", user_pile, "\n")
                print("1.) Use top brick of discard pile (", discard_top_brick, ")\n", "2.) Check top brick of main pile", "\n")
                choice_1 = input("> ")
                if validate_number(choice_1): 
                    # User wants to use the top brick of the discard pile
                    if int(choice_1) == 1:
                        discard = discard[1:]
                        use_brick(discard_top_brick, user_pile, discard)
                        break                
                    # User wants to look at the main pile
                    elif int(choice_1) == 2:
                        main_top_brick = get_top_brick(main_pile)
                        print("The brick at the top of the main pile is ", main_top_brick)
                        while True:
                            print("1.) Use brick\n2.) Discard brick\n")
                            choice_2 = input("> ")
                            if validate_number(choice_2):
                                # User wants to use the top brick of the main pile
                                if int(choice_2) == 1:
                                    use_brick(main_top_brick, user_pile, discard)
                                    main_pile = main_pile[1:]
                                    break
                                # User wants to discard the top brick of the main pile
                                elif int(choice_2) == 2:
                                    add_brick_to_discard(main_top_brick, discard)
                                    main_pile = main_pile[1:]
                                    break
                                # Errorneous input
                                else:
                                    print("\n\'", choice_2, "\' IS NOT A VALID OPTION!")
                                continue
                            else:
                                print("\n\'", choice_2, "\' IS NOT A VALID OPTION!")
                        break
                else:
                    print("\n\'", choice_1, "\' IS NOT A NUMBER!")
                    continue 
            i += 1


if __name__ == '__main__':
    main()

