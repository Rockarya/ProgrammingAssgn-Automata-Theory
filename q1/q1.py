# final states are not handles properly(most probably)
import sys, json

num_of_nodes = 0
states = []
trans_fxn = []
all_letters = []


def regex_to_nfa(ind_start, ind_end, sequence):
    global num_of_nodes, trans_fxn
    # initialising starting and ending bracket position
    bracket_start_pos = 0
    bracket_end_pos = 0
    
    if ind_start == -1:
        ind_start = num_of_nodes 
        states.append(('q{}'.format(num_of_nodes)))
        trans_fxn.append([])
        num_of_nodes += 1
        
    current_node = ind_start
    
    if ind_end == -1:
        ind_end = num_of_nodes 
        states.append(('q{}'.format(num_of_nodes)))
        trans_fxn.append([])
        num_of_nodes += 1

    i = 0
    while i < len(sequence):
        # continuing if found space
        if sequence[i] == ' ':
            i += 1
            continue
        
        # starting another conversion from (i+1) if found union operation
        elif sequence[i] == '+':
            regex_to_nfa(ind_start, ind_end, sequence[i+1:])
            break
        
        elif sequence[i] == '(':
            # finding ending bracket of the corresponding opening bracket
            end_bracket = 0
            count = 1
            for j in range(i + 1, len(sequence)):
                if sequence[j] == ')':
                    count -= 1
                    if count == 0:
                        end_bracket = j
                        break
                if sequence[j] == '(':
                    count += 1
                    
            # we know the startting node but not the ending node
            bracket_start_pos, bracket_end_pos = regex_to_nfa(current_node, -1, sequence[i+1:end_bracket])
            current_node = bracket_end_pos
            i = end_bracket + 1
            continue

        elif sequence[i] == '*':
            # self looping on the current node if found kleen's closure symbol
            if bracket_start_pos == bracket_end_pos:
                trans_fxn[current_node].append([sequence[i-1], current_node])
            else:
                trans_fxn[bracket_start_pos].append(['$', bracket_end_pos])
               

        else:
            all_letters.append(sequence[i])
            if i + 1 < len(sequence):
                if sequence[i + 1] == '*':
                    i += 1
                    continue
                
            new_node = num_of_nodes 
            states.append(('q{}'.format(num_of_nodes)))
            trans_fxn.append([])
            num_of_nodes += 1
            
            trans_fxn[current_node].append([sequence[i], new_node])
            current_node = new_node

        i += 1
        
    # adding null state to the last read node
    trans_fxn[current_node].append(['$', ind_end])
    return ind_start, ind_end



if __name__ == '__main__': 
    # reading data from file
    with open(sys.argv[1], 'r') as f_read:
        data = json.load(f_read)
        regex = data['regex']

    # calling regex to nfa conversion function(-1 denotes no ending state)
    regex_to_nfa(-1,-1,regex)

    # preparing arrays to write in json file
    letters = []
    for i in all_letters:
        flag = 1
        for j in letters:
            if i == j:
                flag = 0
                break
        if flag == 1:
            letters.append(i)
            
    # we will only be adding the immediate $ transitions of q1 as also final states
    final_states = ['q1']
    t_f= []   
    for i in range(num_of_nodes):
        for j in range(len(trans_fxn[i])):
            t_f.append(('q{}'.format(i), trans_fxn[i][j][0], 'q{}'.format(trans_fxn[i][j][1])))
            # adding final states having null transitions to q1(1 index)
            if trans_fxn[i][j][0] == '$' and trans_fxn[i][j][1] == 1:
                if i not in final_states:
                    final_states.append('q{}'.format(i))
            # adding final states having null transitions from q1
            if i == 1 and trans_fxn[i][j][0] == '$':
                if trans_fxn[i][j][1] not in final_states:
                    final_states.append('q{}'.format(trans_fxn[i][j][1]))
    
    output_json = {}
    output_json['states'] = states
    output_json['letters'] = letters
    output_json['transition_function'] = t_f
    output_json['start_states'] = ['q0']
    output_json['final_states'] = final_states
    
    with open(sys.argv[2], 'w') as f_write:
        json.dump(output_json, f_write, indent=1)
