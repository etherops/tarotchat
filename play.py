import random
import argparse
from openai import OpenAI
import os
import subprocess
from PIL import Image  # Import the Pillow library

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

def display_card_images(cards):
    """Display the images for the drawn cards."""
    card_images = []
    for card in cards:
        # Normalize card name to match the file name format
        card_image_name = ("RWS_Tarot_" + card.replace(" - ", "_").replace(" ", "_") + ".jpg")
        card_image_path = os.path.join("./assets", card_image_name)

        if os.path.exists(card_image_path):
            card_images.append(Image.open(card_image_path))
        else:
            print(f"Image not found for card: {card_image_path}")

    if len(card_images) == 1:
        card_images[0].show()
    elif len(card_images) > 1:
        # Concatenate images side by side
        total_width = sum(img.width for img in card_images)
        max_height = max(img.height for img in card_images)
        combined_image = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in card_images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.width

        # Save the combined image to a temporary file
        combined_image_path = "./assets/temp_combined_image.jpg"
        combined_image.save(combined_image_path)

        # Use qlmanage to display the combined image
        subprocess.run(["qlmanage", "-p", combined_image_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Optionally, remove the temporary file after previewing
        os.remove(combined_image_path)

def interpret_cards(question, cards):
    # Initialize conversation history with a system message
    prompt = (
        f"We are playing a game of tarot using the Rider-Waite deck.\n"
        "Please interpret these cards in response to the question.  Please give a brief description of the general "
        "meaning of the card(s) followed by an interpretation of the draw based on the question asked."
    )
    messages = [
        {"role": "system", "content": prompt}
    ]

    # Append the user's question and drawn cards to the conversation
    messages.append({"role": "user", "content": f"Question: {question}"})
    messages.append({"role": "assistant", "content": f"Cards: {', '.join(cards)}"})

    # Send the conversation to OpenAI for interpretation
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Get the interpretation and add it to the conversation
    interpretation = response.choices[0].message.content
    messages.append({"role": "assistant", "content": interpretation})

    return interpretation

def tarot_game(num_cards, question):
    deck = tarot_deck.copy()
    cards = draw_cards(num_cards, deck)
    print(f"\nYour cards are: {', '.join(cards)}")

    interpretation = interpret_cards(question, cards)
    print(f"\nInterpretation based on your question:\n{interpretation}")

    # Display card images
    display_card_images(cards)

    while True:
        clarifier_choice = input("Would you like to draw a clarifying card? (yes/no): ").lower()
        if clarifier_choice == 'no':
            break
        if clarifier_choice == 'yes':
            clarifier_question = input("Please enter a clarifying question: ")
            if clarifier_question:
                clarifier = draw_cards(1, deck[1:])  # Exclude the first card from being drawn again
                print(f"\nYour clarifying card is: {clarifier[0]}")
                cards.append(clarifier[0])
                interpretation = interpret_cards(clarifier_question, cards)
                print(f"\nInterpretation based on your clarifier question:\n{interpretation}")
                display_card_images([clarifier[0]])
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
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
