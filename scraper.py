# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".


import scraperwiki
import lxml.html
import hashlib
import re
from splinter import Browser
import sys, traceback, logging, shutil, platform
from string import ascii_lowercase



def scrape_page(browser):

  cfg = ['a','b','c','d','e','f']


  if not browser.is_element_present_by_xpath('//table[@class="tblSearchResults"]', wait_time=100):
      raise Exception('Failed to find Results Page')

  raw_data_table = browser.find_by_xpath( '//table[@class="tblSearchResults"]' ).first
  print raw_data_table
  trs = raw_data_table.find_by_tag("tr")
  row_counter = 0
  for row in trs:

    row_properties = {}

    if ( row_counter == 0 ):
      print "Skip header"
    else:
      print "processing row";
      tds = row.find_by_tag("td")
      ctr = 0;
      for cell in tds:
        if ( ctr==0 ):
          print "Extract id"
          print cell.text
          row_properties['grantId'] = cell.find_by_tag("a").first['href']
        row_properties[cfg[ctr]]=cell.text
        ctr = ctr +1
    row_counter = row_counter +1

    if row_properties is not None :
      # scraperwiki.sqlite.save(unique_keys=['grantId'], data=row_properties)
      print row_properties

  return;


def scrape_lottery() :
  try:
    print "platform %s" % platform.system()
    print "Python ", sys.version_info

    with Browser('phantomjs') as browser:
      # browser.visit('http://www.lottery.culture.gov.uk/SearchResults.aspx')
      browser.visit('http://www.lottery.culture.gov.uk/AdvancedSearch.aspx')
      submit_button = browser.find_by_xpath('//input[@type="submit"]').first
      submit_button.click()
      scrape_page(browser);

  except:
    print "Unexpected error:", sys.exc_info()
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)

  return

print 'About to Scrape http://www.lottery.culture.gov.uk/SearchResults.aspx'
scrape_lottery();
print 'Completed'


