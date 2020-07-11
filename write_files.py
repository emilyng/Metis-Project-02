import Scrape

files = ['2013-12-30_factbook.json', '2014-12-29_factbook.json',
         '2015-12-28_factbook.json', '2016-12-26_factbook.json',
         '2017-12-25_factbook.json', '2018-12-31_factbook.json',
         '2019-12-30_factbook.json', '2020-05-04_factbook.json']

if __name__ == '__main__':
    for file in files:
        Scrape.write('./factbook 2013-2020/' + file)
