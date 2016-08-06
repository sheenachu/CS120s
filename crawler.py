# CS122: Course Search Engine Part 1
# ESTELLE OSTRO & SHEENA CHU 

import re
import util
import bs4
import queue
import json
import sys
import csv

INDEX_IGNORE = set(['a',  'also',  'an',  'and',  'are', 'as',  'at',  'be',
                    'but',  'by',  'course',  'for',  'from',  'how', 'i',
                    'ii',  'iii',  'in',  'include',  'is',  'not',  'of',
                    'on',  'or',  's',  'sequence',  'so',  'social',  'students',
                    'such',  'that',  'the',  'their',  'this',  'through',  'to',
                    'topics',  'units', 'we', 'were', 'which', 'will', 'with', 'yet'])

def index_page(soup, index, course_map):
    '''
    Adds an html page to an index using a course map.

    Inputs: 
        soup: 
        index: set
        course_map: dictionary
    '''
    courses = soup.find_all('div', class_='courseblock main')
    for course in courses:
        sequence = util.find_sequence(course)
        if len(sequence) != 0:
            for s in sequence:
                course_id = find_course_id(s, course_map)
                index_course(course_id, s, index)
                index_course(course_id, course, index)
        else:
            course_id = find_course_id(course, course_map)
            index_course(course_id, course, index)

def find_course_id(course, course_map):
    '''
    Returns course identifier for a given course using the provided course map.

    Inputs:
        course: bs4 tag object
        course_map: dictionary
    Returns:
        integer
    '''
    t = course.find_all('p', class_='courseblocktitle')
    title = t[0].text
    title = title.replace(u'\xa0', ' ')
    code = re.search('[A-Z]{4} \d{5}', title).group()
    course_id = course_map[code]
    return course_id

def index_course(course_id, course, index):
    '''
    Adds a course to the index.

    Inputs:
        course_id: float
        course: bs4 tag object
        index: set
    '''
    paras = course.find_all('p', class_=['courseblockdesc', 
                            'courseblocktitle'])
    for p in paras:
        t = p.text
        text = t.lower()
        w = re.findall('[a-z][a-z\w]*', text)
        words = set(w)
        words.difference_update(INDEX_IGNORE)
        for w in words:
            index.update([(w, course_id)])

def create_course_map(course_map_filename):
    '''
    Creates a course map dictionary from a JSON file.

    Inputs:
        course_map_filename: string
    Returns:
        dictionary
    '''
    with open(course_map_filename, 'r') as f:
        course_map = json.load(f)
    return course_map

def generate_csv_file(index, index_filename):
    '''
    Writes index to a CSV file.

    Inputs:
        index: list
        index_filename: string
    '''
    index = sorted(index)
    with open(index_filename, 'w') as f:
        index_writer = csv.writer(f, delimiter='|')
        for i in index:
            index_writer.writerow([i[1], i[0]])


def create_queue(starting_url):
    '''
    Creates a queue starting from a given url

    Inputs:
        starting_url: string

    Returns:
        queue
    '''
    all_urls = queue.Queue()
    all_urls.put(starting_url)
    return all_urls

def visit_page(url):
    '''
    Uses bs4 to parse a html webpage

    Inputs:
        url: string

    Returns:
        bs4 object
    '''
    request = util.get_request(url)
    if request == None:
        return None    
    text = util.read_request(request)
    if text == None:
        return None
    soup = bs4.BeautifulSoup(text, 'html5lib')
    return soup

def extract_urls(q, url, soup, limiting_domain):
    '''
    Adds urls to a queue from a bs4 object

    Inputs:
        q: queue
        url: string
        soup: bs4 object from html page
        limiting_domain: string
    Returns:
        queue
    '''
    all_tags = soup.find_all('a')

    for tag in all_tags:
        if tag.has_attr('href'):
            new_url = tag['href']
            new_url = util.remove_fragment(new_url)
            new_url = util.convert_if_relative_url(url, new_url)
            if util.is_url_ok_to_follow(new_url, limiting_domain):
                if new_url not in q.queue:
                    q.put(new_url)

    return q


def go(num_pages_to_crawl, course_map_filename, index_filename):
    '''
    Crawl the college catalog and generates a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs: 
        CSV file of the index index.
    '''

    starting_url = "http://www.classes.cs.uchicago.edu/archive/2015/winter/12200-1/new.collegecatalog.uchicago.edu/index.html"
    limiting_domain = "classes.cs.uchicago.edu"

    
    pages_crawled = 0
    pages_visited = []
    all_urls = create_queue(starting_url)
    index = set()
    course_map = create_course_map(course_map_filename)

    while pages_crawled < num_pages_to_crawl:
        if all_urls.empty():
            break
        url = all_urls.get()
        if url not in pages_visited:
            pages_visited.append(url)
            soup = visit_page(url)
            if soup == None:
                break
            index_page(soup, index, course_map)
            all_urls = extract_urls(all_urls, url, soup, limiting_domain)
            pages_crawled += 1

        else:
            continue

    generate_csv_file(index, index_filename)

    limiting_domain = "cs.uchicago.edu"

if __name__ == "__main__":
    usage = "python3 crawl.py <number of pages to crawl>"
    args_len = len(sys.argv)
    course_map_filename = "course_map.json"
    index_filename = "catalog_index.csv"
    if args_len == 1:
        num_pages_to_crawl = 1000
    elif args_len == 2:
        try:
            num_pages_to_crawl = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)    
        sys.exit(0)
    go(num_pages_to_crawl, course_map_filename, index_filename)