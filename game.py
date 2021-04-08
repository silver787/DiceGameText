import random

# imports the random modules to generate random numbers to be used as players dice rolls

LOGINS_FILE = "logins.txt"
HIGH_SCORES_FILE = "highscores.txt"


# constants specify the locations of the logins file, and the highscores file


class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0
        self.roll_1 = 0
        self.roll_2 = 0


# creates a player class used to store related information about players that log in


class Game:
    def __init__(self):
        self.round = 0
        self.turn = 1


# creates a game class to store related information about games that are being played


def validate(word):
    if 2 < len(word) < 11:
        return True
    else:
        return False


# a function used to validate user input e.g. passwords, to ensure they are strong enough,
# and in the case of usernames, be sustainably created


def evaluate(roll_1, roll_2):
    res = []

    if roll_1 == roll_2:
        res.append('double')

    if (roll_1 + roll_2) % 2 == 0:
        res.append('even')

    return res


# a function that determines certain characteristics about a roll, such as whether it is even, or is a double


def login(player):
    """A function that allows a user to login, this function is repeated twice: once for player one, and once for player two"""
    while True:
        choice_1 = input(f"Player {player}, do you want to login, create an account, or exit? (L/C/E): ")
        if choice_1.upper() == "L":
            while True:
                choice_2 = input("Are you sure you want to login? (Y/N): ")
                if choice_2.upper() == "N":
                    break
                if choice_2.upper() == "Y":
                    login_username = input("Please enter your username: ")
                    login_password = input("Please enter your password: ")
                    with open(LOGINS_FILE, 'r') as f:
                        for i in f:
                            i = i.split(' ')
                            if i[0] == login_username and i[1].strip() == login_password:
                                print(f"Congratulations player {player}, login sucessful.")
                                return Player(login_username, login_password)

                    print("Invalid input detected, please try again.")


        elif choice_1.upper() == "C":
            while True:
                choice_3 = input("Are you sure you want to create an account? (Y/N): ")
                if choice_3.upper() == "N":
                    break
                if choice_3.upper() == "Y":
                    new_username = input("Please enter your new username: ")
                    new_password = input("Please enter your new password: ")
                    new_password_confirm = input("Please confirm your new password: ")
                    if validate(new_username) and validate(new_password) and new_password == new_password_confirm:
                        with open(LOGINS_FILE, 'a') as f:
                            f.write(f"\n{new_username} {new_password}")
                        print("Congratulations, account creation successful.")
                        return Player(new_username, new_password)
                    print("Invalid input detected, please try again.")

        elif choice_1.upper() == "E":
            print("[Exiting...]")
            quit()


while True:
    player_1 = login('one')
    player_2 = login('two')
    players = [player_1, player_2]
    player = player_1
    dice_game = Game()

    print("[Game starting...]")

    while True:
        print(f"[Round: {dice_game.round}]")
        if dice_game.round > 5 and player_1.score != player_2.score:
            winner = 'one' if player_1.score > player_2.score else 'two'
            print(f"[Game over, player {winner} wins!]\n[Final score: {player_1.score} - {player_2.score}]")

            with open(HIGH_SCORES_FILE, 'a') as f:
                f.write(f"\n{player_1.username} {player_1.score}\n{player_2.username} {player_2.score}")

            with open(HIGH_SCORES_FILE, 'r') as f:
                result = ""
                players_and_scores = f.read().split("\n")
                players_and_scores = sorted(players_and_scores, key=lambda score: int(score.split(' ')[1]),
                                            reverse=True)
                try:
                    if len(players_and_scores) >= 10:
                        for i in range(10):
                            result += f"[{i + 1} - {players_and_scores[i].split(' ')[0]}: " \
                                      f"{players_and_scores[i].split(' ')[1]}]\n"
                    else:
                        result = "[Sorry, there are not enough scores to show.]"
                except:
                    result = "[Error: scores could not be shown.]"

                print(f"[Highscores:]\n{result}")

            break

        while True:
            input(f"{player.username}'s turn, press return to roll: ")
            player.roll_1 = random.randint(1, 6)
            player.roll_2 = random.randint(1, 6)
            player.score += player.roll_1 + player.roll_2
            calcs = evaluate(player.roll_1, player.roll_2)
            if 'even' in calcs:
                player.score += 10
            else:
                player.score -= (5 * (player.score >= 5))

            print(f"[You rolled, a {player.roll_1}, and a {player.roll_2}, making your score {player.score}!]")
            if 'double' not in calcs:
                if player == player_2:
                    dice_game.round += 1

                player = players[int(not (players.index(player)))]
                break
            print("[You also rolled a double, meaning you get an additional roll!]")

    choice_4 = input("Do you want to play again or exit? (P/E): ")
    while True:
        if choice_4.upper() == "P":
            break

        elif choice_4.upper() == "E":
            print("[Exiting...]")
            quit()

# this is the main loop for the game, it repeats until five rounds have occured and one player has
# a score which is greater than the other
