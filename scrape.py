# user xpath //*[@id="txtAccessOfCode"]
# password xpath //*[@id="txtAccessOfPassword"]

# login button xpath //*[@id="form1"]/input[3]

# football xpath //*[@id="divSportMenu"]/div[3]/div[2]

# NFL xpath //*[@id="divSportMenu"]/div[3]/div[3]/div[3]

import os
from urllib import request

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# # Navigate to the website
# driver.get("https://betus44.com/Logins/007/sites/betus44/index.aspx")

# # Wait for the page to load
# time.sleep(2)

# # Find the username, password fields and login button by their XPath
# username_field = driver.find_element(By.XPATH, '//*[@id="txtAccessOfCode"]')
# password_field = driver.find_element(By.XPATH, '//*[@id="txtAccessOfPassword"]')
# login_button = driver.find_element(By.XPATH, '//*[@id="form1"]/input[3]')

# # Input username and password
# username_field.send_keys("P85908")
# password_field.send_keys("AG08")

# # Click the login button
# login_button.click()

# # Wait for the next page to load
# time.sleep(2)

# # Perform further interactions here...
# football_button = driver.find_element(By.XPATH, '//*[@id="divSportMenu"]/div[3]/div[2]')
# football_button.click()

# time.sleep(2)

# nfl_button = driver.find_element(By.XPATH, '//*[@id="divSportMenu"]/div[3]/div[3]/div[3]')
# nfl_button.click()


# time.sleep(5)

# data = driver.find_element(By.XPATH, "/html/body/form/div[4]/div/div/div/div[2]/div/div[1]/div[3]/div/div").text

# print(data.split('\n'))

data = '''
9/24 GAME
SPREAD  ($50)
ML  ($50)
TOTAL  ($50)
TEAM TOTAL  ($50)
12:00 PM LA Chargers - MIN Vikings (FOX)
451 LA Chargers
+1 -110
  o54 -110
o26.5 -125
u26.5 -105
452 MIN Vikings
-1 -110
  u54 -110
o27 -115
u27 -115
12:00 PM TEN Titans - CLE Browns (CBS)
453 TEN Titans
+3½ -120
+150
o39½ -110
o17.5 -110
u17.5 -120
454 CLE Browns
-3½ Even
-175
u39½ -110
o21.5 -105
u21.5 -125
12:00 PM HOU Texans - JAX Jaguars (FOX)
455 HOU Texans
+8½ -110
+315
o44½ -105
o17 -115
u17 -115
456 JAX Jaguars
-8½ -110
-435
u44½ -115
o27 -115
u27 -115
12:00 PM NE Patriots - NY Jets (CBS)
457 NE Patriots
-2½ -115
-145
o36 -110
o20 105
u20 -135
458 NY Jets
+2½ -105
+125
u36 -110
o17.5 105
u17.5 -135
12:00 PM NO Saints - GB Packers (FOX)
459 NO Saints
+1½ -110
Even
o42½ -110
o20.5 -110
u20.5 -120
460 GB Packers
-1½ -110
-120
u42½ -110
o21.5 -110
u21.5 -120
12:00 PM DEN Broncos - MIA Dolphins (CBS)
461 DEN Broncos
+6½ -110
+225
o48 -110
o20.5 -110
u20.5 -120
462 MIA Dolphins
-6½ -110
-285
u48 -110
o27.5 -110
u27.5 -120
12:00 PM BUF Bills - WAS Commanders (CBS)
463 BUF Bills
-6½ -110
-275
o43 -115
o24.5 -110
u24.5 -120
464 WAS Commanders
+6½ -110
+220
u43 -105
o17.5 -115
u17.5 -115
12:00 PM ATL Falcons - DET Lions (FOX)
465 ATL Falcons
+3½ -120
+145
o46 -110
o21 -115
u21 -115
466 DET Lions
-3½ Even
-170
u46 -110
o24.5 -105
u24.5 -125
12:00 PM IND Colts - BAL Ravens (CBS)
467 IND Colts
+8 -110
+295
o44 -110
o17.5 100
u17.5 -130
468 BAL Ravens
-8 -110
-395
u44 -110
o27 -110
u27 -120
3:05 PM CAR Panthers - SEA Seahawks (CBS)
469 CAR Panthers
+6 -105
+220
o42 -110
o17.5 -105
u17.5 -125
470 SEA Seahawks
-6 -115
-275
u42 -110
o24.5 105
u24.5 -135
3:25 PM DAL Cowboys - ARI Cardinals (FOX)
471 DAL Cowboys
-12½ -110
-725
o43 -110
o27.5 -110
u27.5 -120
472 ARI Cardinals
+12½ -110
+425
u43 -110
o14.5 -120
u14.5 -110
3:25 PM CHI Bears - KC Chiefs (FOX)
473 CHI Bears
+12½ -110
+470
o48 -110
o17.5 100
u17.5 -130
474 KC Chiefs
-12½ -110
-770
u48 -110
o31 105
u31 -135
7:20 PM PIT Steelers - LV Raiders (NBC)
475 PIT Steelers
+2½ -105
+120
o43 -110
o20.5 -105
u20.5 -125
476 LV Raiders
-2½ -115
-140
u43 -110
o22.5 -120
u22.5 -110
Sunday Night Football
9/24 1ST HALF
SPREAD  ($50)
ML  ($50)
TOTAL  ($50)
TEAM TOTAL  ($50)
12:00 PM LA Chargers - MIN Vikings (FOX)
451 LA Chargers
PK -105
  o26½ -115
o13.5 -110
u13.5 -130
452 MIN Vikings
PK -115
  u26½ -105
o13.5 -115
u13.5 -125
12:00 PM TEN Titans - CLE Browns (CBS)
453 TEN Titans
+2½ -105
+135
o19½ -110
o7.5 -105
u7.5 -135
454 CLE Browns
-2½ -115
-155
u19½ -110
o9.5 -155
u9.5 115
12:00 PM HOU Texans - JAX Jaguars (FOX)
455 HOU Texans
+5½ -110
+220
o22½ -110
o9.5 105
u9.5 -145
456 JAX Jaguars
-5½ -110
-275
u22½ -110
o13.5 -125
u13.5 -115
12:00 PM NE Patriots - NY Jets (CBS)
457 NE Patriots
-½ -110
-130
o18½ -110
o9.5 -135
u9.5 -105
458 NY Jets
+½ -110
+110
u18½ -110
o7.5 -115
u7.5 -125
12:00 PM NO Saints - GB Packers (FOX)
459 NO Saints
PK -105
  o21 -110
o9.5 -145
u9.5 105
460 GB Packers
PK -115
  u21 -110
o10.5 105
u10.5 -145
12:00 PM DEN Broncos - MIA Dolphins (CBS)
461 DEN Broncos
+3½ -105
+170
o24 Even
o9.5 -140
u9.5 100
462 MIA Dolphins
-3½ -115
-205
u24 -120
o13.5 -130
u13.5 -110
12:00 PM BUF Bills - WAS Commanders (CBS)
463 BUF Bills
-3½ -105
-195
o21½ -110
o12.5 -130
u12.5 -110
464 WAS Commanders
+3½ -115
+165
u21½ -110
o9.5 -115
u9.5 -125
12:00 PM ATL Falcons - DET Lions (FOX)
465 ATL Falcons
+2 -110
+140
o23 -105
o9.5 -140
u9.5 100
466 DET Lions
-2 -110
-160
u23 -115
o12.5 -120
u12.5 -120
12:00 PM IND Colts - BAL Ravens (CBS)
467 IND Colts
+5 -110
+205
o22½ -110
o7.5 -110
u7.5 -130
468 BAL Ravens
-5 -110
-255
u22½ -110
o13.5 -125
u13.5 -115
3:05 PM CAR Panthers - SEA Seahawks (CBS)
469 CAR Panthers
+3½ -110
+170
o20½ -110
o9.5 -105
u9.5 -135
470 SEA Seahawks
-3½ -110
-205
u20½ -110
o12.5 -125
u12.5 -115
3:25 PM DAL Cowboys - ARI Cardinals (FOX)
471 DAL Cowboys
-7 -120
-415
o22 -110
o14.5 -105
u14.5 -135
472 ARI Cardinals
+7 Even
+305
u22 -110
o6.5 -145
u6.5 105
3:25 PM CHI Bears - KC Chiefs (FOX)
473 CHI Bears
+7 -110
+290
o24 -105
o7.5 -105
u7.5 -135
474 KC Chiefs
-7 -110
-385
u24 -115
o16.5 -110
u16.5 -130
7:20 PM PIT Steelers - LV Raiders (NBC)
475 PIT Steelers
+½ -110
+110
o21 -115
o9.5 -140
u9.5 100
476 LV Raiders
-½ -110
-130
u21 -105
o12.5 -110
u12.5 -130
9/25 GAME
SPREAD  ($50)
ML  ($50)
TOTAL  ($50)
TEAM TOTAL  ($50)
6:15 PM PHI Eagles - TB Buccaneers (ABC)
477 PHI Eagles
-5 -110
-220
o46 -110
o25.5 -115
u25.5 -115
478 TB Buccaneers
+5 -110
+180
u46 -110
o20.5 -105
u20.5 -125
Monday Night Football
7:15 PM LA Rams - CIN Bengals (ESPN)
479 LA Rams
+3 -110
+130
o44 -110
o20.5 -115
u20.5 -115
480 CIN Bengals
-3 -110
-150
u44 -110
o24 110
u24 -140
Monday Night Football
9/25 1ST HALF
SPREAD  ($50)
ML  ($50)
TOTAL  ($50)
TEAM TOTAL  ($50)
6:15 PM PHI Eagles - TB Buccaneers (ABC)
477 PHI Eagles
-3 -110
-185
o22½ -115
o12.5 -130
u12.5 -110
478 TB Buccaneers
+3 -110
+155
u22½ -105
o9.5 -125
u9.5 -115
7:15 PM LA Rams - CIN Bengals (ESPN)
479 LA Rams
+1 -110
+115
o21½ -110
o9.5 -135
u9.5 -105
480 CIN Bengals
-1 -110
-135
u21½ -110

'''

data = data.split("\n")

count = len(data)

for x in range(0,count):
    if len(data[x]) < 3: 
        continue
    if data[x][0].isdigit() and data[x][1].isdigit() and data[x][2].isdigit():
        # print("START")
        # print(data[x])
        # print(data[x+1])
        # print(data[x+2])
        # print(data[x+3])
        # print(data[x+4])
        # print(data[x+5])
        # print("END")
        team = data[x]
        # is_home = 
        spread = data[x + 1].split(" ")[0]
        ml = data[x + 1].split(" ")[1]
        print(team)
        print(spread)
        print(ml)
        # team_over = data[x]
        # team_over_odds = data[x]
        # team_under = data[x]
        # team_under_odds = data[x]
        # total_over = data[x]
        # total_over_odds = data[x]
        # total_under = data[x]
        # total_under_odds = data[x]
        # opponent = 

# for x in data: 
#     if len(x) < 3: 
#         continue
#     if x[0].isdigit() and x[1].isdigit() and x[2].isdigit():
#         print(x)


# Close the browser
# driver.quit()
