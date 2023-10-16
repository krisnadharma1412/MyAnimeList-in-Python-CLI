import json
import os
import random
from datetime import datetime
from io import BytesIO
from typing import List

import pylast
import requests
from pick import pick
from PIL import Image, ImageDraw, ImageFont
from rich import print
from rich.panel import Panel
from rich.table import Table

def search_anime():
    search = input('Search Anime: ')
    response = requests.get(f'https://api.jikan.moe/v4/anime?q={search}&limit=1')

    anime_data = response.json()
    # Extracting information
    anime_info = anime_data['data'][0]  # Assuming there's only one entry in the 'data' list

    title = anime_info['title']
    score = anime_info['score']
    image_url = anime_info['images']['jpg']['image_url']

    # Displaying the information
    print(f"Title: {title}")
    print(f"Score: {score}")
    print(f"Image URL: {image_url}")


def recommend_anime(genre, num_recommendations=3):
    anime_data = load_anime_data()
    # Filter anime by genre
    filtered_anime = [anime for anime in anime_data if genre in anime["genre"]]
    # If there are no matches, inform the user
    if not filtered_anime:
        return "No anime found for the specified genre."
    # Randomly select recommended anime
    recommendations = random.sample(filtered_anime, min(num_recommendations, len(filtered_anime)))

    return recommendations

def load_or_create_json() -> None:
    if os.path.exists("animes.json"):
        with open("animes.json") as file:
            ratings = json.load(file)
    else:
        # create a new json file with empty dict
        with open("animes.json", "w") as file:
            ratings = {"anime_ratings": [], "tier_lists": []}
            json.dump(ratings, file)

def create_tier_list_helper(animes_to_rank, tier_name):
    # if there are no more animes to rank, return an empty list
    if not animes_to_rank:
        return []
    
    question = f"Select the animes you want to rank in  {tier_name}"
    tier_picks = pick(options=animes_to_rank, title=question, multiselect=True, indicator="→", min_selection_count=0)
    tier_picks = [x[0] for x in tier_picks]
    
    for anime in tier_picks:
        animes_to_rank.remove(anime)

    return tier_picks

def get_anime_cover(anime):
    response = requests.get(f'https://api.jikan.moe/v4/anime?q={anime}&limit=1')
    cover_url = response.json()['images']['jpg']['image_url']
    return cover_url

def create_tier_list():
    load_or_create_json()
    with open("animes.json") as file:
        anime_file = json.load(file)
    
    print("TIERS - S, A, B, C, D, E")

    # question = "Which anime do you want to rank?"
    # anime = input(question).strip()

    try:
         # keep only the album name by splitting the string at the first - and removing the first element
        animes_to_rank = [x.split(" - ", 1)[1] for x in animes_to_rank[1:]]
        
        # Name the tier list
        question = "What do you want to call this tier list?"
        tier_list_name = input(question).strip()

        # repeat until the user enters at least one character
        while not tier_list_name:
            print("Please enter at least one character")
            tier_list_name = input(question).strip()

        # S TIER
        question = "Select the animes you want to rank in S Tier:"
        s_tier_picks = create_tier_list_helper(animes_to_rank, "S Tier")
        s_tier_covers = [get_anime_cover(anime) for anime in s_tier_picks]
        s_tier = [{"anime":anime,"cover_art": cover} for anime, cover in zip(s_tier_picks, s_tier_covers)]
        
        # A TIER
        question = "Select the animes you want to rank in A Tier:"
        a_tier_picks = create_tier_list_helper(animes_to_rank, "S Tier")
        a_tier_covers = [get_anime_cover(anime) for anime in a_tier_picks]
        a_tier = [{"anime":anime,"cover_art": cover} for anime, cover in zip(a_tier_picks, a_tier_covers)]
        
        # B TIER
        question = "Select the animes you want to rank in B Tier:"
        b_tier_picks = create_tier_list_helper(animes_to_rank, "S Tier")
        b_tier_covers = [get_anime_cover(anime) for anime in b_tier_picks]
        b_tier = [{"anime":anime,"cover_art": cover} for anime, cover in zip(b_tier_picks, b_tier_covers)]
        
        # C TIER
        question = "Select the animes you want to rank in C Tier:"
        c_tier_picks = create_tier_list_helper(animes_to_rank, "C Tier")
        c_tier_covers = [get_anime_cover(anime) for anime in c_tier_picks]
        c_tier = [{"anime":anime,"cover_art": cover} for anime, cover in zip(c_tier_picks, c_tier_covers)]
        
        # D TIER
        question = "Select the animes you want to rank in D Tier:"
        d_tier_picks = create_tier_list_helper(animes_to_rank, "D Tier")
        d_tier_covers = [get_anime_cover(anime) for anime in d_tier_picks]
        d_tier = [{"anime":anime,"cover_art": cover} for anime, cover in zip(d_tier_picks, d_tier_covers)]
        
        # E TIER
        question = "Select the animes you want to rank in E Tier:"
        e_tier_picks = create_tier_list_helper(animes_to_rank, "E Tier")
        e_tier_covers = [get_anime_cover(anime) for anime in e_tier_picks]
        e_tier = [{"anime":anime,"cover_art": cover} for anime, cover in zip(e_tier_picks, e_tier_covers)]

        # check if all tiers are empty and if so, exit
        if not any([s_tier_picks, a_tier_picks, b_tier_picks, c_tier_picks, d_tier_picks, e_tier_picks]):
            print("All tiers are empty. Exiting...")
            return
        
        # # add the animes that were picked to the tier list
        tier_list = {
            "tier_list_name": tier_list_name,
            "s_tier": s_tier, 
            "a_tier": a_tier,
            "b_tier": b_tier,
            "c_tier": c_tier,
            "d_tier": d_tier,
            "e_tier": e_tier,
            "time": str(datetime.now())
        }
        
        # add the tier list to the json file
        anime_file["tier_lists"].append(tier_list)
        
        # save the json file
        with open("animes.json", "w") as f:
            json.dump(anime_file, f, indent=4)
        return
    
    except pylast.PyLastError:
        print("❌[b red] Artist not found [/b red]")

def image_generator(file_name, data):
    # return if the file already exists
    if os.path.exists(file_name):
        return
    
    # Set the image size and font
    image_width = 1920
    image_height = 5000
    font = ImageFont.truetype("arial.ttf", 15)
    tier_font = ImageFont.truetype("arial.ttf", 30)
    
    # Make a new image with the size and background color black
    image = Image.new("RGB", (image_width, image_height), "black")
    text_cutoff_value = 20

    #Initialize variables for row and column positions
    row_pos = 0
    col_pos = 0
    increment_size = 200
    
    """S Tier"""
    # leftmost side - make a square with text inside the square and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="red")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "S Tier", font=tier_font, fill="white")
        col_pos += increment_size
        
    for anime in data["s_tier"]:
        # Get the cover art
        response = requests.get(anime["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
    
    	# Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))
        
        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))
        
        # Draw the anime name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the anime name
        name = anime["anime"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0 

    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0

    """A TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="orange")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "A Tier", font=tier_font, fill="white")
        col_pos += increment_size
        
    for anime in data["a_tier"]:
        response = requests.get(anime["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = anime["anime"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0 

    row_pos += increment_size + 50
    col_pos = 0
    
    """B TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="yellow")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "B Tier", font=tier_font, fill="black")
        col_pos += increment_size
        
    for anime in data["b_tier"]:
        response = requests.get(anime["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = anime["anime"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")
        col_pos += 200
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0
    
    row_pos += increment_size + 50
    col_pos = 0
    
    """C TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="green")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "C Tier", font=tier_font, fill="black")
        col_pos += increment_size
        
    for anime in data["c_tier"]:
        response = requests.get(anime["cover_art"])
        cover_art = Image.open(BytesIO(response.content))       
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = anime["anime"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0
    
    row_pos += increment_size + 50
    col_pos = 0
   

    """D TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="blue")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "D Tier", font=tier_font, fill="black")
        col_pos += increment_size
        
    for anime in data["d_tier"]:
        response = requests.get(anime["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))        
        draw = ImageDraw.Draw(image)
        
        name = anime["anime"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0
    
    row_pos += increment_size + 50
    col_pos = 0


    """E TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="pink")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "E Tier", font=tier_font, fill="black")
        col_pos += increment_size
        
    for anime in data["e_tier"]:
        
        response = requests.get(anime["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        cover_art = cover_art.resize((increment_size, increment_size))    
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)
        name = anime["anime"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")
        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0
    
    row_pos += increment_size + 50
    col_pos = 0

    image = image.crop((0, 0, image_width, row_pos))

    image.save(f"{file_name}")

def main():
    startup_question = "What Do You Want To Do?"
    options = ["Give Me Anime Recommendation","Search Anime Information", "Make a Tier List", "See Created Tier Lists", "EXIT"]
    selected_option, index = pick(options, startup_question, indicator="→")
    
    if index == 0:
        recommend_anime()
    elif index == 1:
        search_anime()
    elif index == 2:
        create_tier_list()
    elif index == 3:
        see_tier_lists()
    elif index == 4:
        exit()

if __name__ == "__main__":
    main()


