from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import argparse
import sys
import json

def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')


def main(args):
    
    parser = argparse.ArgumentParser(description='Quickly create multi-class image dataset by scraping images from Google Images.')
    parser.add_argument('-s', '--search', default='', type=str,
                        help='comma separated list of image classes to download (ie. "apple,banana,orange")')
    parser.add_argument('-n', '--num_images', default=0,
                        type=int, help='number of images to download (per class)')
    parser.add_argument('-d', '--directory', default='.',
                        type=str, help='save directory')

    args = parser.parse_args()
    query = args.search
    max_images = args.num_images
    save_directory = args.directory

    if not query or not max_images:
        parser.print_help()
        return
    print "[Saving to: " + str(save_directory) + "]"    
    query = query.split(',')
    for q in query:
        url = "https://www.google.co.in/search?q=" + urllib2.quote(q) + "&source=lnms&tbm=isch"
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = get_soup(url, header)
        ActualImages = []  # contains the link for Large original images, type of  image
        for a in soup.find_all("div", {"class": "rg_meta"}):
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            ActualImages.append((link, Type))
        for i, (img, Type) in enumerate(ActualImages[0:max_images]):
            try:
                req = urllib2.Request(img, headers={'User-Agent': header})
                raw_img = urllib2.urlopen(req).read()
		class_dir = os.path.join(save_directory, str(q))
		if not os.path.exists(class_dir):
			os.makedirs(class_dir)
		if len(Type) == 0:
                    f = open(os.path.join(class_dir,
                                          str(q) + "_" + str(i) + ".jpg"), 'wb')
                else:
                    f = open(os.path.join(class_dir, str(q) +
                                          "_" + str(i) + "." + Type), 'wb')
                f.write(raw_img)
                f.close()
            except Exception as e:
                print "could not load : " + img
                print e


if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
