import re
import time
import urllib.request
from datetime import datetime


# Universal functions

def get_html(url):
    """Takes URL and returns its HTML response as string."""
    with urllib.request.urlopen(url) as response:
        html = str(response.read())
    return html


def match_first(pattern, text):
    """Returns the first regex match in a given string.

    Kwargs:
        pattern -- must be a valid regex expression, e.g. r'^foo.*'
        text -- a string which will be searched for the pattern
    """
    match = re.findall(pattern, text)[0]
    return match


def append_text_file(filename, data):
    """Writes data to a text file in appending mode.

    Kwargs:
        filename -- e.g. 'log.txt', will be created if it doesn't exist
        data -- must be a string
    """
    with open(filename, 'a') as f:
        f.write(data)
        f.close


# Program specific functions

def extract_ip(text):
    """Returns the first IP address found in text.

    The hardcoded pattern matches any IP address, also '999.999.999.999'.

    Kwargs:
        text -- e.g. HTML of a page as string
    """
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ip = match_first(pattern, text)
    return ip


def build_log(data):
    """Builds and returns a row of data for the log file.

    Kwargs:
        data -- should be a string without newline characters
    """
    log = str(datetime.now()) + '\t' + data + '\n'
    return log


# Main program

def main(interval):
    """Main program which triggers other functions and runs in a loop.

    Kwargs:
        interval -- should be a float, represents number of seconds the
        script sleeps between runs
    """
    url = 'http://www.whatismyip.org/'  # This can work with other websites
    while True:
        html = get_html(url)
        ip = extract_ip(html)
        print('Your current IP:', ip)

        log = build_log(ip)
        append_text_file('log.txt', log)

        print('Sleeping for', interval, 'seconds ...')
        time.sleep(interval)


if __name__ == '__main__':
    """Command shell interface for getting user input."""
    print('External IP Monitor v1.0')
    user_input = input('Time between checks (in seconds): ')

    # Validate user input
    while True:
        try:
            # Try to validate user input by turning it into a float
            validated_input = float(user_input)
            # If user input passes float conversion, start the program
            main(float(user_input))
        except ValueError:
            # If float conversion fails, request user input again
            user_input = input('Input error. Please provide a valid number: ')
