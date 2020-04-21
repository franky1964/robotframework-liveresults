import os
import datetime
import webbrowser
import pathlib
from robot.libraries.BuiltIn import BuiltIn

__version__ = '0.5.0'

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
If you already have Python >= 3.6 with pip installed, you can simply
run:
``pip install --upgrade robotframework-liveresults``
"""
	
    ROBOT_LISTENER_API_VERSION = 3
 
    def __init__(self, show=True, capture=False, refresh=15, filename='RF_Live_Results.html'):
        self.ROBOT_PARENT_SUITE_SETUP_FAILED = 'Parent suite setup failed'
        self.RF_LIVE_LOGGING_INITIAL_TITLE = 'Robot Framework Live Results (Initialize...)'
        self.RF_LIVE_LOGGING_RUNNING_TITLE = 'Robot Framework Live Results (Running...)'
        self.RF_LIVE_LOGGING_FINAL_TITLE = 'Robot Framework Live Results (Execution completed)'
        self.RF_LIVE_LOGGING_ICON_PATH = 'https://avatars2.githubusercontent.com/u/574284?s=200&v=4'
        self.PRE_RUNNER = 0
        #self.liveLogFilepath filename = '\\\\SIDERIT\\LiveResults\\RF_Live_Results.html'
        self.liveLogFilepath = filename
        self.openBrowser = show
        self.makeVideo = capture
        self.reportFile = None
        self.logFile = None
        self.expected = 0
        self.executed = 0
        self.skipped = 0
        self.passed = 0
        self.failed = 0
        self.refreshTimer = "http-equiv='refresh' content='" + str(refresh) +"'"
        self.refreshStopped = "http-equiv='refresh' content='5000'"
        self.content = ""
        self.videoFilename = ""
        self.statusColors = {'yellow':'#FFFF66', 'green':'#32CD32', 'red':'#CD5C5C'}
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
	</html>
	<body>
		<table align="center" style="table-layout: fixed ;">
			<td style="text-align: left;">
				<button class="btn" value="Refresh Page" onClick="window.location.href=window.location.href">Reload Page</button>
			</td>
			<td>
				<a><img src="__iconLink__" style="height:10vh;max-width:98%;"></a> 
			</td>
			<td>
				<h3 style="color:#009688;" style="text-align: center;">
					<b>__title__</b>
				</h3>
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
					<td bgcolor='""" + self.statusColors['yellow'] + """'><b>__skipped__</b></td>
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
        self.html_text = self.html_text.replace ("__iconLink__", self.RF_LIVE_LOGGING_ICON_PATH)
        _update_content(self, self.html_text, self.RF_LIVE_LOGGING_INITIAL_TITLE)

    def start_suite(self, suite, result):
        # count expected total testcases and open bowser only on top level
        if self.PRE_RUNNER == 0:
            self.PRE_RUNNER = 1
            self.logFile = BuiltIn().get_variable_value("${LOG FILE}")
            self.reportFile = BuiltIn().get_variable_value("${REPORT FILE}")
            self.liveLogFilepath = os.path.join(pathlib.Path(self.reportFile).parent.absolute(), self.liveLogFilepath)
            self.logFile = self.logFile.replace(' ', '%20')
            self.reportFile = self.reportFile.replace(' ', '%20')
            self.expected = suite.test_count
            _update_content(self, self.html_text, self.RF_LIVE_LOGGING_RUNNING_TITLE)
            if self.openBrowser: _open_liveLogs(self, self.liveLogFilepath)
            if self.makeVideo:
              try:
                BuiltIn().import_library('ScreenCapLibrary')
                self.screencaplib = BuiltIn().get_library_instance('ScreenCapLibrary')
              except:
                self.makeVideo = False
                BuiltIn().log('LiveResults: To get videos for test case executions please install the following library: <a href="https://github.com/mihaiparvu/ScreenCapLibrary">ScreenCapLibrary</a>','ERROR','HTML')
        self.test_count = len(suite.tests)
        if self.test_count != 0:
            self.suite_name = suite.name

    def start_test(self, data, test):
        self.test_start_time = _get_current_date_time('%Y-%m-%d %H:%M:%S.%f',True)
        if (self.makeVideo):
            #self.test_case_name = ''.join([x.replace(' ', '_') for x in str(test)])
            self.test_case_name = str(test)
            self.screencaplib.start_video_recording(name=str(self.test_case_name))
            self.videoFilename = os.path.join(pathlib.Path(self.reportFile).parent.absolute(), self.test_case_name + "_1.webm")
            self.videoFilename = self.videoFilename.replace(' ', '%20')

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
                self.skipped = self.skipped + 1
                statusColor = self.statusColors['yellow']
                status = 'SKIP'
            statusLink = "<a href='file:///" + self.logFile + "#" + test.id + "' target='_blank'>" + status + "</a>"
            criticalLink = str(test.critical)
            if self.makeVideo: criticalLink = "<a href='file:///" + self.videoFilename + "' target='_blank'>" + criticalLink + "</a>"
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
            if self.makeVideo:
               self.screencaplib.stop_video_recording()

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
          if title == self.RF_LIVE_LOGGING_FINAL_TITLE:
            updated_content = updated_content.replace(self.refreshTimer, self.refreshStopped)
            updated_content = _add_result_links(self, updated_content, "file:///" + self.logFile, "file:///" + self.reportFile)
          updated_content = updated_content.replace("__expected__",str(self.expected))
          updated_content = updated_content.replace("__executed__",str(self.executed))
          updated_content = updated_content.replace("__passed__",str(self.passed))
          updated_content = updated_content.replace("__skipped__",str(self.skipped))
          updated_content = updated_content.replace("__failed__",str(self.failed))
          updated_content = updated_content.replace("__content__",str(self.content))
          self.liveLogsFile.write(updated_content)
          self.liveLogsFile.close()

def _add_result_links(self, content, logFile, reportFile):
        #switch if new pages should be opened
        #add_link_ReportFile = """<a href=""" + reportFile.replace(' ', '%20') + """ target='_blank'>Report</a>"""
        #add_link_LogFile = """<a href=""" + logFile.replace(' ', '%20') + """ target='_blank'>Log</a>"""
        add_link_ReportFile = "<a href='" + reportFile.replace(' ', '%20') + "'>Report</a>"
        add_link_LogFile = "<a href='" + logFile.replace(' ', '%20') + "'>Log</a>"
        updated_content = content.replace("__logFile__", add_link_LogFile)
        updated_content = updated_content.replace("__reportFile__", add_link_ReportFile)
        return updated_content;
 
def _open_liveLogs(self, filepath):
        webbrowser.open_new_tab(filepath)
