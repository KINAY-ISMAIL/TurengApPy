from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt
from bs4 import BeautifulSoup as bs
import cloudscraper
import pickle
import os
import sys

    # Main Layout
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TurengApPy")
        self.resize(448, 448)

        layout = QVBoxLayout()

        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(0)

        self.tureng_button = QPushButton("Tureng")
        self.history_button = QPushButton("History")

        nav_layout.addWidget(self.tureng_button)
        nav_layout.addWidget(self.history_button)

        layout.addLayout(nav_layout)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Tureng Layout
        self.tureng_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        self.search_button = QPushButton("🔍")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search")
        self.search_box.returnPressed.connect(self.on_search)
        self.toggle_button = QPushButton("EN-TR")
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.toggle_button)
        self.tureng_layout.addLayout(search_layout)
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.horizontalHeader().hide()
        self.result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tureng_layout.addWidget(self.result_table)
        self.tureng_page = QWidget()
        self.tureng_page.setLayout(self.tureng_layout)
        self.stack.addWidget(self.tureng_page)

        

        # History Layout
        self.history_layout = QVBoxLayout()
        self.clear_button = QPushButton("Clear")
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(2)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setHorizontalHeaderLabels(["Word", "Language"])
        self.history_layout.addWidget(self.clear_button)
        self.history_layout.addWidget(self.history_table)
        self.history_page = QWidget()
        self.history_page.setLayout(self.history_layout)
        self.stack.addWidget(self.history_page)
        self.setLayout(layout)
        
        # Database
        print("Files in current directory:", os.listdir('.'))
        try:
            if 'history.pkl' in os.listdir('.'):
                print("Found 'history.pkl'. Trying to open and load it.")
            
                print("Is 'history.pkl' a symbolic link?", os.path.islink('history.pkl'))

            
                print("Permissions of 'history.pkl':", os.stat('history.pkl'))

                with open('history.pkl', 'rb') as f:
                    history = pickle.load(f)
                if not history:
                    raise EOFError
                for row in reversed(history):
                    self.history_table.insertRow(0)
                    self.history_table.setItem(0, 0, QTableWidgetItem(row[0])) 
                    self.history_table.setItem(0, 1, QTableWidgetItem(row[1])) 
            else:
                raise FileNotFoundError
        except (EOFError, pickle.UnpicklingError):
            print("'history.pkl' is empty or contains corrupt data.")
            self.history_table.setRowCount(1)
            self.history_table.setItem(0, 0, QTableWidgetItem(''))
            self.history_table.setItem(0, 1, QTableWidgetItem('No history yet! Make a query.'))
            self.history_table.setItem(0, 2, QTableWidgetItem(''))
        except FileNotFoundError:
            print("'history.pkl' not found.")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Database File Not Found")
            msg.setInformativeText("Please create a database file!")
            create_button = msg.addButton('Create', QMessageBox.ButtonRole.AcceptRole)
            cancel_button = msg.addButton('Cancel', QMessageBox.ButtonRole.RejectRole)
            msg.exec()

            clicked_button = msg.clickedButton()
            if clicked_button == create_button:
                try:
                    with open('history.pkl', 'wb') as f:
                        pickle.dump([], f)
                    print("'history.pkl' created successfully.")
                    self.history_table.setRowCount(1)
                    self.history_table.setItem(0, 0, QTableWidgetItem(''))
                    self.history_table.setItem(0, 1, QTableWidgetItem('No history yet! Make a query.'))
                    self.history_table.setItem(0, 2, QTableWidgetItem(''))
                except Exception as e:
                    print("An error occured while creating 'history.pkl':", str(e))
            else:
                sys.exit()

        # Connectors
        self.tureng_button.clicked.connect(self.on_tureng)
        self.history_button.clicked.connect(self.on_history)
        self.search_button.clicked.connect(self.on_search)
        self.clear_button.clicked.connect(self.on_clear)
        self.toggle_button.clicked.connect(self.toggle_language)
        self.search_from_history = False
        self.history_table.itemClicked.connect(self.on_history_item_clicked)

    # Functions
    def on_history_item_clicked(self, item):
        self.search_from_history = True
        
        if item.text() == "No history yet! Make a query.":
            return

        
        language = self.history_table.item(item.row(), 1).text()
        
        
        word = self.history_table.item(item.row(), 0).text()

        
        self.toggle_button.setText(language)
        
        
        self.search_box.setText(word)

        self.on_search()
        self.on_home()
        
    def on_home(self):
        self.stack.setCurrentWidget(self.tureng_page)

    def on_tureng(self):
        self.stack.setCurrentWidget(self.tureng_page)

    def on_history(self):
        self.stack.setCurrentWidget(self.history_page)

            # Search Function (based on Tureng)       
    def on_search(self):
        
        search_text = self.search_box.text()
        
        if search_text.startswith("There is no such thing as a"):
            self.search_box.clear()
            return
        if search_text.startswith("Please enter a search term"):
            self.search_box.clear()
            return
        
        self.search_box.clear()
       
        results = []
        

        
        if search_text.strip() != "":
            
            language = self.toggle_button.text()

            
            results = self.perform_search(search_text, language)

            
            self.result_table.setRowCount(0)

            
            for result in results:
                rowPosition = self.result_table.rowCount()
                self.result_table.insertRow(rowPosition)
                
                for col in range(3):
                    item = QTableWidgetItem(result[col])
                    
                    if len(result[col]) > 17:
                        item.setToolTip(result[col])
                        
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                    self.result_table.setItem(rowPosition, col, item)

        else:
            QMessageBox.information(self, 'Blank Search', 'You have not entered any text to search.')

        
        if results and not self.search_from_history and results[0] != f'There is no such thing as a {search_text}.' and results[0][0] != "Please enter a search term.":
            
            if self.history_table.item(0,1) and self.history_table.item(0,1).text() == 'No history yet! Make a query.':
                self.history_table.removeRow(0)

            if (self.history_table.rowCount() > 0 and
                self.history_table.item(0, 0).text() == search_text and
                self.history_table.item(0, 1).text() == language):
                return

            rowPosition = self.history_table.rowCount()
            self.history_table.insertRow(0)
            self.history_table.setItem(0, 0, QTableWidgetItem(search_text))
            self.history_table.setItem(0, 1, QTableWidgetItem(language))
            self.save_history()

        
        self.search_from_history = False

    
            # History Clear
    def on_clear(self):
        self.history_table.setRowCount(0)
        self.save_history()
        
            # Database
    def save_history(self):
        history = []
        for row in range(self.history_table.rowCount()):
            history.append([
                self.history_table.item(row, 0).text(),
                self.history_table.item(row, 1).text()
            ])
        with open(os.path.join(os.getcwd(), 'history.pkl'), 'wb') as f:
            pickle.dump(history, f)

            # Tureng Toggle Button
    def toggle_language(self):
        if self.toggle_button.text() == 'EN-TR':
            self.toggle_button.setText('TR-EN')
        else:
            self.toggle_button.setText('EN-TR')

    def onlistWidget_itemClicked(self, item):
        if item.text() == "Not history yet! Make a query":
            return
        
            # Tureng Search Function
    def perform_search(self, search_text, language):
        if search_text == "No history yet! Make a query.":
            return []
        
        results = []

        scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
        url = f"https://tureng.com/tr/turkce-ingilizce/{search_text}"

        info = scraper.get(url).text

        soup = bs(info, "html.parser")

        if soup.find("h1").text == "Maybe the correct one is" or soup.find("h1").text == "Sanırız yanlış oldu, doğrusu şunlar olabilir mi?":
            self.search_box.setText(f'There is no such thing as a {search_text}.')

        else:
            table = soup.find('table', {'class': 'table table-hover table-striped searchResultsTable'})
            if table:  
                table_tr = table.find_all('tr')
                for i in range(3, len(table_tr)): 
                    category_row = table_tr[i].find_previous_sibling('tr', {'class': 'mobile-category-row'})
                    category = category_row.find('b').text if category_row else None
                    turkish = table_tr[i].find('td', {'class': 'tr ts'})
                    english = table_tr[i].find('td', {'class': 'en tm'})

                    if turkish and english and category: 
                        results.append((category, turkish.text.strip(), english.text.strip()))
            else:
                 if not results or (len(results) == 1 and results[0][0] == "Please enter a search term."):
                    self.search_box.setText("Please enter a search term.")
                    return []
        return results



        
def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
