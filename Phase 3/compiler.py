
import scanner

input_file = open("input.txt", 'r')
token_file = open("tokens.txt", 'w+')
symbol_table_file = open("symbol_table.txt", 'w+')
errors_file = open("lexical_errors.txt", 'w+')



# Main
lookahead_char = input_file.read(1)
current_token = scanner.get_next_token(lookahead_char, input_file)
while (current_token[0] != "eof"):
    if (current_token[0] == "SYMBOL"):
        scanner.token2file(current_token[0], current_token[1], token_file)
    elif (current_token[0] == "ID or Keyword"):
        if (scanner.isKeyword(current_token[1])):
            scanner.token2file("KEYWORD", current_token[1], token_file)
        else:
            scanner.install_ID(current_token[1])
            scanner.token2file("ID", current_token[1], token_file)
    elif (current_token[0] == "NUM"):
        scanner.token2file(current_token[0], current_token[1], token_file)
    if (current_token[0][0:5] == "error"):
        scanner.error2file(current_token[0], current_token[1],errors_file)
    lookahead_char = current_token[2]
    current_token = scanner.get_next_token(lookahead_char,input_file)
if scanner.have_error == False:
    errors_file.write("There is no lexical error.")
scanner.symboltable2file(symbol_table_file)



