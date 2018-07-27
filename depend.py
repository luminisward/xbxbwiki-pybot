import sys
import dokuwiki
from lib.google_sheets import GoogleSheets
from lib.shop import Shop
import subprocess

if __name__ == '__main__':
    try:
        from config.mywiki import *
        from config.shop_sheet import *
    except ModuleNotFoundError:
        print('找不到config')
        sys.exit()

    try:
        wiki = dokuwiki.DokuWiki(siteurl, username, password, True)
    except dokuwiki.DokuWikiError:
        print('Username or password is wrong ,can\'t access wiki')
        sys.exit()

    # Set sheet instance
    shop_sheet = GoogleSheets()
    shop_sheet.sheet_id = SPREADSHEET_ID
    shop_sheet.range = RANGE_NAME
    # pull data
    shop_sheet.pull_data()
    shop_list = shop_sheet.dict_list

    # Set sheet instance
    qiyue_sheet = GoogleSheets()
    qiyue_sheet.sheet_id = SPREADSHEET_ID
    qiyue_sheet.range = '契约书'
    # pull data
    qiyue_sheet.pull_data()
    qiyue_list = qiyue_sheet.dict_list

    subprocess.call('rm 3.txt',shell=True)

    for shop_row in shop_list:
        for qiyue_row in qiyue_list:
            if shop_row['契约书（日）'] == qiyue_row['日文']:
                output = qiyue_row['简中']
                break
            else:
                output = ''
            
        print(output)
        subprocess.call('echo ' + output + ' >> 3.txt',shell=True)
