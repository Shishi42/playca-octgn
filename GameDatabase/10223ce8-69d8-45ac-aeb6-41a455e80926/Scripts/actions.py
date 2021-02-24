import re

drawManyDefault = 3
placedLicense = 0

#SIMPLE ACTIONS#

def shuffle(group, x = 0, y = 0):
    mute()
    group.shuffle()
    notify("{} shuffles their {}.".format(me, group.name))

def draw(group, x = 0, y = 0):
    mute()
    if len(me.Deck) < 1:
        return
    card = me.Deck.top()
    card.moveTo(card.owner.hand)
    notify("{} draws a card from Deck.".format(me))
	
def drawMany(group, x = 0, y = 0):
	if len(me.Deck) < 1:
		return
	mute()
	global drawManyDefault
	count = askInteger("Draw how many cards ?", drawManyDefault)
	if count == None:
		return
	drawManyDefault = count
	for card in me.Deck.top(count):
		card.moveTo(card.owner.hand)
	notify("{} draws {} cards from Deck.".format(me, count))	
	
def discard(card, x = 0, y = 0):	
	mute()
	src = card.group.name
	card.moveTo(card.owner.Discard)
	notify("{} discards {} from {}.".format(me, card, src))
	
def shuffle(group, x = 0, y = 0):
    mute()
    group.shuffle()
    notify("{} shuffles {}.".format(me, group.name))	
	
def rotate(cards, x = 0, y = 0):
  mute()
  for card in cards:
      card.orientation ^= Rot90
      notify('{} turns {}.'.format(me, card))

#HAND ACTIONS#
		
def setCardFaceDown(card, x = 0, y = 0):
	mute()
	if me.isInverted == False:
		card.moveToTable(-38, 7, True)
	else:
		card.moveToTable(-38, -118, True)	
	card.isFaceUp = False
	card.peek()
	notify("{} sets a card face-down.".format(me))
	
def AllToDeck(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveTo(card.owner.Deck)
    notify("{} moves all cards from their {} to Deck.".format(me, group.name))	

#TABLE ACTIONS#

def toHand(card, x = 0, y = 0):
    mute()
    src = card.group
    if src == Table:
        notify("{} moves {} to hand from {}.".format(me, card, src.name))
    else:
        if card.isFaceUp == False:
            if confirm("Reveal to player ?"):
                card.isFaceUp = True
                cardname = card
            else:
                cardname = "a card"
        else:
            cardname = card
        notify("{} moves {} to hand from {}.".format(me, cardname, src.name))
    card.moveTo(card.owner.hand)

def rollDie(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided die.".format(me, n))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def flip(cards, x = 0, y = 0):
    mute()
    for card in cards:
        if card.isFaceUp == True:
          notify("{} flips {} face down.".format(me, card))
          card.isFaceUp = False
        else:
          card.isFaceUp = True
          notify("{} flips {} face up.".format(me, card))

def burningChance(cards, x = 0, y = 0):
	mute()
	for card in me.Deck.top(1):
		if me.isInverted == False:
			card.moveToTable(80, 6, True)
		else:
			card.moveToTable(-158, -118, True)	
		card.isFaceUp = True
		card.highlight = "#ffbb00" #orange#
		notify("{} Burning Chance to {} with {}.".format(me, card.BCP, card))		

def getBall(group, x = 0, y = 0):
	mute()
	if me.isInverted == False:
		cards = group.create('5ac345df-ce42-4d09-920a-9ce457d9cfb0', -195, 112, quantity = 1, persist = False)
	else:
		cards = group.create('5ac345df-ce42-4d09-920a-9ce457d9cfb0', 195, -112, quantity = 1, persist = False)
	notify("{} puts the ball on the table.".format(me))
	
def useTP(cards, x = 0, y = 0):
	mute()
	count = 0
	for card in cards:
		count += 1
		card.moveTo(card.owner.Discard)
		notify("{} uses {} as TP.".format(me, card))
	notify("{} uses a total of {} TP.".format(me, count))
	if confirm("Adjust your TP Counter ?"):
		me.tp -= count		

def toPass(card, x = 0, y = 0):
	mute()		
	card.moveTo(card.owner.Discard)
	notify("{} makes a pass with {}.".format(me, card))
	
def useEffect(card, x = 0, y = 0):
	mute()
	count = askInteger("Use the effect for how much TP ?", 0)
	if count == None:
		return	
	notify("{} uses the effect of {} for {} TP.".format(me, card, count))
	
def setAsTP(card, x = 0, y = 0):
	mute()
	if me.isInverted == False:
		card.moveToTable(-80, 240, True)
	else:
		card.moveToTable(2, -352, True)	
	card.isFaceUp = False		
	if confirm("Adjust your TP Counter ?"):
		me.tp += 1
		
def setAsScore(card, x = 0, y = 0):	
	mute()
	card.isFaceUp = False
	card.orientation ^= Rot90
	card.highlight = "#ffffff" #white#	
	notify("{} scores a goal !".format(me))		
	if me.isInverted == False:
		card.moveToTable(-340, -28, True)
	else:
		card.moveToTable(260, -84, True)
	if confirm("Adjust your Score Counter ?"):
		me.score += 1		

def licenseBurst(card, x = 0, y = 0):	
	mute()
	card.isFaceUp = False
	card.highlight = "#000000" #black#
	notify("{} License Bursts {}.".format(me, card))	
		
		
#DECK ACTIONS#

def addTPMany(cards, x = 0, y = 0):
	mute()
	if me.isInverted == False:
		x1 = -80
	else:
		x1 = 2
	count = askInteger("Add how many TP ?", 5)
	if count == None:
		return
	for card in me.Deck.top(count):
		if me.isInverted == False:
			card.moveToTable(x1, 238, True)
			x1 += 20
		else:
			card.moveToTable(x1, -350, True)	
			x1 -= 20
		card.isFaceUp = False
	notify("{} add {} TP.".format(me, count))
	if confirm("Adjust your TP Counter ?"):
		me.tp += count	
		
def putXtoDiscard(cards, x = 0, y = 0):
	mute()
	count = askInteger("Discard how many cards ?", 0)
	if count == None:
		return
	for card in me.Deck.top(count):
		card.moveTo(card.owner.Discard)
	notify("{} discards {} cards from Deck.".format(me, count))
	
#GOAL ACTIONS#

def setGoal(card, x = 0, y = 0):
	mute()
	if me.isInverted == False:
		card.moveToTable(-56, 155, True)
	else:
		card.moveToTable(-56, -234, True)
	card.isFaceUp = True
	card.highlight = "#0000ff" #blue#
	notify("{} sets {} as goalkeeper.".format(me, card))
	
#LICENSE ACTIONS#

def setLicense(card, x = 0, y = 0):
	mute()
	global placedLicense	
	if me.isInverted == False:
		if placedLicense == 3:
			whisper("You can't set more License Card")
		if placedLicense == 0:
			card.moveToTable(-350, 120, True)	
			card.isFaceUp = True
			card.highlight = "#ffff00" #yellow#
			notify("{} sets {} as Eleven License.".format(me, card))
			placedLicense += 1
		elif placedLicense == 1:
			card.moveToTable(-350, 198, True)
			card.isFaceUp = True
			card.highlight = "#ffff00" #yellow#
			notify("{} sets {} as Eleven License.".format(me, card))
			placedLicense += 1
		else:	
			card.moveToTable(-350, 276, True)
			card.isFaceUp = True
			card.highlight = "#ffff00" #yellow#
			notify("{} sets {} as Eleven License.".format(me, card))
			placedLicense += 1
	else:
		if placedLicense == 3:
			whisper("You can't set more License Card")
		if placedLicense == 0:
			card.moveToTable(236, -182, True)		
			card.isFaceUp = True
			card.highlight = "#ffff00" #yellow#
			notify("{} sets {} as Eleven License.".format(me, card))
			placedLicense += 1
		elif placedLicense == 1:
			card.moveToTable(236, -260, True)
			card.isFaceUp = True
			card.highlight = "#ffff00" #yellow#
			notify("{} sets {} as Eleven License.".format(me, card))
			placedLicense += 1
		else:
			card.moveToTable(236, -338, True)
			card.isFaceUp = True
			card.highlight = "#ffff00" #yellow#
			notify("{} sets {} as Eleven License.".format(me, card))
			placedLicense += 1

#HISSATSU ACTIONS#

def useHissatsu(card, x = 0, y = 0):
	mute()
	cardcost = int(card.HCost)
	count = askInteger("Use the hissatsu for how much TP ?", cardcost)
	if count == None:
		return
	if me.isInverted == False:
		card.moveToTable(-199, 7, True)
	else:
		card.moveToTable(86, -86, True)		
	card.isFaceUp = True
	card.highlight = "#ffbb00" #orange#	
	notify("{} uses {} as {} for {} TP.".format(me, card, card.SubType, count))
		
def toHissatsuArea(card, x = 0, y = 0):	
	mute()
	if me.isInverted == False:
		card.moveToTable(-199, 7, True)
		card.isFaceUp = True
	else:
		card.moveToTable(86, -86, True)	
		card.isFaceUp = True
	notify("{} puts {} in his or her Hissatsu Area.".format(me, card))