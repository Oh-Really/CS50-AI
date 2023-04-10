from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Character is either a knight or a knave.
# A knight will always tell the truth: if a knight states a sentence, then that sentence is true.
# Conversely,
# a knave will always lie: if a knave states a sentence, then that sentence is false.

# Puzzle 0
# A says "I am both a knight and a knave."
sentence0 = And(AKnight, AKnave)
knowledge0 = And(
    #You can either be a knight or knave, but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    Implication(AKnight, sentence0),
    Implication(AKnave, Not(sentence0))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence1 = And(AKnave, BKnave)
knowledge1 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # Can only be both knaves, or a mix. Can't both be knights
    Implication(AKnight, sentence1),
    Implication(AKnave, Not(sentence1))

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentence2_a = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave)
)
sentence2_b = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight)
)
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    Implication(AKnight, sentence2_a),
    Implication(AKnave, Not(sentence2_a)),

    Implication(BKnight, sentence2_b),
    Implication(BKnave, Not(sentence2_b))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
