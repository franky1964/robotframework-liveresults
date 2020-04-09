# Robotframework Live Results
Robot Framework Listener to get Live Results in a web page while RF execution is in progress [![HitCount](http://hits.dwyl.io/ franky1964/RF-LiveResults.svg)](http://hits.dwyl.io/a franky1964/RF-LiveResults)

    > Uses ROBOT_LISTENER_API_VERSION = 3
    
Steps to Use:

 - Step 1: Download or clone this repo
 
 - Step 2: Copy `LiveResults.py` to your project

 - Step 3: Execute test case/suites using LiveResults Listenr
   > - `robot --listener LiveResults.py Tests` 

 - Step 4: Optional: A new browser will be opened with logs
   > Note: Page refresh's for every 5 seconds.
   > - Users can modify reload time by using
   > - `<meta http-equiv="refresh" content="5" >`

---

Available Results:

 - LogListener.py --> Suite and Test status
    > Uses ROBOT_LISTENER_API_VERSION = 3

---

*Screenshot*

<img src="/LiveLogs.jpg" alt="LiveLogs">
