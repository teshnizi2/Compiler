import string

symbol_table = [["keyword", "if"], ["keyword", "else"], ["keyword", "void"], ["keyword", "int"], ["keyword", "while"],
                ["keyword", "break"], ["keyword", "switch"], ["keyword", "default"], ["keyword", "case"],
                ["keyword", "return"], ["keyword", "endif"]]
simple_symbols = [';', ':', ',', '[', ']', '{', '}', '(', ')', '+', '-', '<']
all_symbols = [';', ':', ',', '[', ']', '{', '}', '(', ')', '+', '-', '<', '*', '=', "==", "/"]
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
white_space = ["\n", "\r", "\t", "\v", "\f", " "]
keyword = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "endif"]
alphabet = list(string.ascii_letters)
valid_tokens = ["SYMBOL", "ID", "NUM", "KEYWORD"]
token_lineno = 0
error_lineno = 0
symbol_table_lineno = 0
line_number = 1
have_error = False
input_file = open("input.txt", 'r')
token_file = open("tokens.txt", 'w+')
symbol_table_file = open("symbol_table.txt", 'w+')
errors_file = open("lexical_errors.txt", 'w+')


# error_1 unexpected end of comment, comment ended without starting
# error_2 unexpected end of comment, comment started without ending
# error_3 invalid number
# error_4 invalid input


def get_next_token(look_ahead_char):
    global line_number
    current_char = look_ahead_char
    current_token = current_char
    if not current_char:
        return ("eof", None, None)
    look_ahead_char = input_file.read(1)

    # symbols

    # else "/" , "*" , "=" , "=="
    if current_char in simple_symbols:
        return ("SYMBOL", current_char, look_ahead_char)
    # "=" , "=="
    if current_char == '=':
        if look_ahead_char == '=':
            look_ahead_char = input_file.read(1)
            return ("SYMBOL", "==", look_ahead_char)
        else:
            if look_ahead_char in white_space or look_ahead_char in all_symbols or look_ahead_char == '' or look_ahead_char in alphabet or look_ahead_char in digits:
                return ("SYMBOL", "=", look_ahead_char)
            else:
                current_char = look_ahead_char
                look_ahead_char = input_file.read(1)
                return ("error_4", "="+current_char,look_ahead_char)
    # "*" , error "*/"
    if current_char == '*':
        if look_ahead_char == '/':
            look_ahead_char = input_file.read(1)
            return ("error_1", "*/", look_ahead_char)
        else:
            return ("SYMBOL", "*", look_ahead_char)

    # comment and symbol "/"
    if current_char == '/':
        # comment "//"
        if look_ahead_char == '/':
            while (True):
                current_char = look_ahead_char
                look_ahead_char = input_file.read(1)
                if look_ahead_char == '\n':
                    look_ahead_char = input_file.read(1)
                    line_number += 1
                    return ("comment", "", look_ahead_char)
                elif look_ahead_char == "":
                    return ("comment", "", look_ahead_char)
        # comment "/* */"
        elif look_ahead_char == '*':
            line_number_plus = 0
            commentstring = ""
            while (True):
                current_char = look_ahead_char
                look_ahead_char = input_file.read(1)
                commentstring = commentstring + look_ahead_char
                if look_ahead_char == '':  # error_2
                    return ("error_2", commentstring, look_ahead_char)
                if look_ahead_char == '\n':  # error_2
                    line_number_plus += 1
                if look_ahead_char == "*":
                    current_char = look_ahead_char
                    look_ahead_char = input_file.read(1)
                    if look_ahead_char == "/":
                        current_char = look_ahead_char
                        look_ahead_char = input_file.read(1)
                        line_number += line_number_plus
                        return ("comment", "", look_ahead_char)
                    else:
                        commentstring += '*'
        # comment "/"
        else:
            return ("SYMBOL", "/", look_ahead_char)
    # Number
    if current_char in digits:
        while look_ahead_char in digits:
            # update current token
            current_token += look_ahead_char
            # update chars
            current_char = look_ahead_char
            look_ahead_char = input_file.read(1)

        if look_ahead_char in white_space or look_ahead_char in all_symbols or look_ahead_char == '':
            return ("NUM", current_token, look_ahead_char)
        elif look_ahead_char in alphabet:
            current_token += look_ahead_char
            current_char = look_ahead_char
            look_ahead_char = input_file.read(1)
            return ("error_3", current_token, look_ahead_char)
        else:
            current_token += look_ahead_char
            current_char = look_ahead_char
            look_ahead_char = input_file.read(1)
            return ("error_4", current_token, look_ahead_char)

    # ID and Keyword
    if current_char in alphabet:
        while look_ahead_char in alphabet or look_ahead_char in digits:
            # update current token
            current_token += look_ahead_char
            # update chars
            current_char = look_ahead_char
            look_ahead_char = input_file.read(1)

        if look_ahead_char in white_space or look_ahead_char in all_symbols or look_ahead_char == '':
            return ("ID or Keyword", current_token, look_ahead_char)
        else:
            current_token += look_ahead_char
            current_char = look_ahead_char
            look_ahead_char = input_file.read(1)
            return ("error_4", current_token, look_ahead_char)
    # white_space
    if current_char in white_space:
        if current_char == "\n":
            line_number += 1
        return ("white_space", "", look_ahead_char)

    return ("error_4", current_token, look_ahead_char)


# install ID
def install_ID(ID):
    symbol_table
    symbol_ID = ["ID", ID]
    if not (symbol_ID in symbol_table):
        symbol_table.append(symbol_ID)


# ID or Keyword
def isKeyword(lexime):
    if lexime in keyword:
        return (True)
    return (False)


# symbol table file
def symboltable2file():
    length = len(symbol_table)
    i = 0
    while (i < length):
        symbol_table_file.write(str(i + 1) + ".\t" + symbol_table[i][1] + "\n")
        i = i + 1


# Tokens file
def token2file(token_type, token_lexime):
    global token_lineno
    if (token_lineno != line_number):
        token_lineno = line_number
        if (line_number != 1):
            newlinestring = "\n" + str(line_number) + ".\t"
        else:
            newlinestring = str(line_number) + ".\t"
        token_file.write(newlinestring)
    string = '(' + token_type + ', ' + token_lexime + ') '
    token_file.write(string)


# Error file
def error2file(error_type, error_string):
    global have_error
    have_error = True
    global error_lineno
    if (error_lineno != line_number):
        if (error_lineno != 0):
            newlinestring = "\n" + str(line_number) + ".\t"
        else:
            newlinestring = str(line_number) + ".\t"
        errors_file.write(newlinestring)
    error_lineno = line_number
    if (error_type == "error_1"):
        errors_file.write("(*/, Unmatched comment) ")
    elif (error_type == "error_2"):
        errors_file.write("(" + "/*" + error_string[0:5] + "...," + " Unclosed comment" + ")")
    elif (error_type == "error_3"):
        errors_file.write("(" + error_string + ", Invalid number) ")
    elif (error_type == "error_4"):
        errors_file.write("(" + error_string + ", Invalid input) ")


# Main
lookahead_char = input_file.read(1)
current_token = get_next_token(lookahead_char)
while (current_token[0] != "eof"):
    if (current_token[0] == "SYMBOL"):
        token2file(current_token[0], current_token[1])
    elif (current_token[0] == "ID or Keyword"):
        if (isKeyword(current_token[1])):
            token2file("KEYWORD", current_token[1])
        else:
            install_ID(current_token[1])
            token2file("ID", current_token[1])
    elif (current_token[0] == "NUM"):
        token2file(current_token[0], current_token[1])
    if (current_token[0][0:5] == "error"):
        error2file(current_token[0], current_token[1])
    lookahead_char = current_token[2]
    current_token = get_next_token(lookahead_char)
if have_error == False:
    errors_file.write("There is no lexical error.")
symboltable2file()












