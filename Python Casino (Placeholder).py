import json
import hashlib
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import sys

# SMTP server configuration
SMTP_SERVER = "YourSMTP.net"
SMTP_PORT = 000
SMTP_USE_TLS = True
SMTP_USERNAME = "Test@SMTP.com"
SMTP_PASSWORD = "SamplePassword"

def send_verification_code(email, verification_code):
    sender_email = SMTP_USERNAME
    receiver_email = email

    subject = "Email Verification Code"
    body = f"Your verification code is {verification_code}."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())

def send_password_reset_code(email, verification_code):
    sender_email = SMTP_USERNAME
    receiver_email = email

    subject = "Password Reset Code"
    body = f"Your password reset code is {verification_code}."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())

def reset_password(email):
    print("Sending Verification Email...")
    try:
        verification_code = str(random.randint(1000, 9999))
        send_password_reset_code(email, verification_code)
        print("Done!")
        user_input = input("Enter the password reset code sent to your email (Email might take a few minutes to be sent!): ")

        if user_input == verification_code:
            print("Password reset verified. You can now reset your password.")
            new_pwd = input("Enter new password: ")
            conf_pwd = input("Confirm new password: ")

            if conf_pwd == new_pwd:
                enc = new_pwd.encode()
                hash_val = hashlib.sha256(enc).hexdigest()

                with open("credentials.txt", "r") as f:
                    lines = f.read().splitlines()

                for i in range(0, len(lines), 2):
                    if lines[i] == email:
                        lines[i + 1] = hash_val

                with open("credentials.txt", "w") as f:
                    for i in range(0, len(lines), 2):
                        f.write(lines[i] + "\n")
                        f.write(lines[i + 1] + "\n")

                print("Password reset successful!")
            else:
                print("Passwords do not match! Password reset failed.")

        else:
            print("Password reset verification failed.")
    except Exception as e:
        print("Failed")
        print(f"An error occurred: {e}")

def email_verification(email):
    verification_code = str(random.randint(1000, 9999))
    print("Sending Verification Email...")
    send_verification_code(email, verification_code)
    print("Done!")
    user_input = input("Enter the verification code sent to your email: ")

    if user_input == verification_code:
        print("Email verified successfully!")
        return True
    else:
        print("Email verification failed.")
        return False

def send_message(email, subject, body):
    sender_email = SMTP_USERNAME
    receiver_email = email

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())

def create_message(sender, to, verification_code):
    body = f"Your verification code is {verification_code}."
    return sender, to, "Email Verification Code", body



def authenticate_with_smtp():
    try:
        # Create an SMTP connection
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            # Log in to the SMTP server
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            print("SMTP authentication successful.")
            return server  # Return the server instance for later use if needed

    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP authentication failed. Error: {e}")
        return None  # Return None to indicate authentication failure
    except Exception as e:
        print(f"An error occurred during SMTP authentication: {e}")
        return None


def signup(email):
    try:
        with open("credentials.txt", "r") as f:
            lines = f.read().splitlines()

        for i in range(0, len(lines), 2):
            if lines[i] == email:
                print("You are already registered")
                return 0

        if email_verification(email):
            pwd = input("Enter password: ")
            conf_pwd = input("Confirm password: ")

            if conf_pwd == pwd:
                enc = conf_pwd.encode()
                hash_val = hashlib.sha256(enc).hexdigest()

                with open("credentials.txt", "a") as f:
                    f.write(email + "\n")
                    f.write(hash_val + "\n")

                print("You have registered successfully!")
            else:
                print("Passwords do not match!\n")

        else:
            print("Email verification failed. Registration aborted.")

    except Exception as e:
        print("Failed!")
        print(f"An error occurred: {e}")

def login(email):
    try:
        pwd = input("Enter password: ")
        auth = pwd.encode()
        auth_hash = hashlib.sha256(auth).hexdigest()

        with open("credentials.txt", "r") as f:
            lines = f.read().splitlines()

        if len(lines) % 2 != 0:
            print("File is corrupted.")
            return

        for i in range(0, len(lines), 2):
            stored_email = lines[i]
            stored_pwd = lines[i + 1]
            if email == stored_email and auth_hash == stored_pwd:
                print("Logged in Successfully!")
                while True:
                    choice = menu()
                    if choice == '4':
                        break
                    if choice == '5':
                        break
                    elif choice == '1':
                        email = input("Enter your email address: ")
                        if email not in balances:
                            print("User not found. Please sign up first.")
                            continue
                        balance = roulette_game(balances[email])
                        balances[email] = balance
                        write_balances(balances)
                return

        print("Login failed!\n")
    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_balances():
    try:
        with open("balances.json", "r") as file:
            balances = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        balances = {}
    return balances

def write_balances(balances):
    with open("balances.json", "w") as file:
        json.dump(balances, file)

def spin_wheel():
    result_number = random.randint(0, 36)
    if result_number == 0:
        return result_number, "Green"
    elif result_number in red_numbers:
        return result_number, "Red"
    else:
        return result_number, "Black"

def display_result(result):
    result_number, result_color = result
    print(f"The ball landed on {result_number} - {result_color}")

def roulette_game(balance):
    while True:
        print("===== Welcome to Python Casino Roulette! =====")
        print("1) Play Roulette")
        print("2) Back to Main Menu")
        choice = int(input("Enter your choice: "))
        try:
            if choice == 1:
                while balance > 0:
                    print(f"Your current balance is {balance}.")
                    bet_type = input("Place your bet (number, color, or both): ").lower()
                    if bet_type not in ['number', 'color', 'both']:
                        print("Invalid bet type. Please choose 'number', 'color', or 'both'.")
                        continue
                    bet_amount = int(input("Enter your bet amount: "))
                    if bet_amount > balance:
                        print("Insufficient balance. Please place a bet within your balance.")
                        continue

                    if bet_type in ['number', 'both']:
                        selected_number = int(input("Choose a number between 0 and 36: "))
                        if selected_number not in range(0, 37):
                            print("Invalid number. Please choose a number between 0 and 36.")
                            continue

                    if bet_type in ['color', 'both']:
                        selected_color = input("Choose a color (red or black): ").lower()
                        if selected_color not in ['red', 'black']:
                            print("Invalid color. Please choose either 'red' or 'black'.")
                            continue

                    input("Press enter to spin the wheel...")
                    result = spin_wheel()
                    display_result(result)
                    result_number, result_color = result

                    if bet_type == 'number' and selected_number == result_number:
                        balance += 5 * bet_amount
                        print(f"Congratulations! You won {5 * bet_amount}. Your balance is now {balance}.")
                    elif bet_type == 'color' and selected_color == result_color.lower():
                        balance += 2 * bet_amount
                        print(f"Congratulations! You won {2 * bet_amount}. Your balance is now {balance}.")
                    elif bet_type == 'both' and selected_number == result_number and selected_color == result_color.lower():
                        balance += 10 * bet_amount
                        print(f"Congratulations! You won {10 * bet_amount}. Your balance is now {balance}.")
                    else:
                        balance -= bet_amount
                        print(f"Sorry, you lost {bet_amount}. Your balance is now {balance}.")

                    play_again = input("Do you want to play again? (yes or no): ")
                    if play_again.lower() != 'yes':
                        break

                print("Game over. Thank you for playing!")
                return balance
            elif choice == 2:
                break
            else:
                print("Invalid Input")
        except ValueError:
            print("Please enter a valid number.")

pocket_numbers = [i for i in range(37)]
red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black_numbers = [i for i in pocket_numbers if i not in red_numbers]


def slots(email, balances):
    while True:
        print(f"\n===== Welcome to Python Casino Slots! =====")
        print("1. Spin the Slots")
        print("2. Check Balance")
        print("3. Return to Main Menu")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                bet_amount = int(input("Enter your bet amount: "))
                if bet_amount > balances[email]:
                    print("Insufficient balance. Please place a bet within your balance.")
                    continue

                result = spin_slots()
                display_slots_result(result)
                balance_change = calculate_slots_payout(result, bet_amount)
                balances[email] += balance_change

                print(f"Your balance is now {balances[email]}")
            elif choice == 2:
                print(f"Your current balance is {balances[email]}")
            elif choice == 3:
                break
            else:
                print("Invalid Option!")

        except ValueError:
            print("Please enter a valid number.")

    return balances[email]


def spin_slots():
    symbols = ["Cherry", "Lemon", "Orange", "Plum", "Bell", "Bar", "Seven"]
    result = [random.choice(symbols) for _ in range(3)]
    return result


def display_slots_result(result):
    print("Slot Machine Result:")
    print(" | ".join(result))

def check_balance(balance):
    while True:
        try:
            bet_amount = float(input("Enter the amount you want to bet: $"))
            if bet_amount <= balance:
                return bet_amount
            else:
                print("Insufficient balance. Please enter a lower amount.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")



def calculate_slots_payout(result, bet_amount):
    payout_rules = {
        ("Cherry", "Cherry", "Cherry"): 5,
        ("Seven", "Seven", "Seven"): 10,
        ("Bar", "Bar", "Bar"): 20,
    }

    key = tuple(result)
    if key in payout_rules:
        payout_multiplier = payout_rules[key]
        payout = bet_amount * payout_multiplier
        print(f"Congratulations! You won {payout}.")
        return payout
    else:
        print("Sorry, you didn't win this time.")
        return -bet_amount


def play_crash(balance):
    while True:
        print("\n===== Welcome to Python Casino Crash! =====")
        print("1) Play Crash")
        print("2) Return to Main Menu")
        choice = int(input("Enter you choice: "))
        if choice == 1:
            bet_amount = check_balance(balance)

            print("The game is starting...")

            crash_multiplier = 1.0
            crash_interval = random.uniform(5, 20)
            elapsed_time = 0

            while True:
                time.sleep(1)
                elapsed_time += 1
                crash_multiplier += 0.1

                print(f"Current multiplier: {crash_multiplier:.2f}")

                if elapsed_time >= crash_interval:
                    print(f"Crash event! The game crashed at {crash_multiplier:.2f}x!")
                    print("Sorry, you lost the bet.")
                    return balance - bet_amount

                cash_out_input = input("Do you want to cash out? (Y)es or (N)o: ").lower()
                if cash_out_input[0] == 'y':
                    winnings = bet_amount * crash_multiplier
                    print(f"Congratulations! You cashed out at {crash_multiplier:.2f}x. You won {winnings}.")
                    return balance + winnings

        elif choice == 2:
            break
        else:
            print("Invalid choice")

def blackjack_game(balance):
    while True:
        print("===== Welcome to Python Casino Blackjack! =====")
        print("1) Play Blackjack")
        print("2) Back to Main Menu")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            while True:
                bet_amount = get_bet_amount(balance)

                ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
                suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                deck = [{'rank': rank, 'suit': suit, 'value': 11 if rank == 'A' else 10 if rank in ['K', 'Q', 'J'] else int(rank)} for rank in ranks for suit in suits]

                random.shuffle(deck)

                player_hand = [deck.pop(), deck.pop()]
                dealer_hand = [deck.pop(), deck.pop()]

                print(f"Your hand: {display_hand(player_hand)}")
                print(f"Dealer's hand: {display_hand([dealer_hand[0], {}])}")

                while True:
                    player_value = calculate_hand_value(player_hand)
                    print(f"Your current hand value: {player_value}")

                    if player_value == 21:
                        print("Blackjack! You win.")
                        balance += bet_amount * 1.5
                        break

                    action = input("Do you want to (H)it or (S)tand? ").lower()
                    if action[0] == 'h':
                        player_hand.append(deck.pop())
                        print(f"Your hand: {display_hand(player_hand)}")
                        if calculate_hand_value(player_hand) > 21:
                            print("Bust! You lose.")
                            balance -= bet_amount
                            break
                    elif action[0] == 's':
                        break
                    else:
                        print("Invalid action. Please enter 'hit' or 'stand'.")

                print(f"\nDealer's turn:")
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                    print(f"Dealer's hand: {display_hand(dealer_hand)}")

                player_value = calculate_hand_value(player_hand)
                dealer_value = calculate_hand_value(dealer_hand)

                print(f"\nYour hand: {display_hand(player_hand)} ({player_value})")
                print(f"Dealer's hand: {display_hand(dealer_hand)} ({dealer_value})")

                if player_value > 21:
                    print(f"Bust! You lose {bet_amount}.")
                    balance -= bet_amount
                elif dealer_value > 21:
                    print(f"Dealer busts! You win {bet_amount}.")
                    balance += bet_amount
                elif player_value > dealer_value:
                    print(f"You win! {bet_amount} has been added to your account!")
                    balance += bet_amount
                elif player_value < dealer_value:
                    print(f"Dealer wins! You lose {bet_amount}.")
                    balance -= bet_amount
                else:
                    print("It's a push! No one wins.")

                play_again = input("Do you want to play again? (yes or no): ").lower()
                if play_again != 'yes':
                    break
        elif choice == 2:
            break
        else:
            print("Invalid Choice")

    return balance

def get_bet_amount(balance):
    while True:
        try:
            bet_amount = float(input(f"Enter your bet amount (current balance: {balance}): $"))
            if 0 < bet_amount <= balance:
                return bet_amount
            else:
                print("Invalid bet amount. Please enter a valid amount within your balance.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

def calculate_win_multiplier(player_hand):
    if calculate_hand_value(player_hand) == 21 and len(player_hand) == 2:
        return 1.5
    else:
        return 2


def display_hand(hand):
    return ', '.join([f"{card['rank']} of {card['suit']}" if card else "Unknown Card" for card in hand])


def calculate_hand_value(hand):
    value = 0
    num_aces = 0

    for card in hand:
        rank = card['rank']
        if rank == 'A':
            value += 11
            num_aces += 1
        elif rank in ['K', 'Q', 'J']:
            value += 10
        else:
            value += int(rank)

    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1

    return value



def display_plinko_board(board, ball_positions):
    for i, row in enumerate(board):
        print("+---" * len(row) + "+")
        for j, cell in enumerate(row):
            if i < len(ball_positions) and j == ball_positions[i]:
                print(f"| ◉ ", end="")
            else:
                cell_content = cell if cell is not None else " "
                print(f"| {cell_content} ", end="")
        print("|")

    print("+---" * len(board[-1]) + "+")
    time.sleep(0.5)  # Adjust sleep duration for visual effect

def plinko_game(balance):
    while True:
        print("\n===== Welcome to Python Casino Plinko! =====")
        print("1) Play Plinko")
        print("2) Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                bet_amount = get_bet_amount(balance)

                # Define the Plinko board with specified multipliers only on the bottom row
                plinko_board = [
                    [None, None, None, None, None, None, None, None, None, None],  # Row 1 (empty spaces)
                    [None, None, None, None, None, None, None, None, None, None],  # Row 2 (empty spaces)
                    [None, None, None, None, None, None, None, None, None, None],  # Row 3 (empty spaces)
                    [None, None, None, None, None, None, None, None, None, None],  # Row 4 (empty spaces)
                    [None, None, None, None, None, None, None, None, None, None],  # Row 5 (empty spaces)
                    [2, None, None, 5, None, None, 2, 3, 2, None]  # Updated bottom row multipliers
                ]

                # User chooses the starting position
                start_position = int(input(f"Choose the starting position (0 to {len(plinko_board[0]) - 1}): "))

                # Initialize ball positions for each row
                ball_positions = [start_position]

                # Calculate the final position based on accumulated random movements
                for i in range(len(plinko_board) - 1):
                    move = random.choice([-1, 1])
                    next_position = max(0, min(ball_positions[-1] + move, len(plinko_board[-1]) - 1))
                    ball_positions.append(next_position)

                    # Display Plinko board with ball movement for each step
                    display_plinko_board(plinko_board, ball_positions)

                # The final result is the multiplier of the selected slot from the bottom row
                result = plinko_board[-1][ball_positions[-1]]
                print("\nBall dropped to the bottom!")

                if result is None:
                    print(f"The ball landed on an empty space at the bottom. You lost {bet_amount}.")
                    balance -= bet_amount
                else:
                    print(f"Plinko Result: You won {result} times your bet!")

                    # Calculate winnings based on the result
                    winnings = bet_amount * result
                    print(f"You won {winnings}!")
                    balance += winnings
                choice = input("Would you like to play again? (Y)es or (N)o: ").lower()
                if choice == 'y':
                    continue
                elif choice == 'n':
                    break
                else:
                    print("Invalid Choice")

        elif choice == '2':
            return balance
            break

        return balance
def menu():
    while True:
        print("\n$$$$$ Welcome to Python Casino! $$$$$"
              "\n1) Roulette"
              "\n2) Slots"
              "\n3) Crash"
              "\n4) Black Jack"
              "\n5) Plinko"
              "\n6) Exit")
        user_input = input("What would you like to do?: ")

        if user_input == '1':
            email = input("Enter your email address: ")
            if email not in balances:
                print("User not found. Please sign up first.")
            else:
                balance = roulette_game(balances[email])
                balances[email] = balance
                write_balances(balances)
        elif user_input == '2':
            email = input("Enter your email address: ")
            if email not in balances:
                print("User not found. Please sign up first.")
            else:
                balance = slots(email, balances)
                balances[email] = balance
                write_balances(balances)
        elif user_input == '3':
            email = input("Enter your email address: ")
            if email not in balances:
                print("User not found. Please sign up first.")
            else:
                balance = play_crash(balances[email])
                balances[email] = balance
                write_balances(balances)
        elif user_input == '4':
            email = input("Enter your email address: ")
            if email not in balances:
                print("User not found. Please sign up first.")
            else:
                balance = blackjack_game(balances[email])
                balances[email] = balance
                write_balances(balances)
        elif user_input == '5':
            email = input("Enter your email address: ")
            if email not in balances:
                print("User not found. Please sign up first.")
            else:
                balance = plinko_game(balances[email])
                balances[email] = balance
                write_balances(balances)
        elif user_input == '6':
            print("Exiting the program. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    verification_code = ''
    balances = read_balances()
    pocket_numbers = [i for i in range(37)]
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [i for i in pocket_numbers if i not in red_numbers]

    if __name__ == "__main__":
        while True:
            print("\n---------- Secure Login System ----------")
            print("1. Signup")
            print("2. Login")
            print("3. Forgot Password")
            print("4. Exit")

            try:
                ch = int(input("Enter your choice: "))
                if ch == 1:
                    email = input("Enter your email address: ")
                    signup(email)
                    if email not in balances:
                        balances[email] = 100  # initial balance for the player
                        write_balances(balances)

                elif ch == 2:
                    email = input("Enter your email address: ")
                    login(email)
                    if email not in balances:
                        balances[email] = 100  # initial balance for the player
                        write_balances(balances)
                elif ch == 3:
                    email = input("Enter your email address: ")
                    reset_password(email)
                elif ch == 4:
                    print("Exiting the program. Goodbye!")
                    sys.exit()
                else:
                    print("Invalid Option!")
            except ValueError:
                print("Please enter a number choice.")
            except Exception as e:
                print(f"An error occurred: {e}")