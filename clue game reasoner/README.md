# Clue Game Reasoner

---

## 1. Background

### 1.1 The Game of Clue

We are going to use propositional logic to represent information needed to help solve a game of clue

The game has had many versions of its rules over the years, and we will use the rules, rooms, characters and items from the 1960 through 1996 editions. Apologies if you learned a different edition

If you aren't familiar with the game, don't worry! It has some simple stochastic elements (that we will ignore) but the main basis of the game is deduction: Someone has committed a murder, and our job is to find out who committed it, in what room, and with which weapon.

In each game of clue, there is a deck of cards. On each card is either a suspect, a weapon or a room. There are six suspects, six weapons, and nine rooms for a total of 21 cards.

At the beginning of the game, one suspect, one weapon and one room is randomly selected to go into an envelope known as the "Case File". The remaining cards are dealt to the players.

As the game progresses, your goal is deduce which specific cards are in the Case File. Those cards represent the murderer, the murder weapon and the location that the murder occurred.

The way that you go about this deduction is by asking other players questions about what is in their hand. We will get into the specifics of this later. As you find out more information about what cards are where, you are able to eliminate some possibilities and eventually you should be able to solve the mystery! (Hopefully before anyone else!)

### 1.2 Propositional Logic Variables

We need to decide how to describe our world in the language of propositional logic. For this game, what we need to figure out is where cards are. They can be in the Case File or in a player's hand. We will be playing with 6 players, so we will need a boolean variable to represent each card being in any of the seven possible locations.

For example, one of the cards is the "Revolver". Therefore, we will need seven boolean variables, each of which represent that weapon being in either a player's hand or the Case File. This card must be exactly in one location (card locations don't change during the course of the game) so we can add the propositional logic sentences that enforce that exactly one of those seven variables is true.

## 2. Execute Command

> python3 filename.py

## 3.Content

Implement the solving function using

- Propositional Logic
