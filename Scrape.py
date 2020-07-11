import re
import csv
import sys
import requests
import time, os
import itertools

from collections import defaultdict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ColumnNames import columns

'''
#credit: Roman Konoval StackOverflow
#https://stackoverflow.com/questions/43382447/python-with-selenium-drag-and-drop-from-file-system-to-webdriver

Uses JS_DROP_FILE script to enable selenium to drag and drop a file from
local machine as input for website.
'''

JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""

def drag_and_drop_file(drop_target, path):
    driver = drop_target.parent
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input.send_keys(path)


def xpath_soup(element):
    """
    #credit to: Rob Hawkins from stackoverflow
    #https://stackoverflow.com/questions/37979644/parse-beautifulsoup-element-into-selenium

    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def check_boxes(soup):
    '''
    Check all the boxes for features of interest (specified in 'columns').
    This method may result in some leak-over of features not explicitly specified in 'columns'
    list. This is due to the cases where the column is not one of the checkbox options

    check_boxes() will print out all features in 'columns' list that does not appear as a
    check box option
    '''
    global columns
    for i in range(len(columns)):
        try:
            soup_element = soup.find(text=columns[i]).find_previous('input')
            xpath = xpath_soup(soup_element)
            driver.find_element_by_xpath(xpath).click()
        except:
            print('"{}" not found'.format(columns[i]))
            pass

def scrape(file_path):
    '''
    Uses Selenium web driver to automate interaction with website.
    - Upload factbook.json file
    - Click checkboxes according to 'columns' elements
    - Retrieves organized data

    Input: file path/file name
    Output: header - header row (list)
            data - list of dictionaries mapping header elements to data element
    '''
    chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
    os.environ["webdriver.chrome.driver"] = chromedriver

    url = 'https://iancoleman.io/explorer-cia-world-factbook/'

    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    chooseFile = driver.find_element_by_xpath('//div/p[@class="dz-clickable"]')

    path = os.path.abspath(file_path)
    drag_and_drop_file(chooseFile, path)
    time.sleep(1)

    change_columns_button = driver.find_element_by_xpath('//p/button[@type="button"]').click()
    soup = BeautifulSoup(driver.page_source, 'lxml')
    time.sleep(1)

    #check_boxes(soup)
    ###for some reason, check_boxes() function is inoperable within scrape()
    ###BUT it works well when on its own... ???

    for i in range(len(columns)):
        try:
            soup_element = soup.find(text=columns[i]).find_previous('input')
            xpath = xpath_soup(soup_element)
            check_box = driver.find_element_by_xpath(xpath).click()
        except:
            print('"{}" not found'.format(columns[i]))
            pass

    x_button = driver.find_element_by_xpath('//div/button[@aria-label="Close"]').click()
    soup = BeautifulSoup(driver.page_source, 'lxml')

    driver.close()

    return get_header(soup), get_data(soup)

def get_header(soup):
    '''
    Retrieves header from soup

    Input: BeautfifulSoup.soup element
    Output: list of header (str) elements
    '''
    #regex credit: Brian Balzar from stackoverflow
    #https://stackoverflow.com/questions/53014806/using-regex-to-extract-from-second-period-to-end-of-a-string

    table_headers = soup.find_all('th')
    header = []
    for item in table_headers:
        string = item.text
        try:
            subject = re.match('^([^.]+)\.([^.]+)\.(.+)$', string).group(3)
            subject = subject.replace('.', '_')
        except:
            subject = string
        header.append(subject)
    return header

def get_header(soup):
    '''
    Retrieves header from soup

    Input: BeautfifulSoup.soup element
    Output: list of header (str) elements
    '''
    #regex credit: Brian Balzar from stackoverflow
    #https://stackoverflow.com/questions/53014806/using-regex-to-extract-from-second-period-to-end-of-a-string

    table_headers = soup.find_all('th')
    header = []
    for item in table_headers:
        string = item.text
        try:
            subject = re.match('^([^.]+)\.([^.]+)\.(.+)$', string).group(3)
            subject = subject.replace('.', '_')
        except:
            subject = string
        header.append(subject)
    return header

def get_data(soup):
    '''
    Retrieves table element
    Parses through rows and collects data

    Input: BeautifulSoup.soup element
    Output: list of dictionaries containing data
    '''
    data = []

    header = get_header(soup)
    table = soup.find('table')
    rows = [row for row in table.find_all('tr')][1:]

    for row in rows:
        row_data = defaultdict()
        for i in range(len(header)):
            row_data[header[i]] = row.find_all('td')[i].text
        data.append(row_data)

    return data

def write(file_name):
    '''
    Writes out scraped data as a csv file

    Input: file_ path/file name of factbook.json file
    Output: CSV
    '''
    keys, data = scrape(file_name)
    date = re.search('\/(([\d]*-)+[\d]*)', file_name).group(1)
    with open('{}_data.csv'.format(date), 'w', newline='') as write_obj:
        # create writer object
        dict_writer = csv.DictWriter(write_obj, fieldnames = keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


if __name__ == '__main__':
    file_name = sys.argv[1]
    write(file_name)
