import scanner
import json
from anytree import Node, RenderTree
input_file = open("input.txt", 'r')

# token_file = open("tokens.txt", 'w+')
# symbol_table_file = open("symbol_table.txt", 'w+')
# errors_file = open("lexical_errors.txt", 'w+')
syntax_errors = open("syntax_errors.txt", 'w+')
tree_file= open("parse_tree.txt", 'w+',encoding='utf-8')
lookahead_char = None
current_token = None
json_file = json.load(open("table.json"))


# Main
def get_next_token_parser():
    global input_file
    # global token_file
    # global symbol_table_file
    # global errors_file
    global lookahead_char
    global current_token
    while True:
        if current_token is None:
            lookahead_char = input_file.read(1)
            current_token = scanner.get_next_token(lookahead_char, input_file)
        else:
            lookahead_char = current_token[2]
            current_token = scanner.get_next_token(lookahead_char, input_file)
        token = None
        return_tuple = (current_token[0], current_token[1])
        if current_token[0] == "SYMBOL":
            # scanner.token2file(current_token[0], current_token[1], token_file)
            token = current_token[1]
        elif current_token[0] == "ID or Keyword":
            if scanner.isKeyword(current_token[1]):
                # scanner.token2file("KEYWORD", current_token[1], token_file)
                token = current_token[1]
                return_tuple = ("KEYWORD", current_token[1])
            else:
                scanner.install_ID(current_token[1])
                # scanner.token2file("ID", current_token[1], token_file)
                token = "ID"
                return_tuple = ("ID", current_token[1])
        elif current_token[0] == "NUM":
            # scanner.token2file(current_token[0], current_token[1], token_file)
            token = "NUM"
        elif current_token[0] == "eof":
            token = "$"
        elif current_token[0][0:5] == "error":
            # scanner.error2file(current_token[0], current_token[1], errors_file)
            pass
        if token is not None:
            return token, return_tuple


def parser():
    parser_stack = ["0"]
    token, c_token = get_next_token_parser()
    parse_table = json_file["parse_table"]
    grammer = json_file["grammar"]
    reductions = []
    errors_string = ""
    tokens_in_stack = []
    nodes = []
    end_of_file = False
    while True:
        size = len(parser_stack)
        try:
            next_move, next_move_number = parse_table[parser_stack[size - 1]][token].split("_")
            # -----------------------------------------
            if next_move == "shift":
                if token == "$":
                    break
                parser_stack.append(token)
                nodes.append(Node(f"({c_token[0]}, {c_token[1]})"))
                parser_stack.append(str(next_move_number))
                tokens_in_stack.append(c_token)
                token, c_token = get_next_token_parser()
            # ----------------------------------------
            elif next_move == "reduce":
                reductions.append(next_move_number)
                current_rule = grammer[next_move_number]
                rule_size = len(current_rule) - 2
                non_terminal = current_rule[0]
                nodes.append(Node(non_terminal))
                if current_rule[2] == "epsilon":
                    rule_size = 0
                    Node("epsilon",parent=nodes[-1])
                nodes_size = len(nodes)
                for i in range(rule_size):
                    gorg_alpha = nodes.pop(nodes_size-rule_size-1)
                    gorg_alpha.parent = nodes[-1]
                del parser_stack[size - 2 * rule_size:]
                
                parser_stack.append(non_terminal)
                size = len(parser_stack)
                goto_num = parse_table[parser_stack[size - 2]][non_terminal].split("_")[1]
                parser_stack.append(str(goto_num))
            # ----------------------------------------
            elif next_move == "accept":
                break
        except:
            terminals = json_file["terminals"]
            non_terminals = json_file["non_terminals"]
            errors_string += f"#{scanner.line_number} : syntax error , illegal {c_token[1]}\n"
            token, c_token = get_next_token_parser()
            while not is_there_goto(parser_stack[-1]):
                parser_stack.pop()  # number
                removed_element = parser_stack.pop()  # terminal or nonterminal
                gorg_beta = nodes.pop()
                gorg_beta.parent = None
                if removed_element in terminals:
                    removed_element = tokens_in_stack.pop()
                    errors_string += f"syntax error , discarded ({removed_element[0]}, {removed_element[1]}) from stack\n"
                elif removed_element in non_terminals:
                    errors_string += f"syntax error , discarded {removed_element} from stack\n"
            while not token_in_follow(parser_stack[-1], token):
                if token == "$":
                    errors_string += f"#{scanner.line_number} : syntax error , Unexpected EOF\n"
                    end_of_file = True
                    break
                errors_string += f"#{scanner.line_number} : syntax error , discarded {c_token[1]} from input\n"
                token, c_token = get_next_token_parser()
            if end_of_file:
                break
            else:
                non_terminal = token_in_follow(parser_stack[-1], token)
                errors_string += f"#{scanner.line_number} : syntax error , missing {non_terminal}\n"
                parser_stack.append(non_terminal)
                nodes.append(Node(non_terminal))
                goto_num = parse_table[parser_stack[- 2]][non_terminal].split("_")[1]
                parser_stack.append(str(goto_num))
    if errors_string == "":
        errors_string = "There is no syntax error."
    syntax_errors.write(errors_string)
    nodes.append(Node("$",parent=nodes[-1]))
    if(not end_of_file):
        tree_string=""
        for pre, _, node in RenderTree(nodes[-2]):
            treestr = u"%s%s" % (pre, node.name)
            tree_string +=str(treestr.ljust(8))+"\n"
        tree_file.write(tree_string)


def is_there_goto(state_number):
    state_values = json_file["parse_table"][state_number].values()
    for i in state_values:
        if i.split("_")[0] == "goto":
            return True
    else:
        return False


def token_in_follow(state_number, terminal):
    keys = sorted(list(json_file["parse_table"][state_number].keys()))
    parse_table = json_file["parse_table"]
    follow = json_file["follow"]
    for i in keys:
        if parse_table[state_number][i].split("_")[0] == "goto":
            if terminal in follow[i]:
                return i
    else:
        return False


parser()
