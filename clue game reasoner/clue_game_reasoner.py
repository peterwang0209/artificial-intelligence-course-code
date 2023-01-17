"""clue_game_reasoner.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Ported to Python3 by Andy Exley

Copyright (C) 2008 Dave Musicant
Copyright (C) 2020 Andy Exley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA."""

import sat_interface

# Initialize important variables

CASE_FILE = "CF"
POSSIBLE_PLAYERS = ["SC", "MU", "WH", "GR", "PE", "PL"]
POSSIBLE_CARD_LOCATIONS = POSSIBLE_PLAYERS + [CASE_FILE]
SUSPECTS = ["mu", "pl", "gr", "pe", "sc", "wh"]
WEAPONS = ["kn", "ca", "re", "ro", "pi", "wr"]
ROOMS = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
CARDS = SUSPECTS + WEAPONS + ROOMS


class ClueGameReasoner:
    """This class represents a clue game reasoner, a tool that can be used
    to track the information during a game of clue and deduce information
    about the game. (Hopefully help you win!)
    """

    def __init__(self, player_order, card_nums=None):
        """init for a particular clue game.
            player_order is a list of strings of players in the order that they
            are sitting around the table. Note: This may not include all the suspects,
            as there may be fewer than 6 players in any given game.

            card_nums is a list of numbers of cards in players' hands. It is
            possible that different players have different numbers of cards!
        """
        self.players = player_order
        clauses = []

        # Each card is in at least one place (including case file).
        # If you want to change the string representation of the variables,
        # go ahead!
        for c in CARDS:
            clause = ""
            for p in POSSIBLE_CARD_LOCATIONS:
                clause += c + "_" + p + " "
            clauses.append(clause)

        # TO BE IMPLEMENTED AS AN EXERCISE:

        # A card cannot be in two places.
        for c in CARDS:
            # get two variable from POSSIBLE_CARD_LOCATIONS
            for p1 in POSSIBLE_CARD_LOCATIONS:
                for p2 in POSSIBLE_CARD_LOCATIONS:
                    # card cannot be in the two place, thus we proceed the function
                    # only when p1 is not p2, logic is card is not in p1 or card is not in p2
                    if p1 is not p2:
                        clause = ""
                        clause += "~" + c + "_" + p1 + " " + "~" + c + "_" + p2
                        clauses.append(clause)

        # At least one card of each category is in the case file.
        suspect_clause = ""
        # at least one card from SUSPECTS is in the CASEFILE
        for s in SUSPECTS:
            suspect_clause += s + "_" + CASE_FILE + " "
        clauses.append(suspect_clause)

        weapon_clause = ""
        # at least one card from WEAPONS is in the CASEFILE
        for w in WEAPONS:
            suspect_clause += w + "_" + CASE_FILE + " "
        clauses.append(weapon_clause)

        room_clause = ""
        # at least one card from ROOM is in the CASEFILE
        for r in ROOMS:
            room_clause += r + "_" + CASE_FILE + " "
        clauses.append(room_clause)

        # No two cards in each category can both be in the case file.
        for s1 in SUSPECTS:
            for s2 in SUSPECTS:
                # s1 and s2 cannot both be in the CASEFILE
                # so either s1 is not in CASEFILE or s2 is not in CASEFILE
                if s1 is not s2:
                    clause = ""
                    clause += "~" + CASE_FILE + "_" + s1 + " " + "~" + CASE_FILE + "_" + s2
                    clauses.append(clause)

        for w1 in WEAPONS:
            for w2 in WEAPONS:
                # w1 and w2 cannot both be in the CASEFILE
                # so either w1 is not in CASEFILE or w2 is not in CASEFILE
                if w1 is not w2:
                    clause = ""
                    clause += "~" + CASE_FILE + "_" + w1 + " " + "~" + CASE_FILE + "_" + w2
                    clauses.append(clause)

        for r1 in ROOMS:
            for r2 in ROOMS:
                # w1 and w2 cannot both be in the CASEFILE
                # so either w1 is not in CASEFILE or w2 is not in CASEFILE
                if r1 is not r2:
                    clause = ""
                    clause += "~" + CASE_FILE + "_" + r1 + " " + "~" + CASE_FILE + "_" + r2
                    clauses.append(clause)

        self.KB = sat_interface.KB(clauses)

    def add_hand(self, player_name, hand_cards):
        """Add the information about the given player's hand to the KB"""
        # TO BE IMPLEMENTED AS AN EXERCISE
        for c in hand_cards:
            # Need to use the built-in function add_clause from KB class to add card and player_name
            clause = ""
            clause += c + "_" + player_name
            self.KB.add_clause(clause)

    def suggest(self, suggester, c1, c2, c3, refuter, cardshown=None):
        """Add information about a given suggestion to the KB"""
        # TO BE IMPLEMENTED AS AN EXERCISE

        if refuter is not None:
            if cardshown is None:
                # if there is no card to be shown for refuter, then we have to bind every cards with refuter,
                # indicate all possibilities. Either refuter refute c1 V c2 C c3
                clause = ""
                clause += c1 + "_" + refuter + " " + c2 + "_" + refuter + " " + c3 + "_" + refuter
                self.KB.add_clause(clause)
            else:
                # if the card is shownable, then we bind it with the refuter, because refuter use this card to
                # refute the suggester
                clause = ""
                clause += cardshown + "_" + refuter
                self.KB.add_clause(clause)
            # locate the suggester location, we have to cover up the end -> beginning situation since it is a
            # round table, in this case we use the mod to get the correct person.
            suggester_index = (self.players.index(suggester) + 1) % len(self.players)
            # after locate the suggester index, we will go around the table
            while self.players[suggester_index] is not refuter:
                # the other player must refute the suggestion if they can
                for c in (c1, c2, c3):
                    clause = ""
                    clause += "~" + c + '_' + self.players[suggester_index]
                    self.KB.add_clause(clause)
                # move to the next player who is not refuter
                suggester_index = (suggester_index + 1) % len(self.players)
        else:
            # if there is no refuter, then we add all three cards with all possible players except for suggester
            # since no one will refute it
            for p in self.players:
                # check if the possible player is whether a suggester or not.
                # if it is a suggester, then we skip the process.
                if p is not suggester:
                    for c in (c1, c2, c3):
                        clause = ""
                        clause += "~" + c + '_' + p
                        self.KB.add_clause(clause)

    def accuse(self, accuser, c1, c2, c3, iscorrect):
        """Add information about a given accusation to the KB"""
        # TO BE IMPLEMENTED AS AN EXERCISE
        if not iscorrect:
            # if it is not correct, we add at least one of the card is not in the CASEFILE
            clause = ""
            clause += "~" + c1 + "_" + CASE_FILE + " " + "~" + c2 + "_" + CASE_FILE + " " + "~" + c3 + "_" + CASE_FILE
            self.KB.add_clause(clause)
        else:
            # if iscorrect, then we add the card with case file to the clause
            for c in (c1, c2, c3):
                clause = ""
                clause += c + '_' + CASE_FILE
            self.KB.add_clause(clause)

        # accuser can not accuse anymore but they can still remain in the game to refute the suggestion
        for c in (c1, c2, c3):
            clause = ""
            clause += "~" + c + '_' + accuser
        self.KB.add_clause(clause)

    def print_notepad(self):
        print("Clue Game Notepad:")
        for player in self.players:
            print('\t' + player, end='')
        print('\t' + CASE_FILE)
        for card in CARDS:
            print(card, '\t', end='')
            for player in self.players:
                print(self.get_test_string(card + "_" + player), '\t', end='')
            print(self.get_test_string(card + "_" + CASE_FILE))

    def get_test_string(self, variable):
        """test a variable and return 'Y', 'N' or '-'

            'Y' if this positive literal is entailed by the KB
            'N' if its reverse is entailed
            '-' if neither is entailed

            additionally, the entailed literal (if any) will be added to the KB
        """
        res = self.KB.test_add_variable(variable)
        if res:
            return 'Y'
        elif not res:
            return 'N'
        else:
            return '-'


def play_clue_game1():
    # the game begins! add players to the game
    cgr = ClueGameReasoner(["SC", "MU", "WH", "GR", "PE", "PL"])

    # Add information about our hand: We are Miss Scarlet,
    # and we have the cards Mrs White, Library, Study
    cgr.add_hand("SC", ["wh", "li", "st"])

    # We go first, we suggest that it was Miss Scarlet,
    # with the Rope in the Lounge. Colonel Mustard refutes us
    # by showing us the Miss Scarlet card.
    cgr.suggest("SC", "sc", "ro", "lo", "MU", "sc")

    # Mustard takes his turn. He suggests that it was Mrs. Peacock,
    # in the Dining Room with the Lead Pipe.
    # Mrs. White and Mr. Green cannot refute, but Mrs. Peacock does.
    cgr.suggest("MU", "pe", "pi", "di", "PE", None)

    # Mrs. White takes her turn
    cgr.suggest("WH", "mu", "re", "ba", "PE", None)

    # and so on...
    cgr.suggest("GR", "wh", "kn", "ba", "PL", None)
    cgr.suggest("PE", "gr", "ca", "di", "WH", None)
    cgr.suggest("PL", "wh", "wr", "st", "SC", "wh")
    cgr.suggest("SC", "pl", "ro", "co", "MU", "pl")
    cgr.suggest("MU", "pe", "ro", "ba", "WH", None)
    cgr.suggest("WH", "mu", "ca", "st", "GR", None)
    cgr.suggest("GR", "pe", "kn", "di", "PE", None)
    cgr.suggest("PE", "mu", "pi", "di", "PL", None)
    cgr.suggest("PL", "gr", "kn", "co", "WH", None)
    cgr.suggest("SC", "pe", "kn", "lo", "MU", "lo")
    cgr.suggest("MU", "pe", "kn", "di", "WH", None)
    cgr.suggest("WH", "pe", "wr", "ha", "GR", None)
    cgr.suggest("GR", "wh", "pi", "co", "PL", None)
    cgr.suggest("PE", "sc", "pi", "ha", "MU", None)
    cgr.suggest("PL", "pe", "pi", "ba", None, None)
    cgr.suggest("SC", "wh", "pi", "ha", "PE", "ha")

    # aha! we have discovered that the lead pipe is the correct weapon
    # if you print the notepad here, you should see that we know that
    # it is in the case file. But it looks like the jig is up and
    # everyone else has figured this out as well...

    cgr.suggest("WH", "pe", "pi", "ha", "PE", None)
    cgr.suggest("PE", "pe", "pi", "ha", None, None)
    cgr.suggest("SC", "gr", "pi", "st", "WH", "gr")
    cgr.suggest("MU", "pe", "pi", "ba", "PL", None)
    cgr.suggest("WH", "pe", "pi", "st", "SC", "st")
    cgr.suggest("GR", "wh", "pi", "st", "SC", "wh")
    cgr.suggest("PE", "wh", "pi", "st", "SC", "wh")

    # At this point, we are still unsure of whether it happened
    # in the kitchen, or the billiard room. printing our notepad
    # here should reflect that we know all the other information
    cgr.suggest("PL", "pe", "pi", "ki", "GR", None)

    # Aha! Mr. Green must have the Kitchen card in his hand
    print('Before accusation: should show a single solution.')
    cgr.print_notepad()
    print()
    cgr.accuse("SC", "pe", "pi", "bi", True)
    print('After accusation: if consistent, output should remain unchanged.')
    cgr.print_notepad()


def play_clue_game2():
    """This game recorded by Brooke Taylor and played by Sean Miller,
    George Ashley, Ben Limpich, Melissa Kohl and Andy Exley. Thanks to all!
    """
    cgr = ClueGameReasoner(["SC", "MU", "WH", "GR", "PE", "PL"])
    cgr.add_hand("WH", ["kn", "ro", "ki"])

    # all suggestions
    cgr.suggest("MU", "mu", "di", "pi", "PE", None)
    cgr.suggest("WH", "pl", "ca", "ba", "PE", "ba")
    cgr.suggest("GR", "pe", "ba", "ro", "PE", None)
    cgr.suggest("PE", "ki", "sc", "re", "WH", "ki")
    cgr.suggest("SC", "wh", "st", "ro", "MU", None)
    cgr.suggest("MU", "lo", "pl", "kn", "WH", "kn")
    cgr.suggest("WH", "li", "re", "pl", "GR", "re")
    cgr.suggest("PE", "st", "sc", "wr", "MU", None)
    cgr.suggest("PL", "bi", "gr", "wr", "SC", None)
    cgr.suggest("MU", "co", "pe", "ca", "GR", None)
    cgr.suggest("PE", "lo", "mu", "ro", "PL", None)
    cgr.suggest("PL", "co", "mu", "wr", "GR", None)
    cgr.suggest("SC", "ha", "ro", "pe", "WH", "ro")
    cgr.suggest("MU", "pe", "pi", "ba", "PE", None)
    cgr.suggest("WH", "sc", "pi", "ha", "PE", "sc")
    cgr.suggest("PE", "pl", "wr", "co", "PL", None)
    cgr.suggest("PL", "ba", "mu", "wr", "PE", None)
    cgr.suggest("SC", "st", "pi", "pe", "MU", None)
    cgr.suggest("WH", "ca", "st", "gr", "SC", "ca")
    cgr.suggest("GR", "sc", "ki", "wr", "PE", None)
    cgr.suggest("PE", "ki", "mu", "wr", "WH", "ki")
    cgr.suggest("MU", "st", "gr", "wr", "SC", None)
    cgr.suggest("WH", "gr", "ha", "wr", "SC", "ha")
    cgr.suggest("PE", "pe", "st", "wr", "MU", None)
    cgr.suggest("PL", "ki", "gr", "wr", "SC", None)
    cgr.suggest("SC", "li", "wr", "pe", "PL", None)
    cgr.suggest("WH", "di", "pe", "wr", None, None)

    cgr.print_notepad()
    # final accusation
    cgr.accuse("WH", "di", "pe", "wr", True)
    # Brooke wins!


def play_clue_game3():
    """Same as clue game 2, but from ms. peacock's perspective

    Note: It took my computer over 5 minutes to calculate the notepad on this one
    """
    cgr = ClueGameReasoner(["SC", "MU", "WH", "GR", "PE", "PL"])
    cgr.add_hand("PE", ["sc", "mu", "ba"])
    cgr.suggest("MU", "mu", "di", "pi", "PE", "mu")
    cgr.suggest("WH", "pl", "ca", "ba", "PE", "ba")
    cgr.suggest("GR", "pe", "ba", "ro", "PE", "ba")
    cgr.suggest("PE", "ki", "sc", "re", "WH", "ki")
    cgr.suggest("SC", "wh", "st", "ro", "MU", None)
    cgr.suggest("MU", "lo", "pl", "kn", "WH", None)
    cgr.suggest("WH", "li", "re", "pl", "GR", None)
    cgr.suggest("PE", "st", "sc", "wr", "MU", "st")
    cgr.suggest("PL", "bi", "gr", "wr", "SC", None)
    cgr.suggest("MU", "co", "pe", "ca", "GR", None)
    cgr.suggest("PE", "lo", "mu", "ro", "PL", "lo")
    cgr.suggest("PL", "co", "mu", "wr", "GR", None)
    cgr.suggest("SC", "ha", "ro", "pe", "WH", None)
    cgr.suggest("MU", "pe", "pi", "ba", "PE", "ba")
    cgr.suggest("WH", "sc", "pi", "ha", "PE", "sc")
    cgr.suggest("PE", "pl", "wr", "co", "PL", "pl")
    cgr.suggest("PL", "ba", "mu", "wr", "PE", "ba")
    cgr.suggest("SC", "st", "pi", "pe", "MU", None)
    cgr.suggest("WH", "ca", "st", "gr", "SC", None)
    cgr.suggest("GR", "sc", "ki", "wr", "PE", "sc")
    cgr.suggest("PE", "ki", "mu", "wr", "WH", "ki")
    cgr.suggest("MU", "st", "gr", "wr", "SC", None)
    cgr.suggest("WH", "gr", "ha", "wr", "SC", None)
    cgr.suggest("PE", "pe", "st", "wr", "MU", None)
    cgr.suggest("PL", "ki", "gr", "wr", "SC", None)
    cgr.suggest("SC", "li", "wr", "pe", "PL", None)

    # right before Mrs. White ends the game, I still
    # don't know what room it is in. :(
    cgr.print_notepad()
    cgr.suggest("WH", "di", "pe", "wr", None, None)
    cgr.accuse("WH", "di", "pe", "wr", True)


# Change which game gets called down here if you want to test
# other games
if __name__ == '__main__':
    play_clue_game1()
