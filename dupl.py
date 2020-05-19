#!/usr/bin/env python3

import collections
import concurrent.futures as futures


FILES = [
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


def main():
    sites, excluded = {}, {}

    with futures.ThreadPoolExecutor() as executor:
        files_future = {
            executor.submit(read_file, _file) for _file in FILES
        }

        for future in futures.as_completed(files_future):
            _sites, _excluded = future.result()

            sites = {
                key : sites.get(key, 0) + _sites.get(key, 0)
                for key in set(sites) | set(_sites)
            }
            excluded = {
                key : excluded.get(key, 0) + _excluded.get(key, 0)
                for key in set(excluded) | set(_excluded)
            }

    print_stats(sites, excluded)


def read_file(_file):
    sites = collections.defaultdict(lambda: 0)
    excluded = collections.defaultdict(lambda: 0)

    with open(_file, 'r') as file_:
        for line in file_:
            line = line.strip()
            if line:
                if line.startswith('#'):
                    line = line.strip('#').split()
                    if line:
                        excluded[line[0]] += 1
                else:
                    line = line.split()
                    sites[line[0]] += 1

    return sites, excluded


def print_stats(sites, excluded):
    duplicates = [(site, cnt) for site, cnt in sites.items() if cnt > 1]
    are_in_excluded = [site for site in sites if site in excluded]

    print('liczba stron:', len(sites))
    print('liczba excluded:', len(excluded))
    print('liczba duplicates:', len(duplicates))

    if duplicates:
        print('Duplicates:')
        for dup, cnt in duplicates:
            print(str(cnt)+':', dup)

    if are_in_excluded:
        print('Excluded:')
        for exc in are_in_excluded:
            print(exc)


if __name__ == '__main__':
    main()
