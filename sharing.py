import webbrowser
import urllib.parse
from pathlib import Path

def share(choice, file):
    # The text to include in the email
    with open(file, 'r') as file:
        file_content = file.read()

    # URL encode the text
    encoded_text = urllib.parse.quote(file_content)

    # Create an Outlook compose URL with the text
    outlook_url = f"https://outlook.live.com/owa/?path=/mail/action/compose&body={encoded_text}"

    # Create a Gmail compose URL with the text
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&body={encoded_text}"

    if choice == "Gmail":      
        # Open the Gmail compose URL in the default browser
        webbrowser.open(gmail_url)

    if choice == "Outlook":
        # Open the Outlook compose URL in the default browser
        webbrowser.open(outlook_url)
    else:
        return False
    
def save(text):
    puzzle = text
    # Open the file in write mode
    with open('shared_puzzle.txt', 'w') as file:
        # Write the text to the file
        file.write(puzzle.strip())
        print("Done")
        
def test():        
    choose = input("Choose")
    # Check if the file exists
    if file_path.exists():
        if share(choose, file) == False:
            print("Try again")
            test()
    else:
        print("The file does not exist.")
        test()

    
file = 'sudoku_9x9_easy.txt'
file_path = Path('C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python311\\sudoku\\sudoku_9x9_easy.txt')

# Check if the file exists
if file_path.exists():
    print("The file exists.")
else:
    print("The file does not exist.")
    
#test()
