# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""
import json
import resilient
import requests
from bs4 import BeautifulSoup
import sys
from contextlib import redirect_stdout
from datetime import datetime
import logging
from resilient_circuits import ResilientComponent, function, handler, StatusMessage, FunctionResult, FunctionError


class FunctionComponent(ResilientComponent):
    """Component that implements Resilient function 'utilities_smg_domain"""

    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(FunctionComponent, self).__init__(opts)
        self.options = opts.get("smg_utilities", {})

    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.options = opts.get("smg_utilities", {})

    @function("utilities_smg_domain")
    def _utilities_smg_domain_function(self, event, *args, **kwargs):
        """Function: """
        try:
            # Get the function parameters:
            smg_block_domain = kwargs.get("smg_block_domain")  # text
            
            log = logging.getLogger(__name__)
            log.info("smg_block_domain: %s", smg_block_domain)
			
	        # Date is datetime to be used with print options		
            Date = datetime.today()
            # App.Config Valuse of SMG_Utilities Section							
            smg__url=self.options["smg_url"]
	    smg__username=self.options["smg_username"]
            smg__password=self.options["smg_password"]
            smg__log=self.options["smg_log"]
			
            # URL's which will be Used in Requests
            AUTH_URL =smg__url +'/brightmail/login.do'
            AUTH_URL2 =smg__url +'/brightmail/reputation/sender-group/viewSenderGroup.do'
            AUTH_URL3 =smg__url +'/brightmail/reputation/sender-group/saveSender.do'
			
            auth = {
	'lastlogin':'16b873a0772',
	'userLocale':'',
	'lang':'en_US',
	'username': smg__username,
	'password': smg__password,
	'loginBtn':'Login'
                    }


            auth2 = {
	'selectedSenderGroups':'1|3',
	'view':'badSenders',
	'symantec.brightmail.key.TOKEN':''

                  }

            auth3 = {
    'pageReuseFor':'add',
    'currentSender':'',
	'selectedSenderGroups':'1|3',
	'view':'badSenders',
	'symantec.brightmail.key.TOKEN':'',
    'addEditSenders': smg_block_domain
                    }


            # First Request getting LastLogin Value					
            session = requests.Session()
            response_one = session.post(AUTH_URL, data=auth, verify=False)
            soup = BeautifulSoup(response_one.text, 'html.parser')
            last_login = soup.find('input', attrs={'name':'lastlogin'})
            

            if last_login is None:
               response_one = session.post(AUTH_URL, data=auth, verify=False)
               soup = BeautifulSoup(response_one.text, 'html.parser')
               last_login = soup.find('input', attrs={'name':'lastlogin'})
               s = last_login.attrs
               s['value'] 
			   
	    s = last_login.attrs
            s['value'] 
            # The New data with the Last_Login Value
            auth1 = {
        'lastlogin': s['value'],
        'userLocale':'',
        'lang':'en_US',
        'username': smg__username,
        'password': smg__password,
        'loginBtn':'Login'
                    }

            # Second Request with LastLogin Value	
            response_two = session.post(AUTH_URL, data=auth1, verify=False)
	        # Third Request getting Symantec_Token Value	
            response_three = session.post(AUTH_URL2, data=auth2)
            soup = BeautifulSoup(response_three.text, 'html.parser')
            if soup.find('div', attrs={'id':'bannerConfirm'}) is not None:
               print("Login Failure")
               with open(smg__log, 'a') as f, redirect_stdout(f):
                   print("Login Failure", Date)
               f.close()

            soup = BeautifulSoup(response_three.text, 'html.parser')
            result_two = soup.find('input', attrs={'name':'symantec.brightmail.key.TOKEN'})
            print("------------------------------------------")
            z = result_two.attrs
            z['value']

            auth4 = {
    'pageReuseFor':'add',
    'currentSender':'',
	'selectedSenderGroups':'1|3',
	'view':'badSenders',
	'symantec.brightmail.key.TOKEN': z['value'],
    'addEditSenders': smg_block_domain
                  }
            # Forth Request getting Setting IP to SMG
            response_four = session.post(AUTH_URL3, data=auth4)
	    # Check Success or Faild to Send IP in HTML
            soup = BeautifulSoup(response_four.text, 'html.parser')
            Success = soup.find('div', attrs={'class':'successMessageText'})

            soup = BeautifulSoup(response_four.text, 'html.parser')
            fail = soup.find('div', attrs={'class':'errorMessageText'})

            if Success is not None:
              print(smg_block_domain, "Added Successfully to SMG")
            else:
                 print("Faild to add", smg_block_domain, "Due to", fail)

            with open(smg__log, 'a') as f, redirect_stdout(f):
                print("This is logs of adding", smg_block_domain, Date)
                print(response_one.status_code, Date)
                print("-----------------------------")
                print(response_two.status_code, Date)
                print("-----------------------------")
                print(response_three.status_code, Date)
                print("-----------------------------")
                print("This is the HTML Response to add", smg_block_domain)
                print(response_four.status_code, Success, fail, Date)
            f.close()
            results = {"HTML": response_four.text,
			           "OK": response_four.ok
                      }
            # Produce a FunctionResult with the results
	    yield FunctionResult(results)
        except Exception:
            yield FunctionError()
