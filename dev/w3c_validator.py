"""
W3C validator for Holberton School

Validates HTML and CSS files using two APIs:
- https://validator.w3.org/nu/ for HTML
- http://jigsaw.w3.org/css-validator/validator for CSS

Usage:

For a single file:

For multiple files:

All errors are printed to STDERR.

Exit status:
- Number of errors (#) on failure
- 0 on success

References:

https://developer.mozilla.org/en-US/
"""
import sys
import requests


def __print_stdout(msg):
    """Print message to STDOUT"""
    sys.stdout.write(msg)


def __print_stderr(msg):
    """Print message to STDERR"""
    sys.stderr.write(msg)


def __analyse_html(file_path):
    """Analyzes an HTML file"""
    headers = {'Content-Type': "text/html; charset=utf-8"}
    data = open(file_path, "rb").read()
    url = "https://validator.w3.org/nu/?out=json"
    response = requests.post(url, headers=headers, data=data)
    errors = []
    messages = response.json().get('messages', [])
    for msg in messages:
        errors.append("[{}:{}] {}".format(file_path, msg['lastLine'], msg['message']))
    return errors


def __analyse_css(file_path):
    """Analyzes a CSS file"""
    data = {'output': "json"}
    files = {'file': (file_path, open(file_path, 'rb'), 'text/css')}
    url = "http://jigsaw.w3.org/css-validator/validator"
    response = requests.post(url, data=data, files=files)
    errors = []
    css_errors = response.json().get('cssvalidation', {}).get('errors', [])
    for error in css_errors:
        errors.append("[{}:{}] {}".format(file_path, error['line'], error['message']))
    return errors


def __analyse(file_path):
    """Starts analysis of a file"""
    num_errors = 0
    try:
        result = None
        if file_path.endswith('.css'):
            result = __analyse_css(file_path)
        else:
            result = __analyse_html(file_path)

        if len(result) > 0:
            for msg in result:
                __print_stderr("{}\n".format(msg))
                num_errors += 1
        else:
            __print_stdout("{}: OK\n".format(file_path))

    except Exception as e:
        __print_stderr("[{}] {}\n".format(e.__class__.__name__, e))
    return num_errors


def __files_loop():
    """Loop to analyze each file from input arguments"""
    num_errors = 0
    for file_path in sys.argv[1:]:
        num_errors += __analyse(file_path)
    return num_errors


if __name__ == "__main__":
    """Main function"""
    if len(sys.argv) < 2:
        __print_stderr("usage: w3c_validator.py file1 file2 ...\n")
        exit(1)

    """Execute tests and exit. Exit status = number of errors (0 on success)"""
    sys.exit(__files_loop())

