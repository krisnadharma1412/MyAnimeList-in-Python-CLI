import os
import time
import json
import requests
from pick import pick
from io import BytesIO
from pyfiglet import Figlet
from itertools import islice
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Rich Library
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.text import Text

# MENU 1
def see_myanimelist():
    json_file_path = "my_anime_list.json"

    # Check if the file exist
    if not os.path.exists(json_file_path):
        print(f"❌ {add_bold_color('No MyAnimeList found. Please add anime to your list first.', 'red')}")
        back_to_main_menu(3)
    # Load data from the JSON file
    with open(json_file_path) as json_file:
        data = json.load(json_file)

    # Create a Rich Table instance
    table = Table(title=Text("MyAnimeList", style="bold"))
    table.add_column("No.", style="cyan", justify="right")
    table.add_column("Title", style="magenta")
    table.add_column("MyAnimeList Score", style="green")
    table.add_column("Genres", style="yellow")
    table.add_column("Status", style="cyan")

    # Extracting Data from JSON
    for i in range(len(data)):
        genres = ", ".join(data[i]["genres"])
        table.add_row(
            str(i + 1),
            data[i]["title"],
            str(data[i]["score"]),
            genres,
            data[i]["status"],
        )

    # Create a Rich Console instance
    console = Console()
    # Print the table
    console.print(f"\n\n")
    console.print(table)
    # Create a Panel for the menu options
    menu_panel = Panel(
        """
        What Do You Want To Do?
        1. Add an Anime To Your List
        2. Delete an Anime From Your List
        3. Back To Main Menu
        """,
        title="Menu Options",
        border_style="green",
        padding=(1, 2),
    )
    # Print the menu panel
    print(menu_panel)

    while True:
        selected_option = input(f"\nEnter the number of your choice: ")
        if selected_option == "1":
            clear()
            search_anime()
        elif selected_option == "2":
            print(delete_anime(data))
            time.sleep(3)
            clear()
            see_myanimelist()
        elif selected_option == "3":
            back_to_main_menu()
        else:
            print(f"❌ {add_bold_color('Invalid choice. Please enter a valid number.', 'red')}")
            time.sleep(2)
            clear()
            see_myanimelist()

def create_table_from_api(data, title="MyAnimeList"):
    # Create a Rich Table instance
    table = Table(title=Text(title, style="bold"))
    # Define the table columns
    table.add_column("No.", style="cyan", justify="right")
    table.add_column("Title", style="magenta")
    table.add_column("MyAnimeList Score", style="green")
    table.add_column("Genres", style="yellow")
    table.add_column("Status", style="cyan")

    # Extracting Data
    for i in range(len(data["data"])):
        anime_info = data["data"][i]
        anime_title = anime_info["title"]
        score = anime_info["score"]
        genres = [genre["name"] for genre in anime_info["genres"]]
        genres = ", ".join(genres)
        status = anime_info["status"]

        # Add a row to the table
        table.add_row(str(i + 1), anime_title, str(score), genres, status)
    return table

# MENU 2
def recommend_anime():
    # Create a Rich Console instance
    console = Console()
    clear()
    # Request Genre Information From Jikan API
    genre_api = requests.get("https://api.jikan.moe/v4/genres/anime").json()
    # Create Rich Table for Genre Information
    table = Table(title=Text("Anime Genres", style="bold"))
    table.add_column("MAL ID", style="green")
    table.add_column("Genre Example", style="magenta")
    # Sort Table base on ID
    sorted_data = sorted(genre_api["data"], key=lambda x: x["mal_id"])
    # Extract Data
    # for entry in sorted_data: #All Genres Displayed
    for entry in islice(sorted_data, 10):  # limit to 10 rows
        table.add_row(str(entry["mal_id"]), entry["name"])

    console.print(table)
    # Define the link URL
    link_url = "https://myanimelist.net/anime.php"
    # Print the formatted link
    console.print(f"See All Genres in this link: {link_url}", style="bold green")

    # Create a mapping of genre names to their IDs
    genre_name_to_id = {entry["name"]: entry["mal_id"] for entry in genre_api["data"]}

    while True:
        genre = input("What kind of genre you want? (id or genres name): ")
        # if the genre is str, Convert the user input to the corresponding genre ID
        if not genre.isdigit():  # if the input is not a number
            genre_str = genre
            genre = genre_name_to_id.get(genre.capitalize())
            if genre is None:
                console.print(f"Genre {genre_str} is not available", style="bold red")
                continue
        # if the input is not valid
        available_genre = [genre["mal_id"] for genre in genre_api["data"]]
        if int(genre) not in available_genre:
            console.print("Genre is not available", style="bold red")
        else:
            break

    # Search top anime based on the genre
    response = requests.get(
        f"https://api.jikan.moe/v4/anime?genres={genre}&order_by=score&sort=desc"
    )
    anime_data = response.json()
    clear()
    table = create_table_from_api(anime_data, "Anime Recommendation")
    console.print(table)
    while True:
        answer1 = input(f"Do you want to add an Anime To Your List (y/n): ")
        if answer1 == "y":
            error_check = add_anime_to_json(anime_data)
            if error_check[0] == "❌":
                while error_check[0] == "❌":
                    error_check = add_anime_to_json(anime_data)
                    print(error_check)
                    if error_check[0] == "✅":
                        break
            else:
                print(error_check)
                time.sleep(2)
        elif answer1 == "n":
            while True:
                answer2 = input(f"Do you want to search other Genre (y/n): ")
                if answer2 == "y":
                    clear()
                    recommend_anime()
                elif answer2 == "n":
                    back_to_main_menu()
                else:
                    print(f"❌ {add_bold_color('Invalid choice. Please enter a valid number', 'red')}")
        else:
            print(f"❌ {add_bold_color('Invalid choice. Please enter a valid number', 'red')}")


def add_anime_to_json(anime_data):
    try:
        # Ask the user to choose a number from the displayed results
        selected_no = int(
            input(
                "Enter the number of the anime you want to save to your MyAnimeList (0 to cancel or exit to main menu): "
            )
        )
        if 1 <= selected_no <= len(anime_data["data"]):
            # User selected a valid anime
            selected_anime = anime_data["data"][selected_no - 1]
            # Make a list of dictionary to store the selected anime
            new_anime = {
                "title": selected_anime["title"],
                "score": selected_anime["score"],
                "genres": [genre["name"] for genre in selected_anime["genres"]],
                "status": selected_anime["status"],
                "image_url": selected_anime["images"]["jpg"]["image_url"],
            }
            # Json File Name
            json_file_path = "my_anime_list.json"
            if os.path.exists(json_file_path):
                # File already exists, load existing data
                with open(json_file_path, "r") as json_file:
                    existing_data = json.load(json_file)

                # Check if an anime with the same title already exists
                if any(
                    anime["title"] == new_anime["title"] for anime in existing_data
                ):
                    return f"❌ [b red]'Anime '{new_anime['title']}' is already in 'my_anime_list.json'[/b red]"
                    
                else:
                    # Append existing data with new selected anime
                    existing_data.append(new_anime)
                    # Write the updated data back to the file
                    with open(json_file_path, "w") as json_file:
                        json.dump(existing_data, json_file, indent=2)

                    return f"✅ Anime '{new_anime['title']}' has been added in 'my_anime_list.json'"
            else:
                # File does not exist, create a new file with selected anime data
                existing_data = [new_anime]
                # Write the new data to the file
                with open(json_file_path, "w") as json_file:
                    json.dump(existing_data, json_file, indent=2)

                return f"✅ Anime '{new_anime['title']}' saved to 'my_anime_list.json'"
        elif selected_no == 0:
            back_to_main_menu()
        else:
            return f"❌ [b red]'Invalid input. Please select between 1 and {len(anime_data['data'])}[/b red]."
    except ValueError:
        return f"❌ {add_bold_color('Invalid input. Please enter a number', 'red')}"

# MENU 3
def search_anime():
    console = Console()
    title = input("Search Anime Keyword: ")
    response = requests.get(f"https://api.jikan.moe/v4/anime?q={title}&limit=10")
    anime_data = response.json()
    table = create_table_from_api(anime_data, "Search Results")
    console.print(table)

    while True:
        answer1 = input(f"Do you want to add an Anime To Your List (y/n): ")
        if answer1 == "y":
            error_check = add_anime_to_json(anime_data)
            print(error_check)
            if error_check[0] == "❌":
                while error_check[0] == "❌":
                    error_check = add_anime_to_json(anime_data)
                    print(error_check)
                    if error_check[0] == "✅":
                        break
            else:
                print(error_check)
                time.sleep(2)
        elif answer1 == "n":
            while True:
                answer2 = input(f"Do you want to search other Anime (y/n): ")
                if answer2 == "y":
                    clear()
                    search_anime()
                elif answer2 == "n":
                    back_to_main_menu()
                else:
                    print(f"❌ {add_bold_color('Invalid choice. Please enter a valid number.', 'red')}")
        else:
            print(f"❌ {add_bold_color('Invalid choice. Please enter a valid number', 'red')}")

def back_to_main_menu(seconds=2):
    print("[b yellow]back to main menu...[/b yellow]")
    # Add a delay of 2 seconds
    time.sleep(seconds)
    # Clear the terminal screen
    clear()
    time.sleep(1)
    main()


def delete_anime(data):
    title = input("Enter the title of the Anime: ").strip()
    found = False
    for i in range(len(data)):
        if data[i]["title"] == title:
            found = True
            # ask for confirmation to confirm delete
            console = Console()
            console.print(
                f"Are you sure you want to delete [cyan]'{title}'[/cyan] from [blue]'MyAnimeList Table'?[/blue] (y/n)", end=" "
            )
            confirm = input().strip()
            if confirm.lower() == "y":
                del data[i]
                with open("my_anime_list.json", "w") as json_file:
                    json.dump(data, json_file, indent=2)
                clear()
                return f"✅ Anime '{title}' has been deleted from 'my_anime_list.json'"
            elif confirm.lower() == "n":
                return "No changes were made."
    if not found:
        return f"❌ [b red]'No anime with the title '{title}' found in MyAnimeList table. Please try again.[/b red]"


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
    hint = "Use -> to select the anime and ENTER to Finish The Tier List"
    question = f"{hint}\n\nSelect the animes you want to rank in  {tier_name}"
    tier_picks = pick(
        options=animes_to_rank,
        title=question,
        multiselect=True,
        indicator="→",
        min_selection_count=0,
    )
    tier_picks = [x[0] for x in tier_picks]

    for anime in tier_picks:
        animes_to_rank.remove(anime)

    return tier_picks


def get_anime_cover(anime):
    with open("my_anime_list.json") as file:
        data = json.load(file)
    for i in range(len(data)):
        if data[i]["title"] == anime:
            cover_url = data[i]["image_url"]
    return cover_url


# MENU 4
def create_tier_list():
    clear()
    # Check if the myanimelist file exist
    if not os.path.exists("my_anime_list.json"):
        print(f"❌ {add_bold_color('No MyAnimeList found. Please add anime to your list first.', 'red')}")
        back_to_main_menu(3)

    console = Console()
    load_or_create_json()
    with open("animes.json") as file:
        anime_file = json.load(file)

    print("TIERS - S, A, B, C, D, E")

    # Extract the anime from my_anime_list.json
    with open("my_anime_list.json") as file:
        my_anime_list = json.load(file)
    animes_to_rank = [anime["title"] for anime in my_anime_list]

    # Name the tier list
    question = "What do you want to call this tier list? "
    tier_list_name = input(question).strip()

    # repeat until the user enters at least one character
    while not tier_list_name:
        print("Please enter at least one character")
        tier_list_name = input(question).strip()

    # S TIER
    question = "Select the animes you want to rank in S Tier:"
    s_tier_picks = create_tier_list_helper(animes_to_rank, "S Tier")
    s_tier_covers = [get_anime_cover(anime) for anime in s_tier_picks]
    s_tier = [
        {"anime": anime, "cover_art": cover}
        for anime, cover in zip(s_tier_picks, s_tier_covers)
    ]

    # A TIER
    question = "Select the animes you want to rank in A Tier:"
    a_tier_picks = create_tier_list_helper(animes_to_rank, "A Tier")
    a_tier_covers = [get_anime_cover(anime) for anime in a_tier_picks]
    a_tier = [
        {"anime": anime, "cover_art": cover}
        for anime, cover in zip(a_tier_picks, a_tier_covers)
    ]

    # B TIER
    question = "Select the animes you want to rank in B Tier:"
    b_tier_picks = create_tier_list_helper(animes_to_rank, "B Tier")
    b_tier_covers = [get_anime_cover(anime) for anime in b_tier_picks]
    b_tier = [
        {"anime": anime, "cover_art": cover}
        for anime, cover in zip(b_tier_picks, b_tier_covers)
    ]

    # C TIER
    question = "Select the animes you want to rank in C Tier:"
    c_tier_picks = create_tier_list_helper(animes_to_rank, "C Tier")
    c_tier_covers = [get_anime_cover(anime) for anime in c_tier_picks]
    c_tier = [
        {"anime": anime, "cover_art": cover}
        for anime, cover in zip(c_tier_picks, c_tier_covers)
    ]

    # D TIER
    question = "Select the animes you want to rank in D Tier:"
    d_tier_picks = create_tier_list_helper(animes_to_rank, "D Tier")
    d_tier_covers = [get_anime_cover(anime) for anime in d_tier_picks]
    d_tier = [
        {"anime": anime, "cover_art": cover}
        for anime, cover in zip(d_tier_picks, d_tier_covers)
    ]

    # E TIER
    question = "Select the animes you want to rank in E Tier:"
    e_tier_picks = create_tier_list_helper(animes_to_rank, "E Tier")
    e_tier_covers = [get_anime_cover(anime) for anime in e_tier_picks]
    e_tier = [
        {"anime": anime, "cover_art": cover}
        for anime, cover in zip(e_tier_picks, e_tier_covers)
    ]

    # check if all tiers are empty and if so, exit
    if not any(
        [
            s_tier_picks,
            a_tier_picks,
            b_tier_picks,
            c_tier_picks,
            d_tier_picks,
            e_tier_picks,
        ]
    ):
        print("All tiers are empty. Exiting...")
        time.sleep(2)
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
        "time": str(datetime.now()),
    }

    # add the tier list to the json file
    anime_file["tier_lists"].append(tier_list)

    # save the json file
    with open("animes.json", "w") as f:
        json.dump(anime_file, f, indent=4)
    console.print(f"✅ Tier list '{tier_list_name}' created successfully !")
    back_to_main_menu(3) 

# MENU 5
def see_tier_lists():
    load_or_create_json()
    with open("animes.json", "r") as f:
        data = json.load(f)

    if not data["tier_lists"]:
        print(f"❌ {add_bold_color('No tier lists have been created yet!)', 'red')}")
        back_to_main_menu(3) 

    for key in data["tier_lists"]:
        image_generator(f"{key['tier_list_name']}.png", key)
        print(f"✅ [b green]CREATED[/b green] {key['tier_list_name']} tier list.")

    print("✅ [b green]DONE[/b green]. Check the directory for the tier lists.")
    back_to_main_menu(3) 

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

    # Initialize variables for row and column positions
    row_pos = 0
    col_pos = 0
    increment_size = 200

    """S Tier"""
    # leftmost side - make a square with text inside the square and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (col_pos, row_pos, col_pos + increment_size, row_pos + increment_size),
            fill="red",
        )
        draw.text(
            (col_pos + (increment_size // 3), row_pos + (increment_size // 3)),
            "S Tier",
            font=tier_font,
            fill="white",
        )
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
        draw.rectangle(
            (col_pos, row_pos, col_pos + increment_size, row_pos + increment_size),
            fill="orange",
        )
        draw.text(
            (col_pos + (increment_size // 3), row_pos + (increment_size // 3)),
            "A Tier",
            font=tier_font,
            fill="white",
        )
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
        draw.rectangle(
            (col_pos, row_pos, col_pos + increment_size, row_pos + increment_size),
            fill="yellow",
        )
        draw.text(
            (col_pos + (increment_size // 3), row_pos + (increment_size // 3)),
            "B Tier",
            font=tier_font,
            fill="black",
        )
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
        draw.rectangle(
            (col_pos, row_pos, col_pos + increment_size, row_pos + increment_size),
            fill="green",
        )
        draw.text(
            (col_pos + (increment_size // 3), row_pos + (increment_size // 3)),
            "C Tier",
            font=tier_font,
            fill="black",
        )
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
        draw.rectangle(
            (col_pos, row_pos, col_pos + increment_size, row_pos + increment_size),
            fill="blue",
        )
        draw.text(
            (col_pos + (increment_size // 3), row_pos + (increment_size // 3)),
            "D Tier",
            font=tier_font,
            fill="black",
        )
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
        draw.rectangle(
            (col_pos, row_pos, col_pos + increment_size, row_pos + increment_size),
            fill="pink",
        )
        draw.text(
            (col_pos + (increment_size // 3), row_pos + (increment_size // 3)),
            "E Tier",
            font=tier_font,
            fill="black",
        )
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


# OTHER FUNCTIONS
def add_bold_color(string, color):
    return f"[b {color}]{string}[/b {color}]"
def exit_app():
    clear()
    console = Console()
    console.print(f'[bold green]{Figlet().renderText("See You Again!")}[/bold green]')
    console.print("Thank you for using the CLI MyAnimeList")
    time.sleep(3)
    clear()
    exit()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    figlet_text = Figlet().renderText("WELCOME TO  CLI  MyAnimeList")
    formatted_text = Text.from_markup(f"{figlet_text}\n\nMain Menu")

    # Convert Text object to a string
    startup_question = formatted_text.plain
    options = [
        "See MyAnimeList",
        "Give Me Anime Recommendation",
        "Search Anime Information",
        "Make a Tier List",
        "See Created Tier Lists",
        "EXIT",
    ]
    selected_option, index = pick(options, startup_question, indicator="→")

    if index == 0:
        see_myanimelist()
    elif index == 1:
        recommend_anime()
    elif index == 2:
        search_anime()
    elif index == 3:
        create_tier_list()
    elif index == 4:
        see_tier_lists()
    elif index == 5:
        exit_app()


if __name__ == "__main__":
    main()
