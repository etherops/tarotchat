#!/bin/bash -e

# Directory to store the downloaded images
assets_dir="./assets"

# Create the assets directory if it doesn't exist
mkdir -p "$assets_dir"

# Base URL for the images
base_url="https://upload.wikimedia.org/wikipedia/commons/thumb"

# List of image paths and corresponding filenames
images=(
  "9/90/RWS_Tarot_00_Fool.jpg/350px-RWS_Tarot_00_Fool.jpg RWS_Tarot_0_The_Fool.jpg"
  "d/de/RWS_Tarot_01_Magician.jpg/350px-RWS_Tarot_01_Magician.jpg RWS_Tarot_I_The_Magician.jpg"
  "8/88/RWS_Tarot_02_High_Priestess.jpg/350px-RWS_Tarot_02_High_Priestess.jpg RWS_Tarot_II_The_High_Priestess.jpg"
  "d/d2/RWS_Tarot_03_Empress.jpg/350px-RWS_Tarot_03_Empress.jpg RWS_Tarot_III_The_Empress.jpg"
  "c/c3/RWS_Tarot_04_Emperor.jpg/350px-RWS_Tarot_04_Emperor.jpg RWS_Tarot_IV_The_Emperor.jpg"
  "8/8d/RWS_Tarot_05_Hierophant.jpg/350px-RWS_Tarot_05_Hierophant.jpg RWS_Tarot_V_The_Hierophant.jpg"
  "d/db/RWS_Tarot_06_Lovers.jpg/350px-RWS_Tarot_06_Lovers.jpg RWS_Tarot_VI_The_Lovers.jpg"
  "9/9b/RWS_Tarot_07_Chariot.jpg/350px-RWS_Tarot_07_Chariot.jpg RWS_Tarot_VII_The_Chariot.jpg"
  "f/f5/RWS_Tarot_08_Strength.jpg/350px-RWS_Tarot_08_Strength.jpg RWS_Tarot_VIII_Strength.jpg"
  "4/4d/RWS_Tarot_09_Hermit.jpg/350px-RWS_Tarot_09_Hermit.jpg RWS_Tarot_IX_The_Hermit.jpg"
  "3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg/350px-RWS_Tarot_10_Wheel_of_Fortune.jpg RWS_Tarot_X_Wheel_of_Fortune.jpg"
  "e/e0/RWS_Tarot_11_Justice.jpg/350px-RWS_Tarot_11_Justice.jpg RWS_Tarot_XI_Justice.jpg"
  "2/2b/RWS_Tarot_12_Hanged_Man.jpg/350px-RWS_Tarot_12_Hanged_Man.jpg RWS_Tarot_XII_The_Hanged_Man.jpg"
  "d/d7/RWS_Tarot_13_Death.jpg/350px-RWS_Tarot_13_Death.jpg RWS_Tarot_XIII_Death.jpg"
  "f/f8/RWS_Tarot_14_Temperance.jpg/350px-RWS_Tarot_14_Temperance.jpg RWS_Tarot_XIV_Temperance.jpg"
  "5/55/RWS_Tarot_15_Devil.jpg/350px-RWS_Tarot_15_Devil.jpg RWS_Tarot_XV_The_Devil.jpg"
  "5/53/RWS_Tarot_16_Tower.jpg/350px-RWS_Tarot_16_Tower.jpg RWS_Tarot_XVI_The_Tower.jpg"
  "d/db/RWS_Tarot_17_Star.jpg/350px-RWS_Tarot_17_Star.jpg RWS_Tarot_XVII_The_Star.jpg"
  "7/7f/RWS_Tarot_18_Moon.jpg/350px-RWS_Tarot_18_Moon.jpg RWS_Tarot_XVIII_The_Moon.jpg"
  "1/17/RWS_Tarot_19_Sun.jpg/350px-RWS_Tarot_19_Sun.jpg RWS_Tarot_XIX_The_Sun.jpg"
  "d/dd/RWS_Tarot_20_Judgement.jpg/350px-RWS_Tarot_20_Judgement.jpg RWS_Tarot_XX_Judgement.jpg"
  "f/ff/RWS_Tarot_21_World.jpg/350px-RWS_Tarot_21_World.jpg RWS_Tarot_XXI_The_World.jpg"
  "1/11/Wands01.jpg/350px-Wands01.jpg RWS_Tarot_Ace_of_Wands.jpg"
  "0/0f/Wands02.jpg/350px-Wands02.jpg RWS_Tarot_Two_of_Wands.jpg"
  "f/ff/Wands03.jpg/350px-Wands03.jpg RWS_Tarot_Three_of_Wands.jpg"
  "a/a4/Wands04.jpg/350px-Wands04.jpg RWS_Tarot_Four_of_Wands.jpg"
  "9/9d/Wands05.jpg/350px-Wands05.jpg RWS_Tarot_Five_of_Wands.jpg"
  "3/3b/Wands06.jpg/350px-Wands06.jpg RWS_Tarot_Six_of_Wands.jpg"
  "e/e4/Wands07.jpg/350px-Wands07.jpg RWS_Tarot_Seven_of_Wands.jpg"
  "6/6b/Wands08.jpg/350px-Wands08.jpg RWS_Tarot_Eight_of_Wands.jpg"
  "4/4d/Tarot_Nine_of_Wands.jpg/350px-Tarot_Nine_of_Wands.jpg RWS_Tarot_Nine_of_Wands.jpg"
  "0/0b/Wands10.jpg/350px-Wands10.jpg RWS_Tarot_Ten_of_Wands.jpg"
  "6/6a/Wands11.jpg/350px-Wands11.jpg RWS_Tarot_Page_of_Wands.jpg"
  "1/16/Wands12.jpg/350px-Wands12.jpg RWS_Tarot_Knight_of_Wands.jpg"
  "0/0d/Wands13.jpg/350px-Wands13.jpg RWS_Tarot_Queen_of_Wands.jpg"
  "c/ce/Wands14.jpg/350px-Wands14.jpg RWS_Tarot_King_of_Wands.jpg"
  "3/36/Cups01.jpg/350px-Cups01.jpg RWS_Tarot_Ace_of_Cups.jpg"
  "f/f8/Cups02.jpg/350px-Cups02.jpg RWS_Tarot_Two_of_Cups.jpg"
  "7/7a/Cups03.jpg/350px-Cups03.jpg RWS_Tarot_Three_of_Cups.jpg"
  "3/35/Cups04.jpg/350px-Cups04.jpg RWS_Tarot_Four_of_Cups.jpg"
  "d/d7/Cups05.jpg/350px-Cups05.jpg RWS_Tarot_Five_of_Cups.jpg"
  "1/17/Cups06.jpg/350px-Cups06.jpg RWS_Tarot_Six_of_Cups.jpg"
  "a/ae/Cups07.jpg/350px-Cups07.jpg RWS_Tarot_Seven_of_Cups.jpg"
  "6/60/Cups08.jpg/350px-Cups08.jpg RWS_Tarot_Eight_of_Cups.jpg"
  "2/24/Cups09.jpg/350px-Cups09.jpg RWS_Tarot_Nine_of_Cups.jpg"
  "8/84/Cups10.jpg/350px-Cups10.jpg RWS_Tarot_Ten_of_Cups.jpg"
  "a/ad/Cups11.jpg/350px-Cups11.jpg RWS_Tarot_Page_of_Cups.jpg"
  "f/fa/Cups12.jpg/350px-Cups12.jpg RWS_Tarot_Knight_of_Cups.jpg"
  "6/62/Cups13.jpg/350px-Cups13.jpg RWS_Tarot_Queen_of_Cups.jpg"
  "0/04/Cups14.jpg/350px-Cups14.jpg RWS_Tarot_King_of_Cups.jpg"
  "1/1a/Swords01.jpg/350px-Swords01.jpg RWS_Tarot_Ace_of_Swords.jpg"
  "9/9e/Swords02.jpg/350px-Swords02.jpg RWS_Tarot_Two_of_Swords.jpg"
  "0/02/Swords03.jpg/350px-Swords03.jpg RWS_Tarot_Three_of_Swords.jpg"
  "b/bf/Swords04.jpg/350px-Swords04.jpg RWS_Tarot_Four_of_Swords.jpg"
  "2/23/Swords05.jpg/350px-Swords05.jpg RWS_Tarot_Five_of_Swords.jpg"
  "2/29/Swords06.jpg/350px-Swords06.jpg RWS_Tarot_Six_of_Swords.jpg"
  "3/34/Swords07.jpg/350px-Swords07.jpg RWS_Tarot_Seven_of_Swords.jpg"
  "a/a7/Swords08.jpg/350px-Swords08.jpg RWS_Tarot_Eight_of_Swords.jpg"
  "2/2f/Swords09.jpg/350px-Swords09.jpg RWS_Tarot_Nine_of_Swords.jpg"
  "d/d4/Swords10.jpg/350px-Swords10.jpg RWS_Tarot_Ten_of_Swords.jpg"
  "4/4c/Swords11.jpg/350px-Swords11.jpg RWS_Tarot_Page_of_Swords.jpg"
  "b/b0/Swords12.jpg/350px-Swords12.jpg RWS_Tarot_Knight_of_Swords.jpg"
  "d/d4/Swords13.jpg/350px-Swords13.jpg RWS_Tarot_Queen_of_Swords.jpg"
  "3/33/Swords14.jpg/350px-Swords14.jpg RWS_Tarot_King_of_Swords.jpg"
  "f/fd/Pents01.jpg/350px-Pents01.jpg RWS_Tarot_Ace_of_Pentacles.jpg"
  "9/9f/Pents02.jpg/350px-Pents02.jpg RWS_Tarot_Two_of_Pentacles.jpg"
  "4/42/Pents03.jpg/350px-Pents03.jpg RWS_Tarot_Three_of_Pentacles.jpg"
  "3/35/Pents04.jpg/350px-Pents04.jpg RWS_Tarot_Four_of_Pentacles.jpg"
  "9/96/Pents05.jpg/350px-Pents05.jpg RWS_Tarot_Five_of_Pentacles.jpg"
  "a/a6/Pents06.jpg/350px-Pents06.jpg RWS_Tarot_Six_of_Pentacles.jpg"
  "6/6a/Pents07.jpg/350px-Pents07.jpg RWS_Tarot_Seven_of_Pentacles.jpg"
  "4/49/Pents08.jpg/350px-Pents08.jpg RWS_Tarot_Eight_of_Pentacles.jpg"
  "f/f0/Pents09.jpg/350px-Pents09.jpg RWS_Tarot_Nine_of_Pentacles.jpg"
  "4/42/Pents10.jpg/350px-Pents10.jpg RWS_Tarot_Ten_of_Pentacles.jpg"
  "e/ec/Pents11.jpg/350px-Pents11.jpg RWS_Tarot_Page_of_Pentacles.jpg"
  "d/d5/Pents12.jpg/350px-Pents12.jpg RWS_Tarot_Knight_of_Pentacles.jpg"
  "8/88/Pents13.jpg/350px-Pents13.jpg RWS_Tarot_Queen_of_Pentacles.jpg"
  "1/1c/Pents14.jpg/350px-Pents14.jpg RWS_Tarot_King_of_Pentacles.jpg"
)

# Function to download images and check their size
download_image() {
    local image_path="$1"
    local filename="$2"
    local url="${base_url}/${image_path}"

    # Check if the file already exists
    if [[ ! -f "${assets_dir}/${filename}" ]]; then
        echo "Downloading ${assets_dir}/${filename} from ${url}"
        curl --silent -o "${assets_dir}/${filename}" -L "${url}"

        # Check the file size and exit with an error if it's too small (e.g., indicating a bad download)
        local filesize=$(stat -f%z "${assets_dir}/${filename}")
        if (( filesize < 5000 )); then
            echo "Error: Downloaded file ${filename} is too small (${filesize} bytes). Possible bad URL."
            exit 1
        fi
    else
        echo "File ${assets_dir}/${filename} already exists, skipping download."
    fi
}

# Iterate over the images array and download each one if it doesn't exist
for entry in "${images[@]}"; do
    image_path=$(echo $entry | awk '{print $1}')
    filename=$(echo $entry | awk '{print $2}')
    download_image "$image_path" "$filename"
done

echo "Download complete. Images saved in ${assets_dir}."


