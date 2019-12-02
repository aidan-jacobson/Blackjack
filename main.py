# cardcounting version
from __future__ import division
from blackjack import BlackJackRound, sumCardsSoft, sumCardsHard, createDeck
from re import sub
import sys
def getCardValue(card):
  if (card is "2"): return 1
  if (card is "3"): return 1
  if (card is "4"): return 1
  if (card is "5"): return 1
  if (card is "6"): return 1
  if (card is "7"): return 0
  if (card is "8"): return 0
  if (card is "9"): return 0
  if (card is "10"): return -1
  if (card is "J" or card is "Q" or card is "K" or card is "A"): return -1

softTotals = [
  [1, 1, 1, 2, 2, 1, 1, 1, 1, 1], #13
  [1, 1, 1, 2, 2, 1, 1, 1, 1, 1],
  [1, 1, 2, 2, 2, 1, 1, 1, 1, 1],
  [1, 1, 2, 2, 2, 1, 1, 1, 1, 1],
  [1, 2, 2, 2, 2, 1, 1, 1, 1, 1], #17
  [2, 2, 2, 2, 2, 0, 0, 1, 1, 1],
  [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  #21
  ]

hardTotals = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #4
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #8
  [1, 2, 2, 2, 2, 1, 1, 1, 1, 1],
  [2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
  [1, 1, 0, 0, 0, 1, 1, 1, 1, 1], #12
  [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0, 1, 1, 1, 3, 1],
  [0, 0, 0, 0, 0, 1, 1, 3, 3, 3], #16
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #20
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]

splits = [
  [4, 4, 4, 4, 4, 4, 1, 1, 1, 1], #2
  [4, 4, 4, 4, 4, 4, 1, 1, 1, 1],
  [1, 1, 1, 4, 4, 1, 1, 1, 1, 1],
  [2, 2, 2, 2, 2, 2, 2, 2, 1, 1], #5
  [4, 4, 4, 4, 4, 1, 1, 1, 1, 1],
  [4, 4, 4, 4, 4, 4, 1, 1, 1, 1],
  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], #8
  [4, 4, 4, 4, 4, 0, 4, 4, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], #11
  ]

def userFunc(userHand, dealerHand, numberOfSplits):
  total = sumCardsSoft(userHand)
  dealerCard = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"].index(sub(r"[KQJ]", "10", dealerHand[0]))
  output = 0
  if (len(userHand) is 2 and userHand[0] is userHand[1]):
    if (numberOfSplits < 3):
      #if (total > 21): total -= 10*userHand.count("A")
      output = splits[int(total/2)-2][dealerCard]
      return output

  if "A" in userHand and not numberOfSplits >= 3:
    if (total > 21): total -= 10*userHand.count("A")
    output = softTotals[total-13][dealerCard]
  else:
    if (total > 21): total -= 10*userHand.count("A")
    output = hardTotals[total-4][dealerCard]
  return output


# Parameters
filename = sys.argv[1]
initialMoney = 5000
bet = 5
iters = 10000
breakWhenBroke = False
numberOfDecks = 6
reshuffleThreshold = 0.15

def getBet(trueCount):
  if (trueCount < -2):
    return 5
  if (trueCount >= -2 and trueCount < -1):
    return 5
  if (trueCount >= -1 and trueCount < 0):
    return 5
  if (trueCount >= 0 and trueCount < 1):
    return 5
  if (trueCount >= 1 and trueCount < 2):
    return 10
  if (trueCount >= 2 and trueCount < 3):
    return 20
  if (trueCount >= 3 and trueCount < 4):
    return 30
  if (trueCount >= 4 and trueCount < 5):
    return 40
  if (trueCount >= 5 and trueCount < 6):
    return 50
  if (trueCount >= 6):
    return 60


# Start main program
print("Program start")
history = [[-1, initialMoney, "Start"]]

deck = createDeck(numberOfDecks)
startingAmt = len(deck)
money = initialMoney
trueCount = 0
for i in range(0, iters):
  money -= bet
  round = BlackJackRound(deck, bet)
  round.setUserFunc(userFunc)
  result = round.runRound()
  [back, output, outputType, userHands, dealerHand] = result
  runningCount = 0
  outhand = []
  for hand in userHands:
    for card in hand.cards:
      runningCount += getCardValue(card)
      outhand.append(card)
  for card in dealerHand:
    runningCount += getCardValue(card)
    outhand.append(card)
  trueCount += runningCount / numberOfDecks
  bet = getBet(trueCount)
  #if (i < 100):
    #print("Truecount: {}, Bet: {}, Cards: {}".format(trueCount, bet, ",".join(outhand)))
  if (len(deck) < reshuffleThreshold*startingAmt):
    print("Deck reshuffle: {}, len: {}, sa: {}".format(i+1, len(deck), startingAmt))
    deck = createDeck(numberOfDecks)
    trueCount = 0

  money += back
  history.append([i, money, ["Loss: Dealer Higher", "Win: Dealer Busted", "Win: Dealer Lower", "Tie: Dealer Equal"][outputType]])
  if (money < bet and breakWhenBroke):
    print("User went broke on round {}, terminating...".format(i+1))
    history.append(["", "", ""])
    history.append([i, "Broke", ""])
    break;
print("{}/{} rounds finished".format(i+1,iters))
file = open(filename, "w+")
file.write("Iteration,Balance,Output Type\n")
for [i, balance, outputType] in history:
  if i is "":
    file.write(",\n")
  elif  i is -1:
    file.write("{},{},{},,Remaining Money:,${}\n".format(i+1, balance, outputType, money))
  elif i is 0:
    file.write("{},{},{},,Total Profit:,${}\n".format(i+1, balance, outputType, money-initialMoney))
  elif i is 1:
    file.write("{},{},{},,Percent Profit:,{}%\n".format(i+1, balance, outputType, int((money-initialMoney)/initialMoney*100)))
  else:
    file.write("{},{},{}\n".format(i+1, balance, outputType))
file.close()
print("{} written".format(filename))
print("")
print("===============")
print("  Quick data:")
print("===============")
print("Remaining money: ${}".format(money))
print("Profit: ${}".format(money-initialMoney))
print("Percent profit: {}%".format(int((money-initialMoney)/initialMoney*100)))
print(createDeck(1))
