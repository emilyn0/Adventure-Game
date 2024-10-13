# Emily Nong, starter code for CS 115 Fall 2023 (McCoy)
#Programming Project 7, enhanced code 12/1/23
#This program's behavior is to be an adventure game where the player can navigate through Edmonds college campus. 
#The player must tour the whole campus to win the game.
#Persona, the example given in class: Elena is an engineer at Google with two years experience who has volunteered to attend local career fairs, primarily to help recruit for summer internships.
#She works on an AI-related project that works with large text datasets. A BS CS grad from UW, after transferring from Edmonds College, she enjoys trivia nights with her friends.

#This is the working code with the JSON save/load
#type in 'save' to save your game status, run the game again, and type in 'load'
#to load your previous game back.

#imports
import random
import json

# constants/messages
WELCOME_MSG = """ ************
    An Uber drops you off in a parking area. A sign here reads 'Welcome to Edmonds College'
    Type (H)elp for help. 
    """

HELP_MSG = """
    (H)elp - displays this information
    (N)orth - go north
    (E)ast - go east
    (S)outh - go south
    (W)est - go west
    (B)ack - go back to previous location
    (I)n - go inside a building
    (O)ut - leave a building
    (Q)uit - exit the game
    """

PROMPT = "==>"
BAD_INPUT_MSG = "I'm sorry, I don't understand that."


location = {
    (0, 0): "\nYou are in front of an open area with walkways in all directions. In the middle, there is a seating area filled with tables and chairs. There is a large abstract metal sculpture to the left side.",
    (0, 1): "\nYou are in front of an open area with walkways in all directions. In the middle, there is a seating area filled with tables and chairs. There is a large abstract metal sculpture to the left side.",
    (0, 2): "\nYou are in front of an open area with walkways in all directions. In the middle, there is a seating area filled with tables and chairs. There is a large abstract metal sculpture to the left side.",
    (0, 3): "\nYou are in front of an open area with walkways in all directions. In the middle, there is a seating area filled with tables and chairs. There is a large abstract metal sculpture to the left side.",
    (1, 0): "\nYou are in front of a parking area where students and staff can park. There isn't much space left and cars are beginning to pile up.",
    (2, 0): "\nYou are in front of a parking area where students and staff can park. There isn't much space left and cars are beginning to pile up.",
    (3, 0): "\nYou are in front of a parking area where students and staff can park. There isn't much space left and cars are beginning to pile up.",
    (3, 1): "\nYou are in front of a parking area where students and staff can park. There isn't much space left and cars are beginning to pile up.",
    (3, 2): "\nYou are in front of a parking area where students and staff can park. There isn't much space left and cars are beginning to pile up.",
    (1, 3): "\nYou are in front of a large field of well-kept grass, striped and used for soccer. Students and athletes come here to play when the weather is nice.",
    (2, 3): "\nYou are in front of a large field of well-kept grass, striped and used for soccer. Students and athletes come here to play when the weather is nice.",
    (3, 3): "\nYou are in front of a large field of well-kept grass, striped and used for soccer. Students and athletes come here to play when the weather is nice."
}

at_building = {
    (1, 2): "\nYou are in front of a 3-story concrete building with a grand entry. There is a large tree on the left side of the building. Its large glass windows make the inside very visible from the outside. A sign on the building says Montlake Terrace Hall.",
    (2, 2): "\nYou are in front of a building that is painted blue and white. It has small glass windows, but they are covered up with blinds from the inside. It is filled with student activity such as a bookstore, game room, cafe, and more! A sign on the building says Brier Hall.",
    (1, 1): "\nYou are in front of a building that has large, wooden and glass doors. It consistantly filled with faculty and students inside. \'LIBRARY\' is listed on the side of the building. A sign on the building says Lynnwood Hall.",
    (2, 1): "\nYou are in front of a modern, brick-sided, 3-story building with large windows. There are plants and a tree right next to the entrance. You will find students coming in and out frequently. A sign on the building says Snohomish Hall."
}

in_building_desc = {
    (1, 2): "\nYou enter into a bustling dining area. An espresso bar occupies most of one side. Automatic doors open up off the side to the counseling office and a seating area. \n\nYou wander to the expresso bar and the barista asks you something.",
    (2, 2): "\nYou enter into a large area with benches and vending machines off to the side. There is a bookstore off to the side, a staircase, and a creepy hallway with all the lights turned off.\n\nYou get the chills and get scared just by staring at the hallway. Do you approach it?",
    (1, 1): "You enter into a large area with a front desk and a large staircase leading up to a brightly lit library. There are thousands of books and students working silently.",
    (2, 1): "\nYou enter into an area filled with small tables to the left and a large set of stairs directly in front of you. To the right are vending machines and a seating area. Lab rooms open off the courtyard."
}

#responses for the npc that says multiple things
no = [
    "The student gets mad and pushes you to the ground. You quickly run away from them.",
    "The student stares at you and immidietly runs away, hitting you along the way. You lose your balance and fall on your face. You are all bruised now, but continue on.",
    "The student goes on a tempter tantrum and pushes a random cart into you. You unexpectdly hit your head a little too hard and died.",
    "The student claims that they will report you to the school as trespassing. You get scared, run off of campus and swear to never come back. You run and don't look back."]

yes = [
    "The student appreciates what you have done for them. You continue on.",
    "The student thanks you and gives you a kitten, claiming that you can have it. You hesitate but take it. You hold it in your arms for the rest of your adventure.",
    "The student thanks you and gives you a ham and cheese sandwich. You don't eat it and throw it away. You move on with your adventure and think about how weird that occurance was.",
    "The student says \'thank you\' five times before running off. You are confused but continue exploring."]


#keeps track of visited locations so far using lists
visited = {
    "visited_loc": [(3,0)]
}

candy = False
npc = False
finish = False

class Location:
    """
    Represents and processes a location in the game world.

    Attributes:
        coordinate (tuple): The coordinates of the location.
    """
    def __init__(self, coordinate):
        """
        Initializes a Location object.
        
        """
        self.coordinate = coordinate

    def print_location(self):
        """
        Checks if coordinate has been a visited location and returns the description of the coordinate
        
        """
        if self.coordinate not in visited["visited_loc"] and self.coordinate not in at_building and self.coordinate != (1,0):
            visited["visited_loc"].append(self.coordinate)
        if self.coordinate in location:
            return location[self.coordinate]
        elif self.coordinate in at_building:
            return at_building[self.coordinate]
        

class User:
    """
    Documents and represents a user in the game, including their different states.
    Processes users commands, movements, and health.

    Attributes:
        cur_loc (tuple): The current location of the user.
        last_loc (tuple): The last location of the user.
        health_value (int): The health value of the user.
        in_lyn_library (bool): Indicates if the user is in the library.
        in_building (bool): Indicates if the user is in a building.
    """

    def __init__(self, cur_loc, last_loc, health_value, in_lyn_library, in_building):
        """
        Initializes current location, last location, health, and if the user is in a library or in a building.
        
        """
    
        self.cur_loc = cur_loc
        self.health_value = health_value
        self.last_loc = last_loc
        self.in_lyn_library = in_lyn_library
        self.in_building = in_building

    def get_coord(self):
        """
        Returns the current coordinates of the user.
        """
        return self.cur_loc

    def get_last_coord(self):
        """
        Returns the last coordinates of the user.
        """
        return self.last_loc
    
    def get_in_library(self):
        """
        Returns whether the user is in the library.
        """
        return self.in_lyn_library
    
    def get_in_building(self):
        """
        Returns whether the user is in a building.
        """
        return self.in_building
    
    def get_health(self):
        """
        Returns the health value of the user.
        """
        return self.health_value

    def direction(self, direction):
        """
        Handles the user's movement direction and choice of command.
        """
        if isinstance(self.cur_loc, list):
            self.cur_loc = tuple(self.cur_loc)  # Convert to tuple if it's a list

        if self.cur_loc == (3, 0) and len(visited["visited_loc"]) == 16 and direction == "E":
            if self.health_value <= 0:
                return "no win"
            else:
                return "yes win"

        if (self.cur_loc in location or self.cur_loc in at_building):
            if self.in_lyn_library and (direction == "N" or direction == "W" or direction == "S" or direction == "E"):
                return "fall window"
            elif direction == "N" and not self.in_building and ((self.cur_loc[0], self.cur_loc[1] + 1) in location or (self.cur_loc[0], self.cur_loc[1] + 1) in at_building):
                self.last_loc = self.cur_loc
                self.cur_loc = (self.cur_loc[0], self.cur_loc[1] + 1)
            elif direction == "W" and not self.in_building and ((self.cur_loc[0] - 1, self.cur_loc[1]) in location or (self.cur_loc[0] - 1, self.cur_loc[1]) in at_building):
                self.last_loc = self.cur_loc
                self.cur_loc = (self.cur_loc[0] - 1, self.cur_loc[1])
            elif direction == "S" and not self.in_building and ((self.cur_loc[0], self.cur_loc[1] - 1) in location or (self.cur_loc[0], self.cur_loc[1] - 1) in at_building):
                self.last_loc = self.cur_loc
                self.cur_loc = (self.cur_loc[0], self.cur_loc[1] - 1)
            elif direction == "E" and not self.in_building and ((self.cur_loc[0] + 1, self.cur_loc[1]) in location or (self.cur_loc[0] + 1, self.cur_loc[1]) in at_building):
                self.last_loc = self.cur_loc
                self.cur_loc = (self.cur_loc[0] + 1, self.cur_loc[1])
            elif direction == "H":
                return "help"
            elif direction == "Q":
                print("Thanks for playing!")
                return "quit"
            elif direction == "I" and self.cur_loc in at_building:
                return "in building"
            elif direction == "I" and self.cur_loc not in at_building:
                return "no building"
            elif direction == "B" and not self.in_lyn_library and not self.in_building:
                self.cur_loc = self.last_loc
            elif direction == "O" and not self.in_lyn_library:
                return "out"
            else:
                return "no"
        else:
            return "no"

        
    def health(self, direction):
        """
        Handles the users health. Everytime a user moves, the health decreases.
        """
        if direction != "H" and direction != "I" and direction != "O":
            if (self.cur_loc != self.last_loc) or direction == "B":
                if self.health_value > 0: 
                    self.health_value -=6
                    if self.health_value <=0:
                        self.health_value = 0
                    elif self.health_value >= 100:
                        self.health_value = 100
        return self.health_value

#return current game data
    def to_dict(self):
        return {
            'cur_loc': self.cur_loc,
            'health_value': self.health_value,
            'last_loc': self.last_loc,
            'in_lyn_library': self.in_lyn_library,
            'in_building': self.in_building,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

#basis for every npc
class RandomNPC:
    """
    Represents a non-player character with random characteristics.

    Attributes:
        conversation (str): The initial conversation of the NPC.
    """
    def __init__(self, conversation):
        """
        Initializes a Random NPC object.
        """
        self.conversation = conversation
    def rand_loc(self):
        """
        Generates random coordinates for the NPC.
        """
        random_x = random.randint(0, 3)
        random_y = random.randint(0, 3)
        return (random_x, random_y)
    def convo(self):
        """
        Initiates a conversation with the NPC.
        """
        print(self.conversation)
        while True:
            npc_answ = input(PROMPT)
            if npc_answ == "yes" or npc_answ == "Yes" or npc_answ == "y" or npc_answ == "Y":
                return "yes"
            elif npc_answ == "no" or npc_answ == "No" or npc_answ == "n" or npc_answ == "N":
                return "no"
            print(BAD_INPUT_MSG, "Please answer the question.\n")
        
def getUserCmd():
    while True:
        user_input = input(PROMPT)
        if user_input == "N" or user_input == "n" or user_input == "North" or user_input == "north" or user_input == "NORTH":
            return "N"
        elif user_input == "S" or user_input == "s" or user_input == "South" or user_input == "south" or user_input == "SOUTH":
            return "S"
        elif user_input == "H" or user_input == "h" or user_input == "Help" or user_input == "help" or user_input == "HELP":
            return "H"
        elif user_input == "Q" or user_input == "q" or user_input == "Quit" or user_input == "quit" or user_input == "QUIT":
            return "Q"
        elif user_input == "W" or user_input == "w" or user_input == "West" or user_input == "west" or user_input == "WEST": 
            return "W"
        elif user_input == "E" or user_input == "e" or user_input == "East" or user_input == "east" or user_input == "EAST":
            return "E"
        elif user_input == "In" or user_input == "in" or user_input == "i" or user_input == "I":
            return "I"
        elif user_input == "Out" or user_input == "out" or user_input == "o" or user_input == "O":
            return "O"
        elif user_input == "B" or user_input == "b" or user_input == "Back" or user_input == "back":
            return "B"
        elif user_input.lower() == "save":
            save_game()
            print("Game saved.\n")
        elif user_input.lower() == "load":
            load_game()
            print("Game loaded.\n")
        else:
            print(BAD_INPUT_MSG, "\n")
            
#Cafe question where user has to eat or drink something
def cafe_ques():
    while True:
        print("The barista offers you a muffin, a cheese danish, some candy, and a mocha latte. They do not have water. What do you pick?\n")
        cafe_ques_answ = input(PROMPT)
        if cafe_ques_answ == "Muffin" or cafe_ques_answ == "muffin":
            return "muff"
        elif cafe_ques_answ == "Cheese Danish" or cafe_ques_answ == "cheese danish" or cafe_ques_answ == "Cheese danish" or cafe_ques_answ == "cheese Danish":
            return "danish"
        elif cafe_ques_answ == "Mocha Latte" or cafe_ques_answ == "mocha latte" or cafe_ques_answ == "Mocha latte" or cafe_ques_answ == "mocha Latte" or cafe_ques_answ == "Latte" or cafe_ques_answ == "latte":
            return "latte"
        elif cafe_ques_answ == "Candy" or cafe_ques_answ == "candy" or cafe_ques_answ == "CANDY":
            return "candy"
        elif cafe_ques_answ == "Nothing" or cafe_ques_answ == "Leave" or cafe_ques_answ == "No"  or cafe_ques_answ == "None" or cafe_ques_answ == "nothing" or cafe_ques_answ == "leave" or cafe_ques_answ == "no" or cafe_ques_answ == "none":
            return "leave"
        print(BAD_INPUT_MSG)
        
def lbrary_ques():
    global user
    while True:
        print("\nYou are intrigued by the light coming from the staircase.\n")
        print("Do you go up the stairs to the second floor?\n")
        library_answ = input(PROMPT)
        if library_answ == "yes" or library_answ == "Yes" or library_answ == "y" or library_answ == "Y":
            return "yes"
        elif library_answ == "No" or library_answ == "no" or library_answ == "n" or library_answ == "N":
            return "no"
        print(BAD_INPUT_MSG,)

def special_square():
    global cur_loc, last_loc, user, rand_npc, rand_npc_loc, health_index, desc 
    
    if last_loc == (0, 0): #special square!!
        print("Health:", health_index)
        if cur_loc not in visited["visited_loc"]:
            visited["visited_loc"].append(cur_loc)
        print("Locations visited: " + str(len(visited["visited_loc"])) + " out of 16")
        print(location[(1, 0)], "\n")

    else:
        print("Health:", health_index)
        print("Locations visited: " + str(len(visited["visited_loc"])) + " out of 16")
        print(desc, "\n\nA sudden wind storm takes you for a ride!\n")
        i = 0
        b = 0
        while i <=2:
            random_x = random.randint(0, 3)
            random_y = random.randint(0, 3)
            cur_loc = (random_x, random_y)
            while cur_loc == (0, 3) or cur_loc == (1, 0) or cur_loc == rand_npc_loc:   #adjusted so it can't land interfere with NPC convos
                random_x = random.randint(0, 3)
                random_y = random.randint(0, 3)    
                cur_loc = (random_x, random_y)
            get_description = Location(cur_loc)
            desc = get_description.print_location()
            print("Health:", health_index)
            print("Locations visited: " + str(len(visited["visited_loc"])) + " out of 16")
            print(desc, "\n")
            b += 1
            i += 1
            if b == 1:
                print("\nYou get swept up again!\n")
            elif b == 2:
                print("\nYou get swept up one last time!\n")
            else:
                print("\nThis is where you finally land.\n")
                
def save_game():
    file_path = "text_game.json"
    game_state = {
        'user': user.to_dict(),
        'visited': visited,
        'candy': candy,
        'rand_npc_loc': rand_npc_loc,
    }

    with open(file_path, "w") as file:
        json.dump(game_state, file)

# Function to load the gamedata
def load_game():
    global user, visited, candy, rand_npc_loc, met_trivia_person

    file_path = "text_game.json"

    with open(file_path, "r") as file:
        data = json.load(file)

    user = User.from_dict(data['user'])
    visited = data['visited']
    candy = data['candy']
    rand_npc_loc = data['rand_npc_loc']
                
def main():
    global finish, desc, health_index, cur_loc, cmd, last_loc, user, candy, rand_npc, rand_npc_loc, npc 

    file_path = "text_game.json"
            
    #inital game state
    user = User((3,0), (3,0), 100, False, False)
    libr_status = user.get_in_library()
    candy_trivia = 0
    met_trivia_person = False

    #npc objects
    rand_npc = RandomNPC("You realize you forgot to tell your mom where you are and she will get worried if she doesn't find you at home. Your phone just died.\n\nWhile panicking you bump into another student that is hurriedly trying to get to class. \n\nShould you ask him to borrow his phone?\n")
    frank_npc = RandomNPC("")
    zombie_npc = RandomNPC("")
    npc_one = RandomNPC("\nA student pokes you and asks you if you have a pencil on you that they can borrow. You mysteriously have one in your pocket. Do you be a nice person and give him the pencil or no?\n")
    npc_two = RandomNPC("\nA student slips on a big pile of water and falls right in front of you. Do you help them up or no?\n")
    npc_three = RandomNPC("\nA student is crying in the corner of the room. He asks you to leave him alone. Do you or no?\n")
    npc_four = RandomNPC("\nA student asks where the bathroom is and is about to puke. Do you show him where the bathroom is or no?\n")
    npc_multiple = [npc_one, npc_two, npc_three, npc_four]
    
    rand_npc_loc = rand_npc.rand_loc()
    print(WELCOME_MSG)
    print("Health:", 100)
    print("Locations visited: " + str(len(visited["visited_loc"])) + " out of 16\n")
    while True:
        in_building_status = user.get_in_building()
        cmd = getUserCmd()
        position_change = user.direction(cmd)
        if position_change == "quit":
            save_game()
            break
        elif position_change == "no win":
            print("You need to have more energy to be able to go this way.\n")

        #added feature to project 6. Player must answer trivia question to pass if all other requirements to pass are met.
        #if player gets question wrong, player must bring back candy.    
        elif position_change == "yes win" and met_trivia_person == False:
            if met_trivia_person == False:
                print("Someone stops you in your tracks, informing you that you need to asnwer a question in order to advance in this direction. They ask:")
                print("Which one of the items is sold in Montlake Terrace Hall?\n\nCandy\n\nDonuts\n\nCupcakes\n\nWater\n")
                answer_triv = input(PROMPT)
                if answer_triv == "candy" or answer_triv == "Candy": 
                    print("Congratulations! You have finished your tour of Edmonds College. A bus arrives to whisk you away. Please come again soon!")
                    met_trivia_person = True
                    break
                elif answer_triv == "donuts" or answer_triv == "Donuts" or answer_triv == "Cupcakes" or answer_triv == "cupcakes" or answer_triv == "water" or answer_triv == "Water":
                    print("That is not correct. Bring back candy to pass.\n")
                    met_trivia_person = True
                else:
                    print("I don't understand. Type in one one the options given to asnwer the question.\n")
        elif position_change == "yes win" and cmd == "E" and met_trivia_person == True:
            if candy_trivia >= 1:
                print("The random person lets you through. You have finished your tour of Edmonds College. A bus arrives to whisk you away.") 
                break
            else:
                print("Plese bring back candy to pass. (Go to Mountlake Terrace Hall if you are stuck).\n")
        elif position_change == "help":
            print(HELP_MSG)
        elif position_change == "out" and not in_building_status:
            print("You are already outside.\n")
        elif position_change == "in building" and in_building_status:
            print("You are already inside.\n")
        elif position_change == "no":
            print("You can't go this way.\n")
        elif position_change == "no building":
            print("Sorry there is no building here.\n")
        elif position_change == "fall window":
            print("The librarian doesn't see you and accidently runs into you with their book cart. You faint and wake up in the hospital. You decide to never go back to campus.")
            break
        else:
            #if the user wants to move, it is processed here
            last_loc = user.get_last_coord()
            health_index = user.health(cmd)
            cur_loc = user.get_coord()
            if cur_loc == (1, 0):
                special_square()
            elif cur_loc == (0, 3):
                #npc zombie
                if cur_loc not in visited["visited_loc"]:
                    visited["visited_loc"].append(cur_loc)
                print("Health:", health_index)
                print("Locations visited: " + str(len(visited["visited_loc"])) + " out of 16")
                print(desc, "\n\nA zombie named Tristan suddenly approaches you. Do you conintue talking to him?")
                zombie_result = zombie_npc.convo()
                if zombie_result == "no":
                    print("You leave and continue on your exploration.\n")
                elif zombie_result == "yes":
                    print("He seems to want something small and sweet, something that will give you a lot of energy. He really wants candy. \n\nDo you give him candy?")
                    zombie_result = zombie_npc.convo()
                    if zombie_result == "no":
                        print("You leave and continue on your exploration. The zombie waves goodbye.\n")                            
                    elif zombie_result == "yes":
                        if candy == False:
                            print("You do not have any candy to give at the moment. Come back whenever you have some...\n")
                        elif candy == True:
                            print("You give him some candy and is super happy. He secretly shows you another way to get off of campus. \n\nYou are super excited to finally leave. A bus arrives to whisk you away.")
                            finish = True
            elif position_change == "out" and in_building_status:
                print("Health:", health_index)
                print("Locations visited: " + str(len(visited["visited_loc"])) + " out of 16")
                get_description = Location(cur_loc)
                desc = get_description.print_location()
                print(desc, "\n")
                user.in_building = False
            elif position_change == "in building" and not in_building_status:
                print("Health:", health_index, "\n", in_building_desc[cur_loc])
                user.in_building = True
                if cur_loc == (1, 2):
                    #option to eat food
                    cafe = cafe_ques()
                    if cafe == "muff" and health_index > 0:
                        user.health_value = health_index + 8 
                        print("You now have more energy to explore the campus!\n")
                    elif cafe == "danish" and health_index > 0:
                        user.health_value = health_index + 10
                        print("You now have more energy to explore the campus!\n")
                    elif cafe == "latte" and health_index > 0:
                        user.health_value = health_index + 15
                        print("You now have more energy to explore the campus!\n")
                    #Added additional option for candy. Related to an enhancement in coding project 5.
                    elif cafe == "candy" and met_trivia_person == True:
                        user.health_value = health_index + 30
                        print("You eat some candy and store the rest in your pocket. Go back to the start to deliver the candy.")
                        candy_trivia = candy_trivia + 1
                    elif cafe == "candy" and health_index > 0:
                        print("You store some of the candy in your pocket and eat a few pieces. You might need the candy later for something...\n")
                        candy = True
                        user.health_value = health_index + 10 
                    elif (cafe == "candy" and health_index <= 0) or (cafe == "muff" and health_index <= 0) or (cafe == "danish" and health_index <= 0) or (cafe == "latte" and health_index <= 0):
                        user.health_value = health_index + 30
                        print("You now have more energy to explore the campus!\n")
                    elif cafe == "leave":
                        print("\nThe barista says bye, but you are at still inside the building.\n")
                    else:
                        print("You are already full of energy.\n")
                    if user.health_value >=100:
                        user.health_value = 100
                    health_index = user.health(cmd)
                    print("Health:", health_index, "\n")
                elif cur_loc == (1, 1) and not libr_status:
                    second_floor_library = lbrary_ques()
                    #option to go up to library
                    if second_floor_library == "yes":
                        print("You walk up the stairs and see a magnificiant library with thousands of books. You love to read.")
                        print("\nCurious, you reach out to grab one of the books, but you are startled by the librarian.")
                        print("\nYou get scared but continue on.\n")
                        user.in_lyn_library = True
                    if second_floor_library == "no":
                        print("You stay on the first floor.")
                        print("\nA group of students awkwardly try to get past you because you were standing in the middle of the hallway staring at the stairs.\n")
                elif cur_loc == (2, 1):
                    multiple_npc = random.choice(npc_multiple).convo()
                    if  multiple_npc == "no":
                        n = random.choice(no)
                        print(n, "\n")                 
                        if n == no[2] or n == no[3]:
                            break
                    elif multiple_npc == "yes":
                        print(random.choice(yes), "\n")
                elif cur_loc == (2, 2):
                    #npc frankenstein
                    frank_result = frank_npc.convo()
                    if frank_result == "no":
                        print("You run away from the hallway and don't look back. You continue on with your tour.\n")
                    elif frank_result == "yes":
                        print("You walk into the hallway slowly. Suddenly you see a shawdow followed by a large figure. Do you continue on?")
                        frank_result = frank_npc.convo()
                        if frank_result == "no":
                            print("You run back, out of the hallway. You are so tired from all that running. You lose energy.")
                            user.health_value = health_index - 7
                            if user.health_value <=0:
                                user.health_value =0
                            print("\nHealth:", user.get_health(), "\n")
                        elif frank_result == "yes":
                            print("The figure emerges and you let out a scream. The figure is frankenstein. He tells you to stop screaming. You stop and he asks how your day is. Do you reply back?")
                            frank_result = frank_npc.convo()
                            if frank_result == "no":
                                print("He gets mad at you and eats you. Unfortunately, you did not survive. He peacefully goes back into the shadow, waiting for another person to walk by.")
                                break
                            elif frank_result == "yes":
                                print("You become calm again and you guys have a peaceful conversation. You gain some energy for stopping by and talking to frankenstein. You guys part ways.")
                                user.health_value = health_index + 7 
                                print("\nHealth:", user.get_health(), "\n")
                if cur_loc not in visited["visited_loc"]:
                    visited["visited_loc"].append(cur_loc)                    
            else:
                get_description = Location(cur_loc)
                desc = get_description.print_location()
                print("Health:", health_index)
                print("Locations visited: " + str(len(visited["visited_loc"])) + " out of 16")
                print(desc, "\n")
                if cur_loc == rand_npc_loc and not in_building_status and not npc:
                    #lurking npc
                    npc = True
                    npc_result = rand_npc.convo()
                    if npc_result == "yes":
                        print("He gets mad and storms off. You made him late for class and you can't call your mom. Your only choice is to keep exploring the campus.\n")
                    else:
                        print("He picks up the books you made him drop and hurries off without a word. He glares back at you as you watch him disappear.\n")
            if health_index == 0:
                print("You have run out of energy. Go to Mountlake Terrace to gain more energy and to freshen up.\n")
            if finish == True:
                break

main()
