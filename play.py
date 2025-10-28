import random
import argparse
from openai import OpenAI
import os
import subprocess
from PIL import Image  # Import the Pillow library
import inquirer
from inquirer import errors
from dotenv import load_dotenv  # Import load_dotenv from python-dotenv


load_dotenv()

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

def select_cards(num_cards, deck):
    """Select a specified number of cards from the deck using inquirer."""
    def validate(_, current):
        if len(current) != num_cards:
            raise errors.ValidationError('',
                                         reason=f"Please select {num_cards} card(s)! {len(current)} selected...")
        return True

    questions = [
        inquirer.Checkbox(
            "cards",
            message=f"Select {num_cards} card(s)",
            choices=deck,
            validate=validate
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers["cards"]

def display_card_images(cards, clarifiers=None):
    """Display the images for the drawn cards, including clarifiers in a new row."""
    card_images = []
    clarifier_images = []

    # Load main card images
    for card in cards:
        card_image_name = ("RWS_Tarot_" + card.replace(" - ", "_").replace(" ", "_") + ".jpg")
        card_image_path = os.path.join("./assets", card_image_name)
        if os.path.exists(card_image_path):
            card_images.append(Image.open(card_image_path))
        else:
            print(f"Image not found for card: {card_image_path}")

    # Load clarifier card images
    if clarifiers:
        for clarifier in clarifiers:
            clarifier_image_name = ("RWS_Tarot_" + clarifier.replace(" - ", "_").replace(" ", "_") + ".jpg")
            clarifier_image_path = os.path.join("./assets", clarifier_image_name)
            if os.path.exists(clarifier_image_path):
                clarifier_images.append(Image.open(clarifier_image_path))
            else:
                print(f"Image not found for clarifier: {clarifier_image_path}")

    # Check if this is a Celtic Cross spread (10 cards)
    if len(card_images) == 10:
        # Celtic Cross layout
        # Traditional positions:
        #     3
        #   5 1 6
        #     2
        #     4
        # 7 8 9 10 (column on the right)
        
        max_card_width = max(img.width for img in card_images)
        max_card_height = max(img.height for img in card_images)
        
        # Calculate total size needed
        total_width = max_card_width * 5 + 40  # 5 cards wide + spacing
        total_height = max_card_height * 4 + 30  # 4 cards tall + spacing
        
        combined_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))
        
        # Define positions for Celtic Cross layout (x, y)
        positions = [
            (max_card_width + 10, max_card_height + 10),     # 1 - Present (center)
            (max_card_width + 10, max_card_height * 2 + 20), # 2 - Challenge (below center)
            (max_card_width + 10, 0),                        # 3 - Underlying Cause (above center)
            (max_card_width + 10, max_card_height * 3 + 30), # 4 - Recent Past (bottom)
            (0, max_card_height + 10),                       # 5 - Highest Achievement (left)
            (max_card_width * 2 + 20, max_card_height + 10), # 6 - Moving Forward (right)
            (max_card_width * 3 + 30, 0),                    # 7 - Greatest Strength
            (max_card_width * 3 + 30, max_card_height + 10), # 8 - External Support
            (max_card_width * 3 + 30, max_card_height * 2 + 20), # 9 - Hopes and Fears
            (max_card_width * 3 + 30, max_card_height * 3 + 30)  # 10 - Outcome
        ]
        
        # Place cards in their positions
        for img, pos in zip(card_images, positions):
            combined_image.paste(img, pos)
    else:
        # Generic layout for any number of cards
        max_card_width = max(img.width for img in card_images) if card_images else 0
        max_card_height = max(img.height for img in card_images) if card_images else 0
        max_clarifier_width = max(img.width for img in clarifier_images) if clarifier_images else 0
        max_clarifier_height = max(img.height for img in clarifier_images) if clarifier_images else 0

        # Determine grid layout for main cards
        num_cards = len(card_images)
        if num_cards <= 3:
            cards_per_row = num_cards
        elif num_cards <= 6:
            cards_per_row = 3
        elif num_cards <= 12:
            cards_per_row = 4
        elif num_cards <= 20:
            cards_per_row = 5
        else:
            cards_per_row = 6
        
        rows_needed = (num_cards + cards_per_row - 1) // cards_per_row
        
        # Calculate total size
        total_width = max(max_card_width * cards_per_row + 10 * (cards_per_row - 1), 
                         max_clarifier_width * len(clarifier_images) if clarifier_images else 0)
        total_height = max_card_height * rows_needed + 10 * (rows_needed - 1)
        if clarifier_images:
            total_height += max_clarifier_height + 20

        combined_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))

        # Place main cards in grid
        for i, img in enumerate(card_images):
            row = i // cards_per_row
            col = i % cards_per_row
            x = col * (max_card_width + 10)
            y = row * (max_card_height + 10)
            combined_image.paste(img, (x, y))

        # Place clarifier card images
        if clarifier_images:
            y_offset = max_card_height * rows_needed + 10 * rows_needed + 10
            x_offset = (total_width - (max_clarifier_width * len(clarifier_images))) // 2
            for img in clarifier_images:
                combined_image.paste(img, (x_offset, y_offset))
                x_offset += img.width

    # Save and display the combined image
    combined_image_path = "./last_readings_cards.jpg"
    combined_image.save(combined_image_path)
    subprocess.run(["qlmanage", "-p", combined_image_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def interpret_cards(messages):
    response = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    interpretation = response.choices[0].message.content
    messages.append({"role": "assistant", "content": interpretation})

    return interpretation


def tarot_game(num_cards, question, select_cards_mode=False):
    deck = tarot_deck.copy()

    if select_cards_mode:
        cards = select_cards(num_cards, deck)
    else:
        cards = draw_cards(num_cards, deck)

    if num_cards == 10:
        print("\nYour Celtic Cross spread:")
        positions = ["Present", "Challenge", "Underlying Cause", "Recent Past", 
                    "Highest Achievement", "Moving Forward", "Greatest Strength", 
                    "External Support", "Hopes and Fears", "Outcome"]
        for i, (pos, card) in enumerate(zip(positions, cards)):
            print(f"{i+1}. {pos}: {card}")
    else:
        print(f"\nYour cards are: {', '.join(cards)}")

    # Remove drawn cards from the deck
    for card in cards:
        deck.remove(card)

    # Initialize conversation history with a system message
    if num_cards == 10:
        # Celtic Cross specific prompt
        prompt = (
            "We are playing a game of tarot using the Rider-Waite deck with a Celtic Cross spread.\n"
            "The Celtic Cross positions are:\n"
            "1. Present - The current situation\n"
            "2. Challenge - What crosses you or the immediate challenge\n"
            "3. Underlying Cause - The underlying cause or root of the situation\n"
            "4. Recent Past - Recent influences that led to the present\n"
            "5. Highest Achievement - The highest that can be achieved right now\n"
            "6. Moving Forward - Moving into the future, the next phase\n"
            "7. Greatest Strength - Your greatest strength in this situation\n"
            "8. External Support - External support or influences from others\n"
            "9. Hopes and Fears - Your hopes and fears about the situation\n"
            "10. Outcome - The likely outcome if the current path continues\n\n"
            "Please interpret each card in its position, including the traditional Rider-Waite imagery and meaning, "
            "then provide an integrated interpretation of the full spread in response to the question."
        )
        # Format cards with positions for Celtic Cross
        cards_with_positions = [f"Position {i+1} ({pos}): {card}" for i, (pos, card) in enumerate([
            ("Present", cards[0]),
            ("Challenge", cards[1]),
            ("Underlying Cause", cards[2]),
            ("Recent Past", cards[3]),
            ("Highest Achievement", cards[4]),
            ("Moving Forward", cards[5]),
            ("Greatest Strength", cards[6]),
            ("External Support", cards[7]),
            ("Hopes and Fears", cards[8]),
            ("Outcome", cards[9])
        ])]
        cards_str = '\n'.join(cards_with_positions)
    else:
        prompt = (
            "We are playing a game of tarot using the Rider-Waite deck.\n"
            "Please interpret these cards in response to the question. Please give a brief description of the general "
            "meaning of the card(s) including the traditional Ryder Waite imagery, followed by an interpretation of the "
            "draw based on the question asked."
        )
        cards_str = f"Cards: {', '.join(cards)}"
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Question: {question}"},
        {"role": "assistant", "content": cards_str}
    ]

    interpretation = interpret_cards(messages)
    print(f"\nInterpretation based on your question:\n{interpretation}")

    display_card_images(cards)

    # Skip clarifiers for Celtic Cross - it's already comprehensive
    if num_cards == 10:
        print("\n(Celtic Cross readings are comprehensive and don't require clarifier cards)")
        return
    
    clarifier_cards = []
    clarifier_num = 1
    while True:
        clarifier_question = input(
            "To draw a clarifier, enter a clarifying question or simply press Enter. Type 'no/N/No' to exit: "
        ).strip()

        if clarifier_question.lower() in ['no', 'n']:
            print("Exiting...")
            break

        if not clarifier_question:
            clarifier_question = "Please further clarify based on the following clarifier card..."

        if select_cards_mode:
            clarifier_card = select_cards(1, deck)[0]
        else:
            clarifier_card = draw_cards(1, deck)[0]  # Exclude the first card from being drawn again
        clarifier_cards.append(clarifier_card)
        print(f"\nYour clarifying card is: {clarifier_card}")

        # Remove the drawn clarifier card from the deck
        deck.remove(clarifier_card)

        messages.append({"role": "user", "content": f"Clarifier question: {clarifier_question}"})
        messages.append({"role": "assistant", "content": f"Clarifier card: {clarifier_card}"})

        interpretation = interpret_cards(messages)
        print(f"\nInterpretation based on your clarifier question:\n{interpretation}")

        display_card_images(cards, clarifier_cards)
        clarifier_num += 1


def _parse_args():
    parser = argparse.ArgumentParser(description="Tarot Card Drawing Game")
    parser.add_argument(
        '--num-cards',
        type=int,
        nargs='?',
        help="Number of cards to draw (1-78). Common spreads: 1 (single), 3 (three-card), 10 (Celtic Cross)"
    )
    parser.add_argument(
        '--question',
        type=str,
        help="A question to interpret the cards in response to"
    )
    parser.add_argument(
        '--select-cards',
        action='store_true',
        help="Select cards manually instead of drawing them randomly"
    )

    args = parser.parse_args()

    # Validate num_cards if provided
    if args.num_cards is not None:
        if args.num_cards < 1 or args.num_cards > 78:
            parser.error("--num-cards must be between 1 and 78")
    
    if args.num_cards is None:
        while True:
            print("\nHow many cards would you like to draw?")
            print("1: Draw one card")
            print("3: Draw three cards")
            print("10: Celtic Cross spread (10 cards)")
            print("Or enter any number between 1 and 78 for a custom spread")
            choice = input("Please choose an option: ")

            try:
                num = int(choice)
                if 1 <= num <= 78:
                    args.num_cards = num
                    break
                else:
                    print("Please enter a number between 1 and 78.")
            except ValueError:
                print("Please enter a valid number.")
    return args


if __name__ == "__main__":
    try:
        args = _parse_args()
        tarot_game(args.num_cards, args.question, args.select_cards)
    except KeyboardInterrupt:
        print("\n\nInterrupted! Exiting the tarot game...")
