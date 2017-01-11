import random
from itertools import cycle, islice

#initial player balance
playerBalance = 1000

#face cards
Q = 10
J = 10
K = 10
#ace depends on the total card value
A = None


class Cards:
    cardsVariety = [2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A]
    #initially the shoe(the box which holds the cards) is empty
    totalCards = []

    #cycle through the same array(cardsVariety) 208 times(4 decks of cards)
    s1 = islice(cycle(cardsVariety), 0, None)
    for k in range(208):
        x = next(s1)

        #insert the cards into the shoe
        totalCards.insert(k, x)

    @staticmethod
    def serveCards(pCardList):

        #dealer picks a random card from the shoe
        randomCard = random.choice(Cards.totalCards)
        if randomCard == J:
            return 10
        elif randomCard == Q:
            return 10
        elif randomCard == K:
            return 10
        elif randomCard == A:
            #we need to decide what should be the value of ace
            outcome = Rules.checkAce(randomCard, pCardList)
            return outcome
        else:
            return randomCard

class Rules:
    # pass

    @staticmethod
    def checkRulesForPlayer(pCardList, dCardList):
        global playerBalance
        #Black jack occus when you have an ace and a 10
        if len(pCardList) == 2 and sum(pCardList) == 21:
            print("BlackJack!")
            print("Player Wins!")
            #you get a payout of 1.5 times in case of Blackjack
            playerBalance = playerBalance + (2 * currentBet) + 30
            print("PlayerBalance:", playerBalance)
            return True
        else:
            #if not a Blackjack keep playing
            return Rules.hitOrStand(pCardList, dCardList)


   #in case a split occurs
    @staticmethod
    def split():
        signal = input("Do you want to split?(S/NS)")
        if signal == "S":
            return True
        else:
            return False

    @staticmethod
    def hitOrStand(pCardList, dCardList):

        global playerBalance
        global currentBet
        # while(True):

        move = input("\nDo you want to hit or stand?(H/S)")
        if move == "H":
            #player gets a card from the dealer
            pCard1 = card.serveCards(pCardList)
            pCardList.append(pCard1)
            print("Player Card Total:", sum(pCardList))
            if sum(pCardList) > 21:
                print("Player Busts!")
                currentBet = 0
                return False
            if sum(pCardList) == 21:
                #check for the type of payout a player will receive
                Rules.payout(pCardList)
                return True

            #player goes for another hit or stand
            #below is a recursive function
            return Rules.hitOrStand(pCardList, dCardList)

        else:
            #dealer keeps dealing cards for himself unless a constraint occurs
            while (True):
                dCard1 = card.serveCards(dCardList)
                dCardList.append(dCard1)

                if sum(dCardList) > 21:
                    print("Dealer Busts! ")
                    #check payout for the player
                    Rules.payout(pCardList)
                    return True
                elif sum(dCardList) > sum(pCardList):
                    print("Player loose")
                    currentBet = 0
                    return False

    @staticmethod
    def payout(pCardList):
        global playerBalance
        global currentBet

        print("\nPlayer Wins!")
        #player gets it bet back
        playerBalance = playerBalance + currentBet*2
        print("Player's Balance:", playerBalance)

    @staticmethod
    def checkAce(randCard, pCardList):
        #at the start of the game,the value of ace can be 11
        if pCardList == []:
            return 11

        #value of ace can be 11 since the total amount cannot go beyond 21 ie bust
        elif sum(pCardList) <= 10:
            return 11

        else:
            #value of ace will be 1
            return 1


#player or dealer object
card = Cards()

#reset function will clear the pCardList leaving the first card after one hand is lost in case of split
#so it can be reused for the other hand
def reset(pCardList, index):
    for i in range(index, len(pCardList)):
        pCardList[i] = 0


#we create a main function from where  the game will start
def main():
    global playerBalance
    global currentBet

    #initially the player's card and the dealer's card is empty
    pCardList = []
    dCardList = []

    while(True):
        playerBet = int(input("Please enter your bet: "))
        if(playerBet>playerBalance):
            print("Please enter a valid bet.\n")
        else:
            currentBet = playerBet
            break

    #you pay an amount to start playing
    playerBalance = playerBalance - currentBet
    print("Player Balance:", playerBalance)

    # Dealer serves cards to player
    pCard1 = card.serveCards(pCardList)
    pCard2 = card.serveCards(pCardList)
    pCardList.append(pCard1)
    pCardList.append(pCard2)

    # Dealer serves cards to himself
    dCard1 = card.serveCards(dCardList)
    dCard2 = card.serveCards(dCardList)
    dCardList.append(dCard1)
    dCardList.append(dCard2)

    # show dealer's first card only
    print("Dealer:", dCardList[0],"*")

    # show player's cards
    print("Player:", end=" ")
    for i in pCardList:
        print(i, end=" ")

    #if the first two cards are same ie a split occurs
    if pCard1 == pCard2:
        if Rules.split() == True:
            #we are going to use the same pCardList,so in each hand you have one such cards
            pCardList.remove(pCard1)
            if Rules.checkRulesForPlayer(pCardList, dCardList) == True:
                #game ends
                return
            else:
                #since the player lost one hand and now he will try the other hand
                reset(pCardList, 1)

    #check rules for the present hand
    Rules.checkRulesForPlayer(pCardList, dCardList)



main()
