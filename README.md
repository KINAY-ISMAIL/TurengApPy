# This document and code written with NotionAI.

# Screenshot
![TurengLayout](https://github.com/fishmohuman/TurengApPy/blob/main/Screenshot%202024-05-22%20153553.png)
![HistoryLayout](https://github.com/fishmohuman/TurengApPy/blob/main/Screenshot%202024-05-22%20153618.png)

# TurengApPy
TurengApPy, developed with Python and PyQt6, is a user-friendly desktop app serving as a translator tool based on the popular Turkish-English online dictionary, Tureng. It offers hassle-free word and phrase translation through a simple GUI.

## Structure and Layout
The `MainWindow` class is the core of the application. The `__init__` function initializes the app's components. The `QStackedWidget` enables switching between the Tureng and History layouts.

## Key Features and Functions
The key features and functions that enrich the user experience in TurengApPy are:
### Language Toggle
The `toggle_language` function, vital for the application, allows users to switch between English and Turkish translations, meeting diverse user needs.
### Search Function
The `on_search` function is a critical part of the TurengApPy application. It is responsible for numerous tasks:
1. **Search Text Collection**: The function begins by collecting the search text entered by the user in the `search_box`.
2. **Search Text Verification**: The function checks if the search text is empty and throws a warning message if it is.
3. **Performing Search**: If the search text is not empty, the function calls the `perform_search` function, which scrapes the Tureng website for the translation of the entered text. It passes the search text and the language (from the toggle button) as arguments to the `perform_search` function.
4. **Table Update**: The function then updates the `result_table` with the results returned from the `perform_search` function.
5. **Handling Empty Results**: If no results are retrieved, the function informs the user that they haven't entered any text to search.
6. **History Update**: If the search results are not empty and the search wasn't made from the history table, the function updates the history table with the new search. It does this by inserting a new row at the top of the table with the search text and the language.
7. **History Save**: The function then calls the `save_history` function to update the `history.pkl` file with the updated search history.
8. **Search Reset**: Finally, the `search_from_history` flag is reset to False, readying the function for the next user search.
### History Function
Comprises several operations that enhance the application's user interface and experience
1. **History Table Creation:** The PyQt6 widget `history_table` is used to create a table that stores the history of searched words. Each row of the table contains a previously searched word and its translation.
2. **History Table Interaction:** Users can interact with the `history_table`. By clicking on an item (a previous search term) in the table, the application will automatically perform a new search for the clicked term. This feature saves the user from manual re-entry of a previously searched term.
3. **History Storage:** The application uses the `pickle` module to save the search history between sessions. This means that even if the application is closed, the history of the searches will be preserved for the next session.
4. **Clear History:** The `on_clear` function allows users to delete the entire search history from the `history_table`. This provides users with a way to manage their search history, keeping it clean and relevant to their current needs.
5. **Automatic Update:** The history table is automatically updated whenever a new search is performed. The new search term and its translation are added to the top of the table.
These functionalities collectively enhance user experience by providing an efficient and convenient way to revisit and manage past searches.
### Clear History
The `on_clear` function is designed to allow users to clear the search history. This function provides users with the flexibility to manage their search history effectively.
### Database Interaction
The application utilizes the `pickle` module to store the search history locally within a file named 'history.pkl'. The `save_history` function is responsible for this task, ensuring that user search data is safely stored for future sessions.

## How to Run / Getting Started

Running this application requires the PyQt6, BeautifulSoup, and cloudscraper Python libraries. Ensure these libraries are installed before running the application. To run the application, simply execute the `main` function.

To install PyQt6, BeautifulSoup, and cloudscraper libraries, use the following commands in your terminal:

### Prerequisites
This application requires the following Python libraries:

- PyQt6
- BeautifulSoup
- cloudscraper
- pickle
- os
- sys

You can install these prerequisites using pip, which is a package installer for Python. Here's how to do it:

1. PyQt6: `pip install PyQt6`
2. BeautifulSoup: `pip install beautifulsoup4`
3. cloudscraper: `pip install cloudscraper`
4. pickle: This is a built-in module in Python, so no need to install.
5. os: This is a built-in module in Python, so no need to install.
6. sys: This is a built-in module in Python, so no need to install.

Remember to run these commands in your terminal or command prompt. Make sure that pip is updated to the latest version.

After the installation of these libraries, you can run the application by executing the `main` function.

For packaging the application into standalone executable, you can use PyInstaller. 
First, install PyInstaller with the following command:
```
pip install pyinstaller

```
Then, to create an executable without command line interface, navigate to the directory containing your script and run:
```python
cd C:\{Your_Path}\TurengAppy
```
```python
pyinstaller --onefile --noconsole turengappy.py
```
After this, PyInstaller will create a standalone executable in the `dist` directory.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

## License and Disclaimer

This project is distributed under the MIT License. See `LICENSE` for more information.

This application is a standalone project and is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the official Tureng website or any of its subsidiaries or its affiliates.

The official Tureng website can be found at https://www.tureng.com/. The names Tureng, Tureng Dictionary as well as related names, marks, emblems, and images are registered trademarks of their respective owners.

### “Please note that this application is intended for educational purposes only. Its efficiency and accuracy may vary, and it should not be used for heavy-duty or professional translation tasks. It serves as a great learning tool for understanding the implementation of web scraping in Python and developing a GUI using PyQt6.”
