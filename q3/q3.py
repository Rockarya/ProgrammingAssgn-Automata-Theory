import sys,json

# reading input
with open(sys.argv[1], 'r') as f_read:
   dfa_data = json.load(f_read)
   states = dfa_data['states']
   sybmols = dfa_data['letters']
   trans_fxn = dfa_data['transition_function']
   start_states = dfa_data['start_states']
   end_states = dfa_data['final_states']
   
new_start_state = 'S'
new_end_state = 'E'
obtained_regex = ''
output_json = {}


def dfa_to_gnfa():
    # add new start state
    states.append(new_start_state)
    for i in range(len(start_states)):
        trans_fxn.append([new_start_state, "$", start_states[i]])
        
    # add new end state
    states.append(new_end_state)
    for i in range(len(end_states)):
        trans_fxn.append([end_states[i], "$", new_end_state])
        
    # merging all edges which traverse from same 2 nodes
    for i in range(len(trans_fxn)):
        for j in range(len(trans_fxn)):
            
            new_symbol = []
            for k in range(len(trans_fxn)):
                if trans_fxn[i][0] == trans_fxn[k][0] and trans_fxn[j][2] == trans_fxn[k][2] and trans_fxn[k][1]!='-1':
                    new_symbol.append(trans_fxn[k][1])
                    trans_fxn[k][1] = '-1'
            
            smb_len = len(new_symbol)    
            if smb_len != 0:
                give_symbol = ''
                if smb_len == 1:
                    give_symbol = new_symbol[0]
                else:
                    give_symbol += '($ '
                    for k in range(smb_len):
                        give_symbol += ('+ ' + new_symbol[k])
                    give_symbol += ')'
                trans_fxn.append([trans_fxn[i][0],give_symbol,trans_fxn[j][2]])
                
                
    # removing  the edges that we already added as new_symbols 
    should_continue = 1
    while(should_continue):
        should_continue = 0
        for i in range(len(trans_fxn)):
            if trans_fxn[i][1] == '-1':
                trans_fxn.pop(i)
                should_continue = 1
                break
            
            
    
def dfa_to_regex(node):
    looping_edge = '$'
    looping_edge_flag = 0
        
    global states, trans_fxn
    while(1):
        flag = 0
        for i in range(len(trans_fxn)):
            if (node == trans_fxn[i][0]) and (node == trans_fxn[i][2]):
                looping_edge_flag = 1
                looping_edge += '+' + trans_fxn[i][1]
                trans_fxn.pop(i)
                flag = 1
                break
        if flag == 0:
            break
        
    if looping_edge_flag == 1:
        looping_edge = '(' + looping_edge + ')'

    for i in range(len(trans_fxn)):
        for j in range(len(trans_fxn)):
            if node == trans_fxn[i][2] and node == trans_fxn[j][0]:
                start_node = trans_fxn[i]
                end_node = trans_fxn[j]
                    
                if start_node[1] == '$':
                        indirect_edge = ''
                else:
                    indirect_edge = start_node[1]
                    
                if looping_edge != '$' and looping_edge_flag:
                    indirect_edge += looping_edge + '*'
                    
                if end_node[1] != '$':
                    indirect_edge += end_node[1]
                    
                    
                path = indirect_edge
                itr = 0
                for st in trans_fxn:
                    if (st[0] == start_node[0]) and (st[2] == end_node[2]):
                        direct_edge = st[1]
                        path = '(' + indirect_edge + '+' + direct_edge + ')'
                        trans_fxn.pop(itr)
                        break
                    itr+=1
                
                trans_fxn.append([start_node[0], path, end_node[2]])

    should_continue = 1
    while(should_continue):
        should_continue = 0
        for i in range(len(trans_fxn)):
            if (node == trans_fxn[i][0]) or (node == trans_fxn[i][2]):
                trans_fxn.pop(i)
                should_continue = 1
                break  

    return


# This function converts dfa to gnfa(basically appends the new start state with $ transition to initial start state and similarly add a new final state with $ transition from initial final state)
dfa_to_gnfa()

# till we do not remove all the nodes except the added start node and end node
while len(states) != 2:
    itr = 0
    for st in states:
        # if state is neither start nor end state
        if st[itr] != new_start_state and st[itr] != new_end_state:
            dfa_to_regex(states[itr])
            states.pop(itr)
            break
        itr+=1
        
# writing output 
obtained_regex = trans_fxn[0][1]
output_json['regex'] = obtained_regex

with open(sys.argv[2], 'w') as f_write:
    json.dump(output_json, f_write, indent=1)
