import random
import argparse
from openai import OpenAI
import os

# Get the OpenAI API key from the environment variable

openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define the 78 cards in the Rider-Waite Tarot deck with Major Arcana numbered
tarot_deck = [
    "0 - The Fool", "I - The Magician", "II - The High Priestess", "III - The Empress", "IV - The Emperor",
    "V - The Hierophant", "VI - The Lovers", "VII - The Chariot", "VIII - Strength", "IX - The Hermit",
    "X - Wheel of Fortune", "XI - Justice", "XII - The Hanged Man", "XIII - Death", "XIV - Temperance",
    "XV - The Devil", "XVI - The Tower", "XVII - The Star", "XVIII - The Moon", "XIX - The Sun",
    "XX - Judgement", "XXI - The World",
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands",
    "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands",
    "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands",
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups",
    "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups",
    "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords",
    "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords",
    "Page of Swords", "Knight of Swords", "Queen of Swords", "King of Swords",
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles",
    "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles",
    "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles"
]

def draw_cards(num_cards, deck):
    """Draw a specified number of cards from the deck."""
    random.shuffle(deck)
    return deck[:num_cards]

def interpret_cards(question, cards):
    prompt = (
        f"We are playing a game of tarot using the Rider-Waite deck.\n"
        # f"The question is: {question}\n"
        # f"The drawn cards are: {', '.join(cards)}\n"
        "Please interpret these cards in response to the question.  Please give a brief description of the general "
        "meaning of the card(s) followed by an interpretation of the draw based on the question asked."
    )
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the correct model name (like gpt-4 or gpt-3.5-turbo)
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Question: {question}"},
            {"role": "assistant", "content": f"Cards: {cards}"},
        ]
    )
    return response.choices[0].message.content


def tarot_game(num_cards, question=None):
    deck = tarot_deck.copy()
    cards = draw_cards(num_cards, deck)
    print(f"\nYour cards are: {', '.join(cards)}")

    if not question:
        return

    interpretation = interpret_cards(question, cards)
    print(f"\nInterpretation based on your question:\n{interpretation}")
    while True:
        clarifier_choice = input("Would you like to draw a clarifying card? (yes/no): ").lower()
        if clarifier_choice == 'no':
            break
        if clarifier_choice == 'yes':
            clarifier = draw_cards(1, deck[1:])  # Exclude the first card from being drawn again
            print(f"\nYour clarifying card is: {clarifier[0]}")
            cards.append(clarifier[0])
            if question:
                interpretation = interpret_cards(question, cards)
                print(f"\nInterpretation based on your question with clarifiers:\n{interpretation}")
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    # models = openai_client.models.list()
    parser = argparse.ArgumentParser(description="Tarot Card Drawing Game")
    parser.add_argument(
        '--num-cards',
        type=int,
        nargs='?',
        choices=[1, 3],
        help="Number of cards to draw (1 or 3)"
    )
    parser.add_argument(
        '--question',
        type=str,
        help="A question to interpret the cards in response to"
    )

    args = parser.parse_args()

    if args.num_cards is None:
        while True:
            print("\nHow many cards would you like to draw?")
            print("1: Draw one card")
            print("2: Draw three cards")
            choice = input("Please choose an option (1 or 3): ")

            if choice == '1':
                tarot_game(1, args.question)
                break
            elif choice == '3':
                tarot_game(3, args.question)
                break
            else:
                print("Invalid choice. Please enter 1 or 3.")
    else:
        tarot_game(args.num_cards, args.question)
