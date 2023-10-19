import os
import json
import pytest
from unittest.mock import patch
from rich.table import Table
from rich.text import Text
from project import create_table_from_api, add_bold_color, delete_anime, add_anime_to_json

@pytest.fixture
def api_sample_data():
    return {
            'data':[
                        {
                            'mal_id': 49387,
                            'title': 'Vinland Saga Season 2',
                            'score': 8.81,
                            'genres': [{'name': 'Action'}, {'name': 'Adventure'}, {'name': 'Drama'}],
                            'status': 'Finished Airing'
                        },
                        {
                            'mal_id': 36838,
                            'title': 'Gintama.: Shirogane no Tamashii-hen',
                            'score': 8.81,
                            'genres': [{'name': 'Action'}, {'name': 'Comedy'}, {'name': 'Sci-Fi'}],
                            'status': 'Finished Airing'
                        }
                    ]
            }

def test_create_table_from_api(api_sample_data):
    title = "TestTable"
    result_table = create_table_from_api(api_sample_data, title)

    assert isinstance(result_table, Table)
    assert str(result_table.title) == str(Text(title, style="bold"))
    assert str(result_table.columns[0].header) == str(Text("No.", style="cyan", justify="right"))
    assert str(result_table.columns[1].header) == str(Text("Title", style="magenta"))
    assert str(result_table.columns[2].header) == str(Text("MyAnimeList Score", style="green"))
    assert str(result_table.columns[3].header) == str(Text("Genres", style="yellow"))
    assert str(result_table.columns[4].header) == str(Text("Status", style="cyan"))
    assert str(result_table.rows[0])  == 'Row(style=None, end_section=False)'

def test_add_bold_color():
    string = "test"
    color = "red"
    result_string = add_bold_color(string, color)
    assert result_string == f"[b {color}]{string}[/b {color}]"

@pytest.fixture
def sample_data():
    return [
        {
            "title": "Gintama",
            "score": 8.94,
            "genres": ["Action", "Comedy", "Sci-Fi"],
            "status": "Finished Airing",
            "image_url": "https://cdn.myanimelist.net/images/anime/10/73274.jpg"
        },
        # Add other anime entries as needed
    ]

@pytest.fixture
def sample_anime_data():
    return {
        "data": [
            {
                "title": "Test Anime",
                "score": 9.0,
                "genres": [{"name": "Romance"}],
                "status": "Currently Airing",
                "images": {"jpg": {"image_url": "https://example.com/image.jpg"}}
            }
        ]
    }

@pytest.fixture
def json_file_path(tmp_path):
    return tmp_path / "test_my_anime_list.json"

def test_delete_anime(sample_data, json_file_path, capsys):
    with patch("builtins.input", return_value="Gintama"):
        with open(json_file_path, "w") as json_file:
            json.dump(sample_data, json_file, indent=2)

        result = delete_anime(sample_data)
        captured = capsys.readouterr()
        assert "Are you sure you want to delete 'Gintama' from 'MyAnimeList Table'? (y/n) " in captured.out
        assert os.path.exists(json_file_path)

def test_add_anime_to_json(sample_anime_data, json_file_path, capsys):
    with patch("builtins.input", return_value="1"):
        with open(json_file_path, "w") as json_file:
            json.dump(sample_anime_data["data"], json_file, indent=2)

        result = add_anime_to_json(sample_anime_data)
        captured = capsys.readouterr()
        assert os.path.exists(json_file_path)
