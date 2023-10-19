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
                return f"✅ Anime '{title}' has been deleted from 'my_anime_list.json'"
            elif confirm.lower() == "n":
                return "No changes were made."
    if not found:
        return f"❌ [b red]No anime with the title '{title}' found in MyAnimeList table. Please try again.[/b red]"

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
            json_file_path = "my_anime_list.json"
            if os.path.exists(json_file_path):
                with open(json_file_path, "r") as json_file:
                    existing_data = json.load(json_file)

                if any(anime["title"] == new_anime["title"] for anime in existing_data):
                    return f"❌ [b red]Anime '{new_anime['title']}' is already in 'my_anime_list.json'[/b red]"
                else:
                    existing_data.append(new_anime)
                    with open(json_file_path, "w") as json_file:
                        json.dump(existing_data, json_file, indent=2)
                    return f"✅ Anime '{new_anime['title']}' has been added in 'my_anime_list.json'"
            else:
                existing_data = [new_anime]
                with open(json_file_path, "w") as json_file:
                    json.dump(existing_data, json_file, indent=2)
                return f"✅ Anime '{new_anime['title']}' saved to 'my_anime_list.json'"
        else:
            return "Invalid selection. Please select a valid number."
    except ValueError:
        return "❌ [b red]Invalid input. Please enter a number.[/b red]"
