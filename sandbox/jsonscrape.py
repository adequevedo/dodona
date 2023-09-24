import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import csv
import json
from collections import defaultdict
from datetime import datetime

# Clean up CSV
def clean_csv(filename):
    cleanfilename = "cleaned_" + filename
    print('cleaning csv', filename  )
    cleaned_rows = []
    seen = set()
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            cleaned_row = [cell.replace("�", ".5") for cell in row]
            row_str = ",".join(cleaned_row)
            if row_str not in seen:
                cleaned_rows.append(cleaned_row)
                seen.add(row_str)
   
    with open(cleanfilename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(cleaned_rows)

# Clean up JSON
def clean_json(filename):
    cleanfilename = "cleaned_" + filename
    print('cleaning json', filename)
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
    
    for game_key, game_value in data['data'].items():
        for team in game_value:
            team["betting_data"] = [x.replace("�", ".5") for x in team["betting_data"]]
            team["betting_data"] = [x.replace("\u00bd", ".5") for x in team["betting_data"]]
            
            
    
    with open(cleanfilename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def parse_data(data_list, csvfilename, jsonfilename):
    parsed_data = {}
    game_time, teams = None, None
    current_team_data = None

    for line in data_list:
        if not line.strip():
            continue

        if "GAME" in line:
            # Skip lines that are just game markers
            continue

        if "PM" in line or "AM" in line:
            game_time, teams = line.split(" ", 1)
            current_team_data = []
            parsed_data[f"{game_time}, {teams}"] = current_team_data
            continue

        if line[0].isdigit() and line[1].isdigit() and line[2].isdigit():
            team_number, *rest = line.split(" ")
            team_name = " ".join(rest)
            current_team_data.append({
                "team_number": team_number,
                "team_name": team_name,
                "betting_data": []
            })
            continue

        if current_team_data:
            # Don't append special lines like "Monday Night Football" to betting data
            if "Football" not in line and "HALF" not in line:
                current_team_data[-1]['betting_data'].append(line)
    # Write parsed data to CSV
    with open(csvfilename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Game Time and Teams", "Team Number", "Team Name", "Spread", "Moneyline", "Total Over", "Total Over Odds", "Team Total Over", "Team Total Over Odds", "Team Total Under", "Team Total Under Odds"])
        
        for key, team_data_list in parsed_data.items():
            for team_data in team_data_list:
                csvwriter.writerow([key, team_data["team_number"], team_data["team_name"], *team_data["betting_data"]])

    # Write parsed data to JSON with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data = {
        "timestamp": timestamp,
        "data": parsed_data
    }
    with open(jsonfilename, 'w') as jsonfile:
        json.dump(json_data, jsonfile, indent=4)

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://betus44.com/Logins/007/sites/betus44/index.aspx")

    time.sleep(2)

    username_field = driver.find_element(By.XPATH, '//*[@id="txtAccessOfCode"]')
    password_field = driver.find_element(By.XPATH, '//*[@id="txtAccessOfPassword"]')
    login_button = driver.find_element(By.XPATH, '//*[@id="form1"]/input[3]')

    username_field.send_keys("")
    password_field.send_keys("")

    login_button.click()

    time.sleep(2)

    football_button = driver.find_element(By.XPATH, '//*[@id="divSportMenu"]/div[3]/div[2]')
    football_button.click()

    time.sleep(2)

    nfl_button = driver.find_element(By.XPATH, '//*[@id="divSportMenu"]/div[3]/div[3]/div[3]')
    nfl_button.click()

    time.sleep(5)

    data = driver.find_element(By.XPATH, "/html/body/form/div[4]/div/div/div/div[2]/div/div[1]/div[3]/div/div").text
    data_lines = data.split('\n')
    
    # Remove duplicates and replace unknown characters
    processed_lines = set()
    cleaned_data = []
    for line in data_lines:
        line = line.replace("�", ".5")  # Replace unknown char with .5
        line = line.replace("\u00bd", ".5")  # Replace half symbol with .5
        
        if line in processed_lines:
            continue
        processed_lines.add(line)
        cleaned_data.append(line)
    
    csvfilename = "csv_data.csv"
    jsonfilename = "json_data.json"
        
    print(cleaned_data)  # Debugging, print cleaned data
    
    # Use cleaned_data here instead of data_lines
    parse_data(cleaned_data, csvfilename, jsonfilename)  
    
    # Add cleanup steps
    #clean_csv(csvfilename)
    #clean_json(jsonfilename)
    
    time.sleep(3)

except Exception as e:
    print(f"An error occurred: {e}")