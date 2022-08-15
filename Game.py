#  Game class

import pygwidgets
import pyghelpers
from Constants import *
from Deck import *
from Card import *

class Game():
    CARD_OFFSET = 110
    DEALER_CARDS_TOP = 50
    PLAYER_CARDS_TOP = 350
    CARDS_LEFT = 75
    NCARDS = 8

    def __init__(self, window):
        self.window = window
        self.oDeck = Deck(self.window)
        self.playerScore = 0
        self.dealerScore = 0

        self.dealerScoreText = pygwidgets.DisplayText(window, (420, 250),
                                   "Dealer's Score: " + str(self.dealerScore),
                                    fontSize=36, textColor=WHITE,
                                    justified='right')

        self.playerScoreText = pygwidgets.DisplayText(window, (420, 300),
                                   "Player's Score: " + str(self.playerScore),
                                    fontSize=36, textColor=WHITE,
                                    justified='right')

        self.messageText = pygwidgets.DisplayText(window, (50, 480),
                                    '', width=900, justified='center',
                                    fontSize=36, textColor=WHITE)

        self.loserSound = pygame.mixer.Sound("sounds/loser.wav")
        self.winnerSound = pygame.mixer.Sound("sounds/ding.wav")
        self.cardShuffleSound = pygame.mixer.Sound("sounds/cardShuffle.wav")

        self.cardXPositionsList = []
        thisLeft = Game.CARDS_LEFT
        # Calculate the x positions of all cards, once
        for cardNum in range(Game.NCARDS):
            self.cardXPositionsList.append(thisLeft)
            thisLeft = thisLeft + Game.CARD_OFFSET

        self.reset()  # start a round of the game

    def reset(self):  # this method is called when a new round starts        
        self.playerScore = 0
        self.dealerScore = 0
        self.cardShuffleSound.play()
        self.playerCardList = []
        self.oDeck.shuffle()
        for cardIndex in range(0, Game.NCARDS):  # deal out cards
            oCard = self.oDeck.getCard()
            self.playerCardList.append(oCard)
            thisXPosition = self.cardXPositionsList[cardIndex]
            oCard.setLoc((thisXPosition, Game.PLAYER_CARDS_TOP))

        self.dealerCardList = []
        for cardIndex in range(0, Game.NCARDS):  # deal out cards
            oDealerCard = self.oDeck.getCard()
            self.dealerCardList.append(oDealerCard)
            thisXPosition = self.cardXPositionsList[cardIndex]
            oDealerCard.setLoc((thisXPosition, Game.DEALER_CARDS_TOP))

            

        self.showCard(0)
        self.cardNumber = 0
        self.updatePlayerScore(self.cardNumber)
        
        # For the dealer, the Ace value will always be 11. That's why we don't invoke the Rank function.
        self.showDealerCard(0)
        self.dealerCardNumber = 0
        self.updateDealerScore(self.dealerCardNumber)

        self.dealerScoreText.setValue("Dealer's Score: " + str(self.dealerScore))
        self.playerScoreText.setValue("Player's Score: " + str(self.playerScore))

        self.messageText.setValue("Do you want another card? Click on Hit. If you don't, click on Stand")

    def getCardNameAndValue(self, index):
        oCard = self.playerCardList[index]
        theName = oCard.getName()
        theValue = oCard.getValue()
        return theName, theValue

    def getDealerCardNameAndValue(self, index):
        oDealerCard = self.dealerCardList[index]
        theDEName = oDealerCard.getName()
        theDEValue = oDealerCard.getValue()
        return theDEName, theDEValue

    def getCardRank(self, index):
        oCard = self.playerCardList[index]
        theRank = oCard.getRank()
        return theRank


    def showCard(self, index):
        oCard = self.playerCardList[index]
        oCard.reveal()

    def showDealerCard(self, index):
        oDealerCard = self.dealerCardList[index]
        oDealerCard.reveal()

    def updatePlayerScore(self, cardNumber):
            cardRank = self.getCardRank(cardNumber)
            if cardRank == 'Ace':
                self.aceValueButton = pyghelpers.textYesNoDialog(self.window, (10, 110, 400, 200),
                                            'Your drawn card is an Ace, choose its value.', 
                                            yesButtonText='11',
                                            noButtonText='1',
                                            backgroundColor=(0, 128, 0))

                aceValue = self.aceValueButton
                if aceValue:
                    self.playerScore = self.playerScore + 11
                    return self.playerScore
                else:
                    self.playerScore = self.playerScore + 1
                    return self.playerScore

            else:

                nextCardName, nextCardValue = self.getCardNameAndValue(cardNumber)
                self.playerScore = self.playerScore + nextCardValue
                return self.playerScore

    
    def updateDealerScore(self, dealerCardNumber):

        nextDealerCardName, nextDealerCardValue = self.getDealerCardNameAndValue(
                                                        dealerCardNumber)                                                                          
        self.dealerScore = self.dealerScore + nextDealerCardValue
        return self.dealerScore

   
    def hitOrStand(self, hitOrStand):

        if hitOrStand == HIT:
  
            if  self.dealerScore <= 16: 
                # Only show another card if score is less than or equal to 16
                self.dealerCardNumber = self.dealerCardNumber + 1
                self.showDealerCard(self.dealerCardNumber)
                self.updateDealerScore(self.dealerCardNumber)

            else:
                self.dealerScore = self.dealerScore

               
            # Only show another card if you click on Hit
            self.cardNumber = self.cardNumber + 1
            self.showCard(self.cardNumber)
            self.updatePlayerScore(self.cardNumber)
            
            self.dealerScoreText.setValue("Dealer's Score: " + str(self.dealerScore))
            self.playerScoreText.setValue("Player's Score: " + str(self.playerScore))

            if self.playerScore == 21:
                self.messageText.setValue('You won. Congrats.')
                self.winnerSound.play()
                return True

            # I chose this format instead of 'z < x < y' because it improves clarity.
            elif (self.playerScore > 21) and (self.dealerScore <= 21):
                self.dealerScore <= 21 < self.playerScore
                self.messageText.setValue('You lost, kek')
                self.loserSound.play()
                return True

            elif (self.playerScore > 21) and (self.dealerScore > 21):
                self.messageText.setValue('Tie.')
                self.loserSound.play()
                return True

            elif (self.playerScore < 21) and (self.dealerScore > 21):
                self.messageText.setValue('You win')
                self.winnerSound.play()
                return True

            elif (self.dealerScore == 21) and (self.playerScore < 21):
                self.messageText.setValue('You will lose if you stand. Click on hit and you can still tie.')
                return False

            elif (self.dealerScore == 21) and (self.playerScore == 21):
                self.messageText.setValue('Tie.')
                return True

        if hitOrStand == STAND:  # user hit the Stand button

            while  (self.dealerScore <= 16) and (self.playerScore > self.dealerScore): 
                # Only show another card if score is less than or equal to 16
                self.dealerCardNumber = self.dealerCardNumber + 1
                self.showDealerCard(self.dealerCardNumber)
                self.updateDealerScore(self.dealerCardNumber)


            self.dealerScoreText.setValue("Dealer's Score: " + str(self.dealerScore))
            self.playerScoreText.setValue("Player's Score: " + str(self.playerScore))

            if (self.playerScore < 21) and (self.dealerScore < 21):

                if self.playerScore > self.dealerScore:
                    self.messageText.setValue('You win')                   
                    self.winnerSound.play()

                if self.playerScore < self.dealerScore: 
                    self.messageText.setValue('You lost against the dealer. Try again.')
                    self.loserSound.play()

                if self.playerScore == self.dealerScore: 
                    self.messageText.setValue('Tie. Try again.')

            
            #if both are > than 21, that's being dealt with in HIT

            elif (self.playerScore < 21) and (self.dealerScore > 21):

                self.messageText.setValue('You win')                   
                self.winnerSound.play()

            elif (self.dealerScore == 21) and (self.playerScore < 21):
                self.messageText.setValue('You lose.')                   
                self.loserSound.play()


            done = True
            return done

     
    def draw(self):
        # Tell each card to draw itself
        for oCard in self.playerCardList:
            oCard.draw()

        for oDealerCard in self.dealerCardList:
            oDealerCard.draw()

        self.dealerScoreText.draw()
        self.playerScoreText.draw()
        self.messageText.draw()

''' Notes:

 Too many elifs. I could've put them all on a dictionary, but that would have requiered
a nested dictionary, which would have worsened the already affected readability. 

 I'm aware the elifs can be written in a < b < c format. I think this worsens the clarity 
 in this case. 

'''



