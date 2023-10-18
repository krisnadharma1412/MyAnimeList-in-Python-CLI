# If you want to use PrettyTable instead RichTable, you can use the following code:
from prettytable import PrettyTable

def see_myanimelist():
    # # Using Pretty Table 
    # # Create a PrettyTable instance
    # table = PrettyTable()
    # # Define the table columns
    # table.field_names = ["No.","Title", "MyAnimeList Score", "Genres", "Status"]
    
    # for i in range(len(data)):
    #     genres = ', '.join(data[i]['genres'])
    #     table.add_row([i+1,data[i]['title'], data[i]['score'], genres, data[i]['status']])
    
    # # Figlet header
    # fig = Figlet()
    # header = fig.renderText("MyAnimeList")
    # print(header)
    # print(f"\n{table}\n\n")

# def create_table_from_api(data):
#     # Create a PrettyTable instance
#     table = PrettyTable()
#     # Define the table columns
#     table.field_names = ["No.","Title", "MyAnimeList Score", "Genres", "Status"]
    
#     # Extracting Data
#     for i in range(len(data['data'])):
#         anime_info = data['data'][i]
#         title = anime_info['title']
#         score = anime_info['score']
#         genres = [
#             genre['name'] for genre in anime_info['genres']
#         ]
#         genres = ', '.join(genres)
#         status = anime_info['status']

#         # Add a row to the table
#         table.add_row([i+1,title, score, genres, status])
#     return table