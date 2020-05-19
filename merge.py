#!/usr/bin/env python3

import collections
import concurrent.futures as futures
import os


SITEFILTER_TMP_DIR = '/tmp/sitefilter'
UNIQUE_SITES_FILE_PATH = f'{SITEFILTER_TMP_DIR}/unique-sites'
EXCLUDED_SITES_FILE_PATH = f'{SITEFILTER_TMP_DIR}/excluded-sites'
SITE_CANDIDATES_FILE_PATH = f'{SITEFILTER_TMP_DIR}/google-results'
MERGE_FILE = f'/home/{os.environ["USER"]}/Projects/sitefilter/rest2'
FILES = [
    'books',
    'cnc',
    'dictionaries',
    'economy',
    'exceptionsitelist',
    'informatics',
    'informatics2',
    'math',
    'radio',
    'recipes',
    'rest',
    'rest2',
    'spiritual',
    'to-sort-0',
    'to-sort-1',
]
EXCLUDED_PHRASES = [
    'ali',
    'allegro',
    'amazon',
    'arvix.org',
    'audio',
    'bcc',
    'blogspot',
    'book',
    'buy',
    'chomikuj',
    'czyta',
    'dailymotion',
    'demotywatory',
    'dis',
    'ebay',
    'edu',
    'etsy',
    'facebook',
    'fakt',
    'fandom',
    'film',
    'flickr',
    'gallery',
    'github',
    'giphy',
    'google',
    'gov',
    'health',
    'image',
    'instagram',
    'interia',
    'issuu',
    'ksiazki',
    'media',
    'msn.com',
    'newsweek',
    'nk',
    'onet',
    'photo',
    'pic',
    'pinterest',
    'readthedocs',
    'reddit',
    'shutter',
    'slide',
    'smog',
    'stack',
    'steemit',
    'travel',
    'trip',
    'tube',
    'tumblr',
    'tv',
    'twitter',
    'vimeo',
    'yandex',
    'youtube',
    'wiki',
    'wordpress',
    'wp',
    'wyborcza',
]


def main():
    if not os.path.isdir(SITEFILTER_TMP_DIR):
        os.makedirs(SITEFILTER_TMP_DIR)

    if (
        not os.path.isfile(UNIQUE_SITES_FILE_PATH) or
        not os.path.isfile(EXCLUDED_SITES_FILE_PATH)
    ):
        create_cache_files()

    sites, excluded = get_from_cache()
    candidates = read_set(SITE_CANDIDATES_FILE_PATH)
    no_duplicates = candidates - sites - excluded

    with open(SITE_CANDIDATES_FILE_PATH, 'w'):  # clear this file
        pass

    with open(MERGE_FILE, 'a') as f, open(UNIQUE_SITES_FILE_PATH, 'a') as g:
        for site in no_duplicates:
            for exc in EXCLUDED_PHRASES:
                if exc in site:
                    print(f'({exc}) in', site)
                    break
            else:
                txt = f'{site}\n'
                f.write(txt)
                g.write(txt)

def create_cache_files():
    sites, excluded = set(), set()

    with futures.ThreadPoolExecutor() as executor:
        files_future = set(executor.submit(read_file, _file) for _file in FILES)

        for future in futures.as_completed(files_future):
            _sites, _excluded = future.result()
            sites.update(_sites)
            excluded.update(_excluded)

    with open(UNIQUE_SITES_FILE_PATH, 'w') as f:
        for site in sites:
            f.write(f'{site}\n')

    with open(EXCLUDED_SITES_FILE_PATH, 'w') as f:
        for exc in excluded:
            f.write(f'{exc}\n')

def read_file(_file):
    sites, excluded = set(), set()

    with open(_file, 'r') as file_:
        for line in file_:
            line = line.strip()
            if line:
                if line.startswith('#'):
                    line = line.strip('#').split()
                    if line:
                        excluded.add(line[0])
                else:
                    line = line.split()
                    sites.add(line[0])

    return sites, excluded

def get_from_cache():
    sites = read_set(UNIQUE_SITES_FILE_PATH)
    excluded = read_set(EXCLUDED_SITES_FILE_PATH)
    return sites, excluded

def read_set(fname):
    with open(fname, 'r') as f:
        data = f.readlines()

    http_prefix, https_prefix = 'http://', 'https://'
    http_pref_len, https_pref_len = len('http://'), len('https://')

    s = set()
    for d in data:
        d = d.strip()
        d = d.lower()
        if d.startswith('http'):
            d = d[d.startswith(http_prefix) and http_pref_len :]
            d = d[d.startswith(https_prefix) and https_pref_len :]
        s.add(d)
    return s

if __name__ == '__main__':
    main()
