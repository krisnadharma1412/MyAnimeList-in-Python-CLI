# CLI MyAnimeList
#### Video Demo:  <URL HERE>
#### Description:
CLI MyAnimeList is a program where you can create a list of anime that you want to watch just like in https://myanimelist.net/,
and create a Tier List of anime from S tier to E tier in png image from your list. To collect the anime data i use an API named Jikan which is a Unofficial MyAnimeList REST API. You can see the repository at https://github.com/jikan-me/jikan.
## Main Menu
![Main Menu Interface](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/d297d3a064020b82410622ce2a517fae220f3f90/readme%20img/main_menu.png)
In this Main Menu, you can see "WELCOME TO CLI MyAnimeList" that i created using pyfiglet.
To install  pyfiglet library in Python, you can use the following command:
```sh
pip install pyfiglet
```
There are 5 menus in this main menu, to select the menu i used pick library for creating interactive selection menus.
To install the pick library in Python, you can use the following command:
```sh
pip install pick
```
## Empty List 
When you select the first menu 'See MyAnimeList' and you haven't made a list yet which mean the list is still empty,
there will be a message and force you to back to main menu to add a list first: 
![Empty Table](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/no_list.png)

## Give Me A Anime Recommendation Menu
If you doesn't have an idea what anime you want to add to your list, you can pick the second menu 'Give Me Anime Recommendation'. 
In this menu you can ask the program to recommend an anime based on the genre you want.
If you don't  know what kind of genres that are available, you can see the given example of the genres or you can see the full
list of genres  in the myanimelist link below.
![Display Genre Example](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/recommend1.png)
For example, if you want a romance genre, there will be a list of top 'Romance' anime that have been sorted by the score which you can see below.
![Anime Recommendation Table](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/recommend2.png)
Then the program will ask you if you want to add an anime to your list or not. 
If you input anything beside y or n, the program will show the error messsage.
![Invalid Choice](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/recommend3.png)
Then when you want to add an anime to your list, you need to input the number of the anime that are shown in the table.
There will be an message that the anime saved successfully to your myanimelist file.
![Anime Saved Successfully to Json File](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/recommend4.png)
The list is saved at a json file. Below is the structure of the json file.
![my_anime_list.json structure](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/myanimelistjson.png)
If you select 'n', the program will ask if you want to search for another genre.
The terminal screen will be cleared and go back to the seach genre menu.
![Search Another Genre](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/recommend1.png)
If you doesn't want to search for another genre, you will go back to the main menu.
![Back to Main Menu](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/recommend5.png)

## Seach Anime Information Menu
If you have already know the name of the anime that you want to search for, you can select the third menu which is Search Anime Information Menu.
In this menu, you can search an anime with a keyword that the user inputed.
This is the example of the search result where the user search for an anime with a keyword 'Hunter x Hunter'. 
There will be a list of anime that related to the keyword 'Hunter x Hunter'.
![Search Hunter x Hunter](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/search1.png)
This is the second example of the search result where the user search for an anime with a keyword 'Frieren'. 
There will be a list of anime that related to the keyword 'Frieren'.
![Search Frieren](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/search2.png)
If you want to add an anime to your list, there will be a message that the anime has been added to the list, but if the anime is already in the list, there will be an error message to prevent a duplicate list.
if you want to exit to main menu, you can input 0.

## See MyAnimeList Menu
After you added some anime to your list, you can see the list in the "See MyAnimeList" menu.
![MyAnimeList Table](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/animelist1.png)
It will show the list of anime that displayed using a rich table library.
There are 3 menu options. The first one will redirect the user to go to the search anime information menu.
The second option is you can delete the anime from the list.
![Delete Failed](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/delete1.png)
You need to match the name of the anime from the list to delete the anime or there will be an error message.
![Delete Confirmation](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/delete2.png)
When you input the right title, the program will ask a cofirmation if you really want to delete the anime.
If the anime have been deleted successfully, there will be a message.
![Delete Successful](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/delete3.png)
If you chose the third option, you will going back to main menu.
![Back to Main Menu](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/animelist2.png)

## Create a Tier List Menu
The last menu of this program is that you can make a tier list from the list of anime that are saved in your MyAnimeList.
First the program will ask you to create a title for your tier list file.
![Ask Tier List Title](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/tierlist1.png)
After that the program will ask the user to rank the anime from S tier to E tier. 
![Ask Tier List Anime](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/tierlist2.png)
In order to select the anime, the use need to use the right arrow. The selected anime will have an X symbol.
![X symbol](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/tierlist3.png)
After the user press ENTER,the program will remove the anime that have been selected and the program will ask the user to rank the anime to the A tier until the E tier OR if the anime list is empty and there will be a success message.
![A tier](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/tierlist4.png)
Success Message:
![A tier](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/tierlist5.png)
In order to convert the tier list data (https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/json format), the user need to go to the 'See Created Tier List' option in Main Menu.
Success Message: 
![Tier List Success Message](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/tierlist6.png)
### The Tier List Image Result:
![Tier List Image](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/tierlist7.png)
Thats it, thank you for visiting my project.
![EXIT](https://github.com/krisnadharma1412/MyAnimeList-in-Python-CLI/blob/main/readme%20img/exit.png)
