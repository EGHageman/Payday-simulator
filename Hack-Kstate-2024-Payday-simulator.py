
#importing random for card drawing and dice rolling
#importing pysimlegui for a basic GUI
import random
import PySimpleGUI as sg

#last minute changes call for last minute solutions
#Changes all of the print statments to PySimpleGUI window prints
print = sg.Print

#The player class  used to create each model of a PayDay player 
#holding game items, cards (bills and deals), money, and location on the board
#as well as player stats: roll_ability and name.
class player:

    def __init__(self, name):
        self.name = name
        self.money = 3500
        self.deals = []
        self.bills = []
        self.month = 1
        self.board_location = 0
        self.debt = 0
        self.roll_ability = True

    #generates a random number from 1 to 6 in order to mimic one d6
    def roll(self):
        x = random.randint(1, 6)
        self.board_location += x
        return(x)
        
    #aquires a deal card (given from pick_deal method in the game class) if affordable
    #if not affordable, computes a potentially return on investment and takes loans if it looks ideal
    def get_deal(self, deal):
        if self.money > deal.price:
            self.money -= deal.price
            self.deals.append(deal)

        elif self.money - deal.price > (deal.price - deal.value):
            while self.money < deal.price:
                self.take_loan()
            self.money -= deal.price
            self.deals.append(deal)
    
    #If the player model has a deal card, sells it (removing from the hand and increaseing money by deal value)
    #If the player model has multiple deal cards, sells the one worth the highest value
    def sell_deal(self):
        largest_value = 1
        top_deal = None
        if not self.deals:
            print("however has nothing to sell")
            return
        for deal in self.deals:
            if deal.value > largest_value:
                largest_value = deal.value
                top_deal = deal
        self.money += top_deal.value
        print(f"{self.name}, made {largest_value} from {top_deal.name}")
        self.deals.remove(top_deal)

    #PayDay for when the player reaches the end of the month, increases month count, gives payday bonus, handles payment of bills and debt
    def payday(self):
        self.month += 1
        print(f"{self.name} is now on month {self.month}")
        self.money += 3250
        self.board_location = 0 #board location back to start
        for bill in self.bills:
            self.money -= bill
        if self.money > self.debt:
            self.money -= self.debt
            self.debt = 0
        else:
            self.money -= (self.debt * 0.10)

    def ending(self):
        self.money -= self.debt
        
    #gives the ability to take out debt, at 1k per loan note
    def take_loan(self):
        print(f"{self.name} took a lone")
        self.money += 1000
        self.debt += 1000
        
    #generates random mail from a pool, either a letter (essentially doing nothing) or a bill
    def get_mail(self, amount):
        mail_list = ["Greeting card from France", "Advertisment for window washing", "Advertisment for dogs", "Advertisment for cats", "pizza hut coupon",
                     "free snikers bar", 200, 300, 10, 20, 40, 50, 60, 70, 80, 90, 100, 500, 1000]
        for i in range(amount):
            card = random.choice(mail_list)
            if isinstance(card, int):
                self.bills.append(card)
                print(f"{self.name} got billed ${card}")
            else:
                print(f"{self.name}: {card}")

#The deal class, allowing for cards to be structured with a name, purchasing price and selling value
class deal:
    def __init__(self, name, price, value):
        self.name = name
        self.price = price
        self.value = value


#The PayDay game class, in charge of handling the model game components
#constructs a custom board array
#builds the deal deck, with a method to re shuffle the deck if the cards run out
#sets game length (max months) and the drawing of deal cards
class game:

    def __init__(self):
        self.board = [
                ["start"],["1-mail"],["inheritance"],["3-mail"],["deal"],["2-mail"],["weekend-company"],["sunday"],["suprise-bonus"],["buyer"],["bet"],["1-mail"],
                ["deal"],["school-dance"],["sunday"],["deal"],["3-mail"],["buyer"],["groceries"],["1-mail"],["buyer"],["sunday"],["1-mail"],["home-repairs"],
                ["2-mail"],["deal"],["home-repairs"],["buyer"],["sunday"],["1-letter"],["pay-day"]
        ]
        self.deals_deck = []
        self.roll_count = 0
        self.moth = 0 
        

    #Re-adds the cards back into the deal deck, ideally when the deck is empty
    def deal_shuffle(self):
        new_jeans = deal("new_jeans", 7000, 12000)
        hamburger_co = deal("hamburger_co", 8000, 15000)
        rad_skates = deal("rad_skates", 3000, 6000)
        computers_and_stuff = deal("computers_and_stuff", 4500, 10000)
        big_hotel = deal("big_hotel", 13500, 22000)
        cool_shoes = deal("cool_shoes", 2000, 5000)
        lemonade_stand = deal("lemonade_stand", 1500, 3500)
        pizza_hut = deal("pizza_hut", 6500, 11000)
        cool_hats = deal("cool_hats", 5000, 8000)
        pumpkin_patch = deal("pumpkin_patch", 800, 1500)
        coffee_stand = deal("coffee_stand", 3300, 4700 )


        self.deals_deck.append(new_jeans)
        self.deals_deck.append(hamburger_co)
        self.deals_deck.append(rad_skates)
        self.deals_deck.append(computers_and_stuff)
        self.deals_deck.append(big_hotel)
        self.deals_deck.append(cool_shoes)
        self.deals_deck.append(lemonade_stand)
        self.deals_deck.append(pizza_hut)
        self.deals_deck.append(cool_hats)
        self.deals_deck.append(pumpkin_patch)
        self.deals_deck.append(coffee_stand)

    #Draws deal cards when the player model lands on a deal square
    #Draws 3 cards, the model computes which card is the best, based on total return on investment
    #if there are not 3 cards available, chooses a random cardw (one of the 2)
    def pick_deal(self):
        temp_choice = []
        if len(self.deals_deck) > 3:
            for i in range(3):
                temp_choice.append(random.choice(self.deals_deck))
            total_value_1 = temp_choice[0].value - temp_choice[0].price
            total_value_2 = temp_choice[1].value - temp_choice[1].price
            total_value_3 = temp_choice[2].value - temp_choice[2].price
            choice = max(total_value_1, total_value_2, total_value_3)
            if choice == total_value_1:
                choice = temp_choice[0]
            if choice == total_value_2:
                choice = temp_choice[1]
            if choice == total_value_3:
                choice = temp_choice[2]
            self.deals_deck.remove(choice)
        else:
            choice = random.choice(self.deals_deck)
        return choice

#The main gameplay loop for running teh game
def main():
    game_on = True
    max_month = 6
    PayDay = game()
    char_select = True
    characters = []

    sg.theme("green")

    #Layout settings for the initial game start GUI, using the PySimpleGUI libary
    layout = [
        [sg.Text("Welcome to the PayDay simulater")],
        [sg.InputText(), sg.Button("Add"), sg.Button("Start")],
        [sg.Text("Enter the names of the players (above) and the months you want to play ->"), sg.Listbox([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], size=(10, 1), select_mode="single")]
    ]

    window = sg.Window("PayDay Simulation", layout)
    while True:
        months = None
        event, action = window.read()
        if event == sg.WIN_CLOSED or event == "Start":
            break
        if event == "Add":
            characters.append(player(action[0]))
            if not action[1]:
                max_month = 6
            else:
                max_month = action[1][0]
    window.close()
    remaining = len(characters)
    
    #While the game runs (game on == True) each player model takes a turn rolling the dice, then performing action(s) based on the board location
    print("Game Beginning")
    while game_on == True:
        for char in characters:
            if not PayDay.deals_deck:
                PayDay.deal_shuffle()
            if char.month == max_month:
                char.roll_ability = False
                char.board_position = -1
                char.ending()
                remaining -= 1
            
            #If the remaining players == 0 the game concludes, counting each model's final money count to decide a winner
            if remaining == 0:
                game_on = False
                print("\n")
                print("The game has concluded")
                winning_money = 0
                winning_char = None
                for char in characters:
                    print(f"{char.name}: ${char.money}")
                for char in characters:
                    if char.money > winning_money:
                        winning_money = char.money
                        winning_char = char
                print(f"{winning_char.name} wins with ${winning_char.money}", wait=True)

            
            #rolls the dice, if the model has not surpassed the allowed months
            if char.roll_ability == True:
                moves = char.roll()
                print(f"{char.name} has ${char.money}")
                print(f"Rolling for {char.name}: rolled a {moves}")
                PayDay.roll_count += 1

            #entering a new month
            if char.board_location > 30:
                print(f"its payday for {char.name}")
                char.payday()
            
            #The next 30 if statements are for the boards custom layout, per square

            if char.board_location == 2:
                char.get_mail(1)
            
            if char.board_location == 3:
                print(f"{char.name} got $500 in inheratence")
                char.money += 500

            if char.board_location == 4:
                char.get_mail(3)

            if char.board_location == 5:
                card = PayDay.pick_deal()
                char.get_deal(card)
                print(f"{char.name} got a deal, {card.name}, for {card.price}")

            if char.board_location == 6:
                char.get_mail(2)

            if char.board_location == 7:
                print(f"{char.name} aquired weekend visiters costing $50")
                char.money -= 50

            if char.board_location == 8:
                print(f"{char.name} is enjoying their sunday")

            if char.board_location == 9:
                print(f"{char.name} got a suprise $250 bonus")
                char.money += 250

            if char.board_location == 10:
                print(f"{char.name} found a buyer")
                char.sell_deal()

            if char.board_location == 11:
                x = random.choice(characters)
                print(f"{x.name} wone the loterry game, gaining $50")
                x.money += 50

            if char.board_location == 12:
                print(f"{char.name} got mail")
                char.get_mail(1)

            if char.board_location == 13:
                card = PayDay.pick_deal()
                char.get_deal(card)
                print(f"{char.name} got a deal, {card.name}, for {card.value}")

            if char.board_location == 14:
                print(f"{char.name} dance, -$50 for suit and tie rental")
                char.money -= 45

            if char.board_location == 15:
                print(f"{char.name} is enjoying their sunday")

            if char.board_location == 16:
                print(f"{char.name} got mail")
                char.get_mail(3)

            if char.board_location == 17:
                print(f"{char.name} found a buyer")
                char.sell_deal()

            if char.board_location == 18:
                print(f"{char.name} spent $50 on grociers")
                char.money -= 50

            if char.board_location == 19:
                print(f"{char.name} got mail")
                char.get_mail(1)

            if char.board_location == 20:
                print(f"{char.name} found a buyer")
                char.sell_deal()

            if char.board_location == 21:
                print(f"{char.name} relaxing on their sunday off")

            if char.board_location == 22:
                print(f"{char.name} got mail")
                char.get_mail(1) 

            if char.board_location == 23:
                print(f"{char.name} has to pay $125 for home repairs")
                char.money -= 125

            if char.board_location == 24:
                print(f"{char.name} got mail")
                char.get_mail(2)

            if char.board_location == 25:
                card = PayDay.pick_deal()
                char.get_deal(card)
                print(f"{char.name} got a deal, {card.name}, for ${card.price}")

            if char.board_location == 26:
                print(f"{char.name} has to pay $125 for home repairs")
                char.money -= 125 

            if char.board_location == 27:
                print(f"{char.name} found a buyer")
                char.sell_deal()

            if char.board_location == 28:
                print(f"{char.name} has the sunday off")

            if char.board_location == 29:
                print(f"{char.name} got mail")
                char.get_mail(2)

            if char.board_location == 30:
                print(f"its payday for {char.name}")
                char.payday()
        

if __name__ == "__main__":
    main() 

