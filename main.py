# NON cardcounting version
from __future__ import division
from blackjack import BlackJackRound, sumCardsSoft, sumCardsHard
from re import sub
import sys

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


# Start main program
print("Program start")
history = [[-1, initialMoney, "Start"]]

money = initialMoney
for i in range(0, iters):
  money -= bet
  round = BlackJackRound(6, bet)
  round.setUserFunc(userFunc)
  result = round.runRound()
  [back, output, outputType] = result
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
