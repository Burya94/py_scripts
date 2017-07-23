
#!/usr/bin/python3.5

from urllib import request
from bs4 import BeautifulSoup
import wget
import os
import re


URL = 'http://www.newstudio.tv/'

#"function that return location for downloads "
def downloads_location():
    os.chdir('/home/buria/Загрузки')
    return os.getcwd()

#"Function to download torrent and open it in BitTorrent client"
def download_torrent_720p(soup):
    a_hrefs = soup.find_all('a')
    download_link = a_hrefs[3].get('href')
    wget.download(URL+download_link, downloads_location())
    
    file_list = os.listdir(path='.')
    
    pattern =  'Marvel\'s\.Iron\.Fist.*'
    for i in file_list:
    	if re.match(pattern, i):
    		file_name = i
    		file_name = file_name[:6] + "\\" + file_name[6:]
    		print(file_name)
    		print("Job done! New episode available.")
    		os.system('transmission-gtk /home/buria/Загрузки/{}'.format(file_name))
    		


#"Get html code from url request"
def html_response(url):
    response = request.urlopen(url)
    return response.read()

#"Parsing, finding and matches to certain series"
def find_series(html):

    soup = BeautifulSoup(html, 'lxml')
    div_with_all_series = soup.find('div', id="sideLeft")
    div_with_all_series = div_with_all_series.find_all('div', class_="accordion-group")[1]
    div_list = div_with_all_series.find('div', class_="accordion-inner")
    series = div_list.find_all('div', class_='torrent')
    
    iron_fist = []
    for i in range(len(series)):
        if "Железный Кулак" in series[i].find('div', class_='ttitle').text :
            iron_fist.append(series[i])
                
        
    base = []
    with open('episodes.txt', 'r') as bd:
        for line in bd:
            base.append(line.strip())

    bd = open('episodes.txt', 'a')
    for r in range(len(iron_fist)):
        if iron_fist[r].find('div', class_='tdesc').text.strip() in base:
            continue
        else:
            download_torrent_720p(iron_fist[r])
            bd.write(iron_fist[r].find('div', class_='tdesc').text.strip() + '\n')
    bd.close()

def main():
    find_series(html_response(URL))



if __name__ == "__main__":
    main()