# -*- coding: utf-8 -*-

import os
import re
import time
import email
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from email.mime.multipart import MIMEMultipart

class SendEmail(object):
    def __init__(self):
        self.log_path = self.get_log_path('log.html')
        self.report_path = self.get_log_path('report.html')
        self.head = '''
        <!doctype html>
        <html>
        <head>
        <style type="text/css">
		

        div:hover {
			background-color: #555;
			color: white;
		}
        h3:hover {
			background-color: #555;
			color: white;
		}
        }
           
        .report_style{margin:20px 10%}        
        .header{text-align:center;width:100%;font-family:"Times New Roman"}    
        .report_table {text-align:center; width:100%; font-family:"Times New Roman"}        
        .report_table_title  {height:40px; text-align:center; width:100%; font-weight: bold; font-size:24px} 
       
        .report_table_content {background-color:#99CCFF; width:27%; text-align:center; padding:0 10px;} 
        .report_table_total {background-color:#CCFFFF; width:18%; text-align:center; padding:0 10px;}
        .table_content_success {background-color: #6bff8f; width:16%; text-align:center; padding:0 10px;}        
        .table_content_fail {background-color: #ff6c6d; width:15%; text-align:center; padding:0 10px;}
        .table_elapsed_time {background-color:#99CCFF; width:24%; text-align:center; padding:0 10px;}
        .table_head {background-color: #66CCFF; text-align:center; font-weight:bold; padding:0 10px;} 
        .table_path {background-color:#FFCC99; width:0%; text-align:center; padding:0 10px;}
        #summary_info {border: 1px solid #ccc;background-color:#FFEBCD;
                    border-spacing: 0.2em;
                    clear: both;
                    width: 100%;
                    margin-bottom: 1em;}
         </style>
        </head> 
        <body>
                <div class="header">
                    <h1>TD-Shim Automation Test Report</h1>
                </div>
        '''

        self.table_head = '''<div class="report_style">
        
        <table class="report_table">
            <tr>
                <th colspan="6" class="report_table_title">table_title_name</th>
            </tr>
        <br>
            <tr>
                <td class="table_head">name</td>
                <td class="table_head">Total</td>
                <td class="table_head">Pass</td>
                <td class="table_head">Fail</td>
                <td class="table_head">Elapsed Time</td>
            </tr>
        '''
        self.table_content = '''<tr>
            <td class="report_table_content">replace0</td>
            <td class="report_table_total">replace1</td>
            <td class="table_content_success">replace2</td>
            <td class="table_content_fail">replace3</td>
            <td class="table_elapsed_time">replace4</td>
            </tr>'''
        self.summary_info = '''
        <div>
            <p style='margin-top:26.25pt;margin-right:0in;margin-bottom:15.0pt;margin-left:0in'>
		<b><span style='font-size:16.5pt;color:black'>Summary Infomation:</span></b>
		</p>
			<ol><li style='mso-list:l1 level1 lfo3'><b><span
		 style='font-size:11.0pt;font-family:"Calibri",sans-serif;mso-fareast-font-family:
		 "Times New Roman"'>This is weekly automation test report for TD-Shim.</span></b>
			</li>
            <li style='mso-list:l1 level1 lfo3'><b><span
		 style='font-size:11.0pt;font-family:"Calibri",sans-serif;mso-fareast-font-family:
		 "Times New Roman"'>Test contatin functionality and fuzzing test.</span></b>
			</li>
            <li style='mso-list:l1 level1 lfo3'><b><span
		 style='font-size:11.0pt;font-family:"Calibri",sans-serif;mso-fareast-font-family:
		 "Times New Roman"'>Each fuzzing test case run about 1 hour.</span></b>
			</li>
			<li  style='mso-list:l1 level1 lfo3'><b><span
		 style='font-size:11.0pt;font-family:"Calibri",sans-serif;mso-fareast-font-family:
		 "Times New Roman"'>TD-Shim version: replace0.</span></b>
			</li>
			<li style='mso-list:l1 level1 lfo3'><b>
            <span style='font-size:11.0pt;font-family:"Calibri",sans-serif;mso-fareast-font-family:
		 "Times New Roman"'>Completion Rate: <span style='background:yellow;
		 mso-highlight:yellow'>100%</span></span></b>
			</li>
            </ol>
        </div>
        '''
        self.tail_info = '''
            <h5>Please see the attachment of the email for more details</h5>
        '''

    def set_value_to_html(self):
        self.set_value_to_summary()
        content_dict = self.get_value_from_html()  # list
        table_tile = ['Total Statistics', 'Statistics by Tag', 'Statistics by Suite']
        table_head_html = ''
        for a in range(len(content_dict)):
            table_dict = content_dict[a]
            table_head_html = table_head_html + '\r\n' + self.table_head.replace('table_title_name', table_tile[a])
            table_content_html = ''
            for b in range(len(table_dict)):
                table_content_html = table_content_html + '\r\n' + self.table_content
                name = table_dict[b]['label']
                total_num = table_dict[b]['pass'] + table_dict[b]['fail']
                pass_num = table_dict[b]['pass']
                fail_num = table_dict[b]['fail']
                elapsed_time = table_dict[b]['elapsed']
                table_list = [name, str(total_num), str(pass_num), str(fail_num), elapsed_time]

                for c in range(5):
                    table_content_html = table_content_html.replace('replace' + str(c), table_list[c])
            table_head_html = table_head_html + '\r\n' + table_content_html + '</table></div>'

        all_html = self.head + '<br></br>' + self.summary_info + table_head_html + '<br></br>'  + \
            self.tail_info + '</body></html>'
        return all_html
    
    def set_value_to_summary(self):
        try:
            soup = BeautifulSoup(open(self.log_path, 'rb+'), "html.parser")
            pattern = re.compile(r'version_hash} = (\w+)')

            get_config_hash = re.search(pattern, soup.decode()).group(1)
            
            tmp_list = [] 
            for v in get_config_hash,:
                tmp_list.append(v)
            if len(tmp_list) == 0:
                return 0
            
            for l in range(len(tmp_list)):
                self.summary_info = self.summary_info.replace('replace' + str(l), tmp_list[l])
            
            return  self.summary_info
        except Exception as e:
            print(e)
        
    def receive_ret_value(self,*value):
        pass
        
        
    def get_log_path(self, file_name):
        current_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_path, file_name)
        return config_path

    def get_value_from_html(self):
        soup = BeautifulSoup(open(self.log_path, 'rb+'), "html.parser")
        content = re.findall(r'stats\"] = (.+);', soup.decode())
        content_dict = eval(content[0])
        return content_dict

    def send_mail(self):
        log_path = self.log_path
        report_path = self.report_path

        smtp_server = "smtp.intel.com"
        sender = "wei3.liu@intel.com" 
        
        receivers = ['wei3.liu@intel.com',]  
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        detail_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        send_header = "TD-Shim Automation Test Report " + today + " " + detail_time 
        msg = MIMEMultipart()
        msg['Subject'] = send_header
        msg['From'] = sender
        msg['To'] = ",".join(receivers)

        content = self.set_value_to_html()
        msg.attach(MIMEText(content, _subtype='html', _charset='utf-8'))

        log_file = MIMEApplication(open(log_path, 'rb').read())
        log_file.add_header('Content-Disposition', 'attachment', filename='log.html')
        msg.attach(log_file)

        report_file = MIMEApplication(open(report_path, 'rb').read())
        report_file.add_header('Content-Disposition', 'attachment', filename='report.html')
        msg.attach(report_file)

        try:
            server = smtplib.SMTP(smtp_server)
            server.sendmail(sender, receivers, msg.as_string())
            server.close()
            print('Sendmail successfully')
        except Exception as e:
            print('Sendmail fail', str(e))
