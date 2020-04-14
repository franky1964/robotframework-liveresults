# Robotframework Live Results
Robot Framework Listener to get Live Results in a web page while RF execution is in progress
[![HitCount](http://hits.dwyl.com/franky1964/RF-LiveResults.svg)](http://hits.dwyl.com/franky1964/RF-LiveResults)

> Uses ROBOT_LISTENER_API_VERSION = 3
    
Steps to Use:

 - Step 1: Download or clone this repo
 
 - Step 2: Copy `LiveResults.py` to your project or use 'pip install git+https://github.com/franky1964/RF-LiveResults.git'

 - Step 3: Execute test case/suites using LiveResults Listenr
   > - `robot --listener LiveResults Tests` 

 - Step 4: Optional: A new browser will be opened with logs
   > Note: Page refresh's for every 5 seconds.
   > - Users can modify reload time by using
   > - `<meta http-equiv="refresh" content="5" >`
   > - Users can specify the filename of the page:          robot --listener LiveResults:myPage.html Tests
   > - Users can specify the option for browser is opened:  robot --listener LiveResults:myPage.html Tests
   > - Users can specify the filename of the page:          robot --listener LiveResults:myPage.html Tests
   

---

Available Results:

 - LogListener.py --> Suite and Test status
    > Uses ROBOT_LISTENER_API_VERSION = 3

---

*Screenshot*

<img src="/LiveLogs.jpg" alt="LiveLogs">
