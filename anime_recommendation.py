import argparse
import random

# Replace this with your actual data loading logic
def load_anime_data():
    # For simplicity, using hardcoded data here
    anime_data = [
        {"title": "Hunter X Hunter", "genre": ["Action", "Adventure"]},
        {"title": "Black Bullet", "genre": ["Action", "Adventure"]},
        {"title": "Naruto", "genre": ["Action", "Adventure"]},
        {"title": "One Piece", "genre": ["Action", "Adventure"]},
        {"title": "Fullmetal Alchemist", "genre": ["Action", "Adventure"]},
        {"title": "Ore no Imouto ga Konnani Kawaii Wake ga Nai", "genre": ["Comedy", "Romance"]},
        # Add more anime entries
    ]
    return anime_data

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

def main():
    parser = argparse.ArgumentParser(description="Anime Recommendation CLI")
    parser.add_argument("genre", type=str, help="Specify the genre for anime recommendations")

    args = parser.parse_args()
    genre = args.genre

    recommendations = recommend_anime(genre)

    for anime in recommendations:
        print(f"Title: {anime['title']}")
        print(f"Genre: {', '.join(anime['genre'])}")
        print("=" * 30)

if __name__ == "__main__":
    main()
