# From Rachel and Bill:
#
# We have 20 of the 52 so far.
#
# Ace of diamonds- L
# 3 of diamonds- Q
# 6 of diamonds- 9
# Jack of diamonds- 3
#
# Ace of hearts- T
# 3 of hearts- P
# 7 of hearts- 4
# 10 of hearts-M
# Jack of hearts-10
# Queen of hearts-C
#
# 2 of spades-W
# 4 of spades-13
# 6 of spades- V
# 7 of spades- 26
# 8 of spades- B
# King of spades-11
#
# 4 of clubs- A
# 5 of clubs-18
# 6 of clubs-E
# Queen of clubs-23

# Set up the source-of-truth grid as a continuous array of indices, 0-51, each coordinating with a card and suit
# Order is Ace, 2-10, J, Q, K
# Order is Spades, Hearts, Clubs, Diamonds
import logging
import random
from collections import namedtuple
import string

all_cards = [
    "A♠", "2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "10♠", "J♠", "Q♠", "K♠",
    "A♥", "2♥", "3♥", "4♥", "5♥", "6♥", "7♥", "8♥", "9♥", "10♥", "J♥", "Q♥", "K♥",
    "A♣", "2♣", "3♣", "4♣", "5♣", "6♣", "7♣", "8♣", "9♣", "10♣", "J♣", "Q♣", "K♣",
    "A♦", "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "8♦", "9♦", "10♦", "J♦", "Q♦", "K♦",
]

# Set up the base array of the final message
sample_from_final_message = [
    "7♥", "9♦", "10♣", "10♣", "9♠", "10♦", "5♥", "J♦", "9♠", "9♦", "7♥", "A♣", "A♠", "9♦", "7♥", "10♣", "J♥",
    "9♦",  # <-- ??? may be incorrect, couldn't read on scan
    "10♣", "9♠", "2♣", "Q♣", "5♥", "2♦", "7♥",
    "Q♣", "4♦",
    "6♦",  # <-- first card which was bolded with a non-serif font
    "7♥", "9♦", "K♥", "A♣", "7♥", "J♦", "7♠", "7♥", "J♦", "A♣", "9♠", "8♣", "J♦", "9♠", "J♥", "A♠", "9♦",
    "9♠", "4♦", "A♣", "6♦", "9♦"
]

# Note that there are 52 cards and only 26 characters in the alphabet
# A prior page has a title "Level Three: Find the Pairs", which seems to hint that perhaps certain cards may combine
# in some way or another

# Hypothesis 1: when a card is assigned a number, that number is just the letter of the alphabet,
#               and that card is the pair of the other which was directly assigned the same letter
#               e.g., based on current info Q♥ and J♦ are synonyms.
# Evidence: no number exceeds 26
# Evidence: 7 of spades seems rare, as expected if representing "z"
# Counter: 7 of spades is still present, which is a bit unexpected

# Test 1: randomly assign pairings for all "unknown" letters, locking in ones which are "known"
#         check whether there are many words present in the top 1000 words, with a special check for "MAINE"
#         hand-check any candidates
LetterPairing = namedtuple("LetterPairing", ["direct_assign", "numeric_assign"])
locked_letters = {
    LetterPairing("4♣", None): "a",
    LetterPairing("8♠", None): "b",
    LetterPairing("Q♥", "J♦"): "c",
    LetterPairing(None, "7♥"): "d",
    LetterPairing("6♣", None): "e",
    LetterPairing(None, None): "f",
    LetterPairing(None, None): "g",
    LetterPairing(None, None): "h",
    LetterPairing("6♦", None): "i",
    LetterPairing(None, "J♥"): "j",
    LetterPairing(None, "K♠"): "k",
    LetterPairing("A♦", None): "l",
    LetterPairing("4♠", "10♥"): "m",
    LetterPairing(None, None): "n",
    LetterPairing(None, None): "o",
    LetterPairing("3♥", None): "p",
    LetterPairing("3♦", None): "q",
    LetterPairing(None, "5♣"): "r",
    LetterPairing(None, None): "s",
    LetterPairing("A♥", None): "t",
    LetterPairing(None, None): "u",
    LetterPairing("6♠", None): "v",
    LetterPairing("2♠", "Q♣"): "w",
    LetterPairing(None, None): "x",
    LetterPairing(None, None): "y",
    LetterPairing(None, "7♠"): "z",
}
result = ""
for card in sample_from_final_message:
    _tmp = "".join([val for letter_pairing, val in locked_letters.items()
                    if letter_pairing.direct_assign == card
                    or letter_pairing.numeric_assign == card])
    if _tmp:
        result += _tmp
    else:
        result += " "

print("Hypothesis 1 results:\n{}".format(result))


# OUTPUT:
# Results:
# d      c  d   d j    w  dw id   dczdc   c j     i

# Conclusion: the pairing hypothesis appears to be invalid
# In particular, the "dczdc" string seems to be completely impossible to decode further by splitting
# A quick test of ROTs only yielded something interesting on ROT11: "onkon"
# Very likely this is not correct


# Is brute force an option?
# It's entirely possible that the initial card assignments uncovered by the team so far are only applicable during
# the immediately following phase, so the "locked" cards assumed above could be inapplicable.
# Assuming that each card may only be assigned one character, which may not be correct,
# and assuming that only alphabet characters are at play (no numerics, punctuation, spaces, etc),
# it's expected that there are roughly 6.15E36 combinations, which is definitely outside the realm of reason.
# Random assignment could yield results, but even then we're talking 3.12E36 combinations by median chance to reach the
# correct result.
# Still, it's worth a (smallish) try, just for fun.


def random_double_alphabet():
    # Create a function to return two of each character in the alphabet to a list randomly and return
    _tmp = list(string.ascii_lowercase) + list(string.ascii_lowercase)
    random.shuffle(_tmp)
    return _tmp


# Set up a logger just in case the system crashes during runs
logging.basicConfig(filename="experimenting.log",
                    filemode="a",
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                    level=logging.DEBUG)

# Open the file with the top thousand words
with open("1-1000.txt", "r") as top_thousand_words_file:
    # Read the top thousand words into a variable for speed
    top_thousand_words = top_thousand_words_file.readlines()

    # Loop for a randomly large number of tries, decided on 50 billion
    # Log every log_frequency tries
    count = 0
    stop_count = 50000000000
    log_frequency = 1000000
    # Start the log
    logging.info(f"Started attempts. Config: stop_count: {stop_count}, log_frequency: {log_frequency}")
    while count < stop_count:
        # Set up the input for this round
        random_input = random_double_alphabet()

        # Set up the crosswalk
        # This will be taking the index of the random input, coordinating it with the index of the all_cards list,
        # then pulling together a sample message based on the sample_from_final_message
        assignments = dict(zip(all_cards, random_input))
        result = "".join([assignments.get(card)
                          for card in sample_from_final_message])

        # Test whether there are words in the sample that might be interesting, log if so
        # Chose threshold of 3 distinct common words present
        words_found = [word for word in top_thousand_words
                       if word in result]
        if len(words_found) >= 3:
            logging.info("\n\nInteresting results!\n{}".format(result))
            logging.info("Words found:\n{}".format(words_found))
            logging.info("Using assignments:\n{}".format(assignments.items()))

        count += 1

        if count % log_frequency == 0:
            logging.info("\n\nCompleted {} attempts\n\n".format(count))

# Hypothesis 2: when a card is assigned a number, it literally means that number
# Evidence: instructions may include directions to coordinates, number of steps to take, or other numeric-type "words"
# Counter: it seems very unlikely to see single-digit coordinates, and the spread of numbers makes it seem likely
#          that they aren't to be used literally
