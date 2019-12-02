# cardcounting version
from __future__ import division
from random import shuffle

def sumCardsSoft(cardList):
  output = 0
  for card in cardList:
    if card is "2": output += 2
    if card is "3": output += 3
    if card is "4": output += 4
    if card is "5": output += 5
    if card is "6": output += 6
    if card is "7": output += 7
    if card is "8": output += 8
    if card is "9": output += 9
    if card is "10": output += 10
    if card in ["K", "Q", "J"]: output += 10
    if card is "A": output += 11 #count ace as 11
  return output

def sumCardsHard(cardList): #count ace as 1
  output = 0
  for card in cardList:
    if card is "2": output += 2
    if card is "3": output += 3
    if card is "4": output += 4
    if card is "5": output += 5
    if card is "6": output += 6
    if card is "7": output += 7
    if card is "8": output += 8
    if card is "9": output += 9
    if card is "10": output += 10
    if card in ["K", "Q", "J"]: output += 10
    if card is "A": output += 1
  return output

#"""
def createDeck(numberOfDecks):
  cards = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
  out = []
  for i in range(0, numberOfDecks):
    for j in range(0, len(cards)):
      for k in range(0, 4):
        out.append(cards[j])
  shuffle(out)
  return out
#"""

"""
def createDeck(numberOfDecks):
  return ["5","K","5","Q","10","J","K","5","4","7","K","7","K","5","4","4","A","10","6","J","4","J","9","9","8","9","A","Q","9","J","Q","10","6","J","7","6","K","8","Q","9","K","J","9","10","Q","K","Q","7","4","A","3","10","10","3","5","8","3","8","4","3","6","K","7","5","K","6","2","5","10","A","4","9","4","3","10","3","5","6","6","Q","5","10","6","2","Q","2","8","J","7","6","4","3","6","7","2","10","10","2","8","3","3","J","9","J","6","A","4","2","5","6","Q","6","7","5","3","7","2","2","A","10","A","5","5","2","10","7","9","6","6","3","8","9","K","Q","5","9","6","5","8","J","7","8","3","K","8","8","4","5","A","A","K","J","9","8","7","5","J","10","4","8","J","9","A","2","2","A","10","K","A","7","3","Q","3","2","K","7","6","10","10","2","7","7","Q","8","5","Q","Q","4","5","A","2","10","A","10","K","Q","2","Q","3","K","A","7","9","4","A","2","Q","A","J","9","6","9","2","2","9","3","5","3","9","3","K","A","8","10","2","J","3","8","K","K","5","J","9","5","J","6","J","Q","9","A","2","7","5","K","4","K","6","6","A","2","4","7","8","3","9","8","8","3","4","Q","6","8","4","10","J","A","J","2","A","10","2","K","8","K","7","J","J","Q","3","4","5","9","J","4","3","4","6","3","8","7","A","7","Q","2","Q","7","7","4","J","8","K","Q","Q","A","4","9","10","10","4","6","9","8"]
"""

class BlackJackRound:
  def __init__(self, deck, bet):
    def userFunc(uhs, dhu): pass
    self.bet = bet
    self.bet2 = 0
    self.bet3 = 0
    self.back = 0
    self.userFunc = userFunc
    self.dealerHandUp = []
    self.dealerHandDown = []
    self.userHands = [UserHand([])]
    self.deck = deck
    self.userHands[0].cards.append(self.deck.pop(0))
    self.userHands[0].cards.append(self.deck.pop(0))
    self.dealerHandUp.append(self.deck.pop(0))
    self.dealerHandDown.append(self.deck.pop(0))
  def runRound(self):
    numberOfSplits = 0
    outputs = []
    for hand in self.userHands:
      while True:
        if (sumCardsSoft(hand.cards) > 21):
          if (sumCardsHard(hand.cards) > 21):
            outputs.append(5)
            break

        current = self.userFunc(hand.cards, self.dealerHandUp, numberOfSplits)
        if (current is 0):
          outputs.append(current)
          break
        if (current is 3):
          self.back = self.bet / 2
          outputs.append(current)
          break
        if current is 2:
          if (len(self.userHands) is 1):
            self.back -= self.bet
            self.bet *= 2
          if (len(self.userHands) is 2):
            self.back -= self.bet2
            self.bet2 *= 2
          if (len(self.userHands) is 3):
            self.back -= self.bet3
            self.bet3 *= 2
          hand.cards.append(self.deck.pop(0))
          outputs.append(0)
          break
        if current is 1:
          hand.cards.append(self.deck.pop(0))
          continue
        if current is 4:
          numberOfSplits+=1
          self.userHands.append(UserHand([hand.cards.pop(0)]))
          if (len(self.userHands) is 2):
            self.bet2 = self.bet
            self.back -= self.bet2
          if (len(self.userHands) is 3):
            self.bet3 = self.bet
            self.back -= self.bet3


    self.dealerHandUp.append(self.dealerHandDown.pop(0))

    outputType = 0 #0: Loss-Dealer Higher, 1: Win-Dealer Busted, 2: Win-Dealer Lower, 3: Tie
    while True:
      dealerTotal = sumCardsSoft(self.dealerHandUp)
      if (dealerTotal > 21):
        dealerTotal = sumCardsHard(self.dealerHandUp)
        if (dealerTotal > 21):
          outputType = 1
          self.back += 2*self.bet
          return [self.back, outputs[0], outputType, self.userHands, self.dealerHandUp] # return value
      if (dealerTotal <= 17):
        self.dealerHandUp.append(self.deck.pop(0))
        continue
      elif (dealerTotal > 17 and dealerTotal <= 21):
        break
    values = [sumCardsHard(hand.cards) for hand in self.userHands]
    for (value, output) in zip(values, outputs):
      if output is 0:
        if value > dealerTotal:
          if outputType is 0: outputType = 2
          self.back += 2*self.bet
        elif value is dealerTotal:
          if outputType is 0: outputType = 3
          self.back += self.bet
    return [self.back, outputs[0], outputType, self.userHands, self.dealerHandUp] # return value

  def setUserFunc(self, func):
    self.userFunc = func


def myFunction(userHand, dealerHandUp):
  pass

lastId = 0
class UserHand:
  def __init__(self, cards, newID=-1):
    global lastId
    self.cards = cards
    if (newID is not -1):
      self.handId = newId
    else:
      self.handId = lastId
      lastId = lastId + 1
