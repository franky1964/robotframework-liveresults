import os
import datetime
import webbrowser
import pathlib
from distutils.util import strtobool
from robot.libraries.BuiltIn import BuiltIn

__version__ = '2.0'

class LiveResults:
    """|
|
===================================================
robotframework-liveresults
===================================================
Live Results ... 
|
Installation
------------
If you already have Python >= 3.6 with pip and git installed, you can simply
run:
``pip install --upgrade git+https://github.com/franky1964/robotframework-liveresults.git``
"""
	
    ROBOT_LISTENER_API_VERSION = 3
#https://stackoverflow.com/questions/28435865/can-i-stop-a-meta-refresh-using-javascript

 
    def __init__(self, show='False', capture='False', refresh=15, filename='RF_Live_Results.html'):
        print ("LiveResults - Parameter 'show' ist set to: " + str(show))
        print ("LiveResults - Parameter 'capture' ist set to: " + str(capture))
        print ("LiveResults - Parameter 'filename' ist set to: " + filename)
        print ("LiveResults - Parameter 'refresh' ist set to: " + str(refresh))
        self.ROBOT_PARENT_SUITE_SETUP_FAILED = 'Parent suite setup failed'
        self.RF_LIVE_LOGGING_INITIAL_TITLE = 'Robot Framework Live Results (Initialize...)'
        self.RF_LIVE_LOGGING_RUNNING_TITLE = 'Robot Framework Live Results (Running...)'
        self.RF_LIVE_LOGGING_FINAL_TITLE = 'Robot Framework Live Results (Execution completed)'
        self.RF_LIVE_LOGGING_ICON_PATH_1 = 'https://avatars2.githubusercontent.com/u/574284?s=200&v=4'
        self.RF_LIVE_LOGGING_ICON_PATH_2 = 'http://www.imbus.de/fileadmin/Resources/Public/Images/social.png'
        self.PRE_RUNNER = 0
        self.liveLogFilepath = filename
        self.openBrowser = strtobool(show)
        self.makeVideo = strtobool(capture)
        self.reportFile = None
        self.logFile = None
        self.expected = 0
        self.executed = 0
        self.skipped = 0
        self.blocked = 0
        self.passed = 0
        self.failed = 0
        self.refresh = refresh
        self.refreshTimer = "http-equiv='refresh' content='" + str(refresh) + "'"
        self.refreshStopped = "http-equiv='refresh' content='5000'"
        self.content = ""
        self.videoFilename = ""
        self.videoPath= ""
        self.statusColors = {'yellow':'#FFFF66', 'green':'#32CD32', 'red':'#CD5C5C', 'blue':'#87CEFA'}
        self.videoFoldername = "Videos"
        self.buttonStopRefresh = "<button class='btn' value= 'Stop Reload' onclick= 'pauseshow()'>Stop Refresh</button>"
        self.html_text = """
        <html>
	<title>Robot Framework Live Results</title>
	<meta """ + self.refreshTimer + """>
		<link href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" rel="stylesheet" />
		<link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" />
		<script src="https://code.jquery.com/jquery-3.3.1.js" type="text/javascript"></script>
		<script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js" type="text/javascript"></script>
		<script src="https://cdn.datatables.net/buttons/1.5.2/js/dataTables.buttons.min.js" type="text/javascript"></script>
		<script src="https://cdn.datatables.net/buttons/1.5.2/js/buttons.flash.min.js" type="text/javascript"></script>
		<script>$(document).ready(function() {$('#live').DataTable({"order": [[0, "desc"]],"lengthMenu": [[10,50,100, -1], [10,50,100, "All"]]});});</script>
		<script type="text/javascript">function pauseshow(){window.stop();}</script>
	</html>
	<body>
		<table align="center" style="table-layout: fixed ;">
			<td style="text-align: left;">
				<button class="btn" value="Refresh Page" onClick="window.location.href=window.location.href">Reload Page</button>
			</td>
			<td>
				&emsp;<a><img src="__iconLink1__" style="height:10vh;max-width:98%;"></a>&emsp;
			</td>
			<td>
				<h3 style="color:#009688;" style="text-align: center;">
					<b>__title__</b>
				</h3>__refreshInfo__
			</td>
			<td>&emsp;<td>
			<td>__buttonStopRefresh__</td>
			<td>
				<a><img src="__iconLink2__" style="height:10vh;max-width:98%;"></a> 
			</td>
		</table>
		<table class="table table-bordered"
			<thead>
				<tr style="text-align:center">
					<th>Log File:</th>
					<th>Report File:</th>
					<th>Tests to be executed:</th>
					<th>Test already executed:</th>
					<th>Tests Skipped:</th>
					<th>Tests Blocked:</th>
					<th>Tests Passed:</th>
					<th>Tests Failed:</th>
				</tr>
			</thead>
			<tbody>
				<tr style="text-align:center">
					<td><b>__logFile__</b></td>
					<td><b>__reportFile__</b></td>
					<td><b>__expected__</b></td>
					<td><b>__executed__</b></td>
					<td bgcolor='""" + self.statusColors['blue'] + """'><b>__skipped__</b></td>
					<td bgcolor='""" + self.statusColors['yellow'] + """'><b>__blocked__</b></td>
					<td bgcolor='""" + self.statusColors['green'] + """'><b>__passed__</b></td>
					<td bgcolor='""" + self.statusColors['red'] + """'><b>__failed__</b></td>
				</tr>
			</tbody>
		</table>
		<table id="live" class="table table-striped table-bordered">
			<thead>
				<tr>
					<th>Start Time</th>
					<th>Elapsed</th>
					<th>Parent Suite Name</th>
					<th>Test Name</th>
					<th>Tags</th>
					<th>Critical</th>
					<th>Status</th>
					<th>Message</th>
				</tr>
			</thead>
			<tbody>
			__content__        
        """
        self.html_text = self.html_text.replace ("__iconLink1__", self.RF_LIVE_LOGGING_ICON_PATH_1)
        self.html_text = self.html_text.replace ("__iconLink2__", self.RF_LIVE_LOGGING_ICON_PATH_2)
        _update_content(self, self.html_text, self.RF_LIVE_LOGGING_INITIAL_TITLE)

    def start_suite(self, suite, result):
        # count expected total testcases and open bowser only on top level
        if self.PRE_RUNNER == 0:
            self.PRE_RUNNER = 1
            self.logFile = BuiltIn().get_variable_value("${LOG FILE}")
            self.reportFile = BuiltIn().get_variable_value("${REPORT FILE}")
            self.liveLogFilepath = os.path.join(pathlib.Path(self.reportFile).parent.absolute(), self.liveLogFilepath)
            self.videoPath = os.path.join(pathlib.Path(self.reportFile).parent.absolute(), self.videoFoldername)
            self.logFile = os.path.basename(self.logFile)
            self.reportFile = os.path.basename(self.reportFile)
            self.expected = suite.test_count
            _update_content(self, self.html_text, self.RF_LIVE_LOGGING_RUNNING_TITLE)
            if self.openBrowser:
              print ("LiveResults - Default browser is opened with page: " + self.liveLogFilepath)
              _open_liveLogs(self, self.liveLogFilepath)
            if self.makeVideo:
              try:
                BuiltIn().import_library('ScreenCapLibrary')
                self.screencaplib = BuiltIn().get_library_instance('ScreenCapLibrary')
                print ("LiveResults - Videos will be saved in : " + self.videoPath)
                if not os.path.exists(self.videoPath):
                  os.makedirs(self.videoPath)
              except:
                self.makeVideo = False
                BuiltIn().log('LiveResults: To get videos for test case executions please install the following library: <a href="https://github.com/mihaiparvu/ScreenCapLibrary">ScreenCapLibrary</a>','ERROR','HTML')
        self.test_count = len(suite.tests)
        if self.test_count != 0:
            self.suite_name = suite.name

    def start_test(self, data, test):
        self.test_start_time = _get_current_date_time('%Y-%m-%d %H:%M:%S.%f',True)
        if (self.makeVideo):
            self.test_case_name = str(test)
            self.screencaplib.set_screenshot_directory(self.videoPath)
            self.screencaplib.start_video_recording(name=str(self.test_case_name))
            self.videoFilename = os.path.join(self.videoFoldername, self.test_case_name + "_1.webm")
            #self.videoFilename = self.videoFilename.replace(' ', '%20')

    def end_test(self, data, test):
        if self.test_count != 0:
            self.executed = self.executed + 1
            self.elapsed = str(datetime.timedelta(milliseconds=test.elapsedtime))[:-3]
            tags = test.tags
            if len(tags) == 0: tags = ""
            status = test.status
            if test.status == 'PASS':
                self.passed = self.passed + 1
                statusColor = self.statusColors['green']
            else:
                self.failed = self.failed + 1
                statusColor = self.statusColors['red']
            if test.message.startswith(self.ROBOT_PARENT_SUITE_SETUP_FAILED):
                self.failed = self.failed - 1
                self.blocked = self.blocked + 1
                statusColor = self.statusColors['yellow']
                status = 'BLOCKED'
            #statusLink = "<a href='file:///" + self.logFile + "#" + test.id + "' target='_blank'>" + status + "</a>"
            statusLink = "<a href='" + self.logFile + "#" + test.id + "' target='_blank'>" + status + "</a>"
            criticalLink = str(test.critical)
            #if self.makeVideo: criticalLink = "<a href='file:///" + self.videoFilename + "' target='_blank'>" + criticalLink + "</a>"
            if self.makeVideo:
               criticalLink = "<a href='" + self.videoFilename + "' target='_blank'>" + criticalLink + "</a>"
               self.screencaplib.stop_video_recording()
            test_detail_message = """
					<tr>
						<td style="text-align: left;max-width: 70px;">%s</td>
						<td style="text-align: left;max-width: 70px;">%s</td>
						<td style="text-align: left;max-width: 190px;">%s</td>
						<td style="text-align: left;max-width: 210px;">%s</td>
						<td style="text-align: left;max-width: 140px;">%s</td>
						<td style="text-align: center;">%s</td>
						<td bgcolor='%s' style="text-align: center;">%s</td>
						<td style="text-align: left;max-width: 250px;">%s</td>
					</tr>
            """ %(str(self.test_start_time), str(self.elapsed), str(self.suite_name), str(test), str(tags), str(criticalLink), str(statusColor), str(statusLink), str(test.message))
            self.content += test_detail_message
            _update_content(self, self.html_text, self.RF_LIVE_LOGGING_RUNNING_TITLE)

    def close(self):
        _update_content(self, self.html_text, self.RF_LIVE_LOGGING_FINAL_TITLE)

def _get_current_date_time(format,trim):
    t = datetime.datetime.now()
    if t.microsecond % 1000 >= 500:  # check if there will be rounding up
        t = t + datetime.timedelta(milliseconds=1)  # manually round up
    if trim:
        return t.strftime(format)[:-3]
    else:
        return t.strftime(format)

def _update_content(self, content, title):
    self.liveLogsFile = open(self.liveLogFilepath,'w')
    updated_content = content.replace("__title__", title)
    updated_content = updated_content.replace("__refreshInfo__", "Refresh timer is set to '" + str(self.refresh) + "' seconds")
    updated_content = updated_content.replace("__buttonStopRefresh__", self.buttonStopRefresh)
    if title == self.RF_LIVE_LOGGING_FINAL_TITLE:
        updated_content = content.replace("__title__", title)
        updated_content = updated_content.replace("__refreshInfo__", "")
        updated_content = updated_content.replace("__buttonStopRefresh__", "")
        updated_content = updated_content.replace(self.refreshTimer, self.refreshStopped)
        updated_content = _add_result_links(self, updated_content, self.logFile, self.reportFile)
    updated_content = updated_content.replace("__expected__",str(self.expected))
    updated_content = updated_content.replace("__executed__",str(self.executed))
    updated_content = updated_content.replace("__passed__",str(self.passed))
    updated_content = updated_content.replace("__skipped__",str(self.skipped))
    updated_content = updated_content.replace("__blocked__",str(self.blocked))
    updated_content = updated_content.replace("__failed__",str(self.failed))
    updated_content = updated_content.replace("__content__",str(self.content))
    self.liveLogsFile.write(updated_content)
    self.liveLogsFile.close()

def _add_result_links(self, content, logFile, reportFile):
    #change if new pages should be opened
    #add_link_ReportFile = """<a href=""" + reportFile.replace(' ', '%20') + """ target='_blank'>Report</a>"""
    #add_link_LogFile = """<a href=""" + logFile.replace(' ', '%20') + """ target='_blank'>Log</a>"""
    add_link_ReportFile = "<a href='" + self.reportFile + "'>Report</a>"
    add_link_LogFile = "<a href='" + self.logFile + "'>Log</a>"
    print ("LiveResults - Link to Log file: " + add_link_LogFile)
    print ("LiveResults - Link to Report file: " + add_link_ReportFile)
    updated_content = content.replace("__logFile__", add_link_LogFile)
    updated_content = updated_content.replace("__reportFile__", add_link_ReportFile)
    return updated_content;
 
def _open_liveLogs(self, filepath):
    webbrowser.open_new_tab(filepath)
