def color_text(text, color_code, bold=False) -> str:
    bold_code = "1;" if bold else ""
    return f"\033[{bold_code}{color_code}m{text}\033[0m"

def red_text(text, bold=False) -> str:
    return color_text(text, "91", bold)

def green_text(text, bold=False) -> str:
    return color_text(text, "92", bold)

def yellow_text(text, bold=False) -> str:
    return color_text(text, "93", bold)

def blue_text(text, bold=False) -> str:
    return color_text(text, "94", bold)

def magenta_text(text, bold=False) -> str:
    return color_text(text, "95", bold)

def cyan_text(text, bold=False) -> str:
    return color_text(text, "96", bold)



def print_error(message):
    print(red_text(message))

def print_warning(message):
    print(yellow_text(message))

def print_info(message):
    print(blue_text(message))

def print_success(message):
    print(green_text(message))

def print_title(message):
    print(magenta_text(message))

def print_debug(message):
    print(cyan_text(message))


def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
    

if __name__ == "__main__":
    print_error("Error message")
    print_warning("Warning message")
    print_info("Info message")
    print_success("Success message")
    print_title("Title message")
    print_debug("Debug message")
    print_progress_bar(10, 100)
