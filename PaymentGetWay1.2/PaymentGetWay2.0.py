from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
import time
import re
import pandas as pd
import os
import yagmail
import pypyodbc as odbc

time.sleep(60);
user_firefox_profile = r'C:\Users\User\AppData\Roaming\Mozilla\Firefox\Profiles\m36o8ly3.default-release-1675278311411'
bkash_sms_url='https://messages.google.com/web/conversations/620'
google_sheet_id = '15hP7KX-svbiOJBX8tpLikG8Vk6ORuqbMjtWsIAtKSzw'
joining_column_name = 'Transection ID'
file_name = 'validated_data.csv'
sender = 'aust.decipher@gmail.com'

# password for your gmail account. please refer to the video instruction.
credential = 'sijhpnswfycrjsvx'

# your mail subject.
subject = 'eTICKET PAYMENT'

# text of your mail body.
mail_body = '''Dear Customer,
YOUR PAYMENT IS COMPLETED

Best regards
eTicket payment service
'''
#Data Base
DRIVER_NAME='SQL SERVER'
SERVER_NAME = 'DESKTOP-03NNHMH\SQLEXPRESS'
DATABASE_NAME='RAILWAY_DB'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
conn=odbc.connect(connection_string)
cursor = conn.cursor()

# load the provided default firefox user frofile to selenium, this will helps to bypass the loging process
profile = FirefoxProfile(user_firefox_profile)

driver = webdriver.Firefox(profile)

# browse to messages for web website. it should automatically login.
driver.get('https://messages.google.com/web')

driver.get(bkash_sms_url)
time.sleep(10)

# find the html tags by class name which contains text sms.
elements = driver.find_elements_by_class_name(r'text-msg-content')

# finally grab the text part and store the string in a list named messages.
messages = []
for element in elements:
    messages.append(element.text)

print(messages)


# this function will return the transection type as a string based on
# matching group of words contains in the input string/text sms.
def transection_type(input_string=''):
    transec_type_dict = {
        'cash_in': 'Cash In Tk',
        'cash_out': 'Cash Out Tk',
        'send_money': 'Send Money Tk',
        'receive_money': 'You have received Tk'
    }
    for key in transec_type_dict:
        if transec_type_dict[key] in input_string:
            return key
    else:
        return 'unknown'


# this function find regular expression pattern match in input string and return the findings as a dictionary.
def extract_info(input_string=''):
    pattern_dict = {
        'trxId': r'\b[A-Z\d]{10}\b',
        'phn_num': r'01[3-9]\d{8}',
        'tk_amount': r'[\d,]+\.\d+',
        'date_time': r'[\d/]+ \d+:\d+'
    }
    info_dict = {}
    for key in pattern_dict:
        info_dict[key] = re.findall(pattern_dict[key], input_string)[0]
    cursor.execute(
        'insert into tempData(trxId,phn_num,tk_amount,date_time) values(?,?,?,?);',
        (info_dict['trxId'], info_dict['phn_num'],info_dict['tk_amount'],info_dict[key])
        )
    conn.commit()    
    info_dict['transec_type'] = transection_type(input_string)
    info_dict['mail_status'] = None
    return info_dict


# look for each sms which contains a phone number and extract the information
# using extract_info() function and add them to a list named info_list.
info_list = []
for message in messages:
    if re.findall(r'01[3-9]\d{8}', message):
        info_list.append(extract_info(message))
    else:
        continue

# create a pandas dataframe using the list just created.
info_df = pd.DataFrame(info_list)
print(info_df)

# load data from google sheet as pandas dataframe.
google_sheet_location = f'https://docs.google.com/spreadsheets/d/{google_sheet_id}/export?format=csv'
client_df = pd.read_csv(google_sheet_location)
client_df
# join two dataframe using columns which contains same information, in this case we are joining on transection_Id.
joined_df = pd.merge(left=client_df,
                     right=info_df,
                     left_on=joining_column_name,
                     right_on='trxId',
                     how='left')

# save the joined dataframe as a csv file if it is not saved previously.
# if it is saved previously then look for new information. if found any, add them to the end of our existing csv file.
if os.path.exists(file_name):
    previous_df = pd.read_csv(file_name)
    new_info_df = joined_df[~joined_df[joining_column_name].
                            isin(previous_df[joining_column_name])]
    updated_df = pd.concat([previous_df, new_info_df])
    updated_df.to_csv(file_name, index=False)
else:
    joined_df.to_csv(file_name, index=False)

joined_df
print(joined_df)


# inititate yagmail providing critical login info.
yag = yagmail.SMTP(sender, credential)

# load the saved csv file.
mail_df = pd.read_csv(file_name)


# This function will get each row of given dataframe from pandas apply method and modify it.
# and return the modified row to to pandas apply method.
# Main logic for this function is, if we didn't send email to a perticular person previously
# and his given transection ID is matched with our received bkash transection sms, then this
# person is a verified person and we should sent him a confirmation email.
# if a persons given transection Id is not matched with our bkash transection sms then 
# we will skip this person and don't send any email to him.
def mail_n_update(row):
    if row['mail_status'] != 'sent':
        if pd.isna(row['trxId']):
            row['mail_status'] = 'skipped'
            row['transec_type'] = 'not_matched!'
        else:
            try:
                yag.send(to=row['Email Address'], subject=subject, contents=mail_body)
                row['mail_status'] = 'sent'
            except:
                row['mail_status'] = 'failed'
               
    
    return row


mail_df = mail_df.apply(mail_n_update, axis=1)

# sometimes pandas apply method alter the order of columns in dataframe, 
# this line will rearrange the columns in correct order.
mail_df = mail_df[joined_df.columns]

mail_df.to_csv(file_name, index=False)
mail_df
print(mail_df)
