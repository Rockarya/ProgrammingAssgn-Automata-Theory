import sys, json

# reading data from file
with open(sys.argv[1], 'r') as f_read:
    org_dfa_data = json.load(f_read)
    trans_fxn = org_dfa_data['transition_function']
    states = org_dfa_data['states']
    letters = org_dfa_data['letters']
    start_states = org_dfa_data['start_states']
    final_states = org_dfa_data['final_states']

    
# final and non-final state
f_state = []
nf_state = []
eq_set = []
min_tra_fxn = []
min_start_states = []
min_states = []
min_final_states = []
output_json = {}

# valid states will contain all states after removing the dead/end states
valid_states = []
valid_states = start_states

def dfs(node):
    global valid_states
    for i in range(len(trans_fxn)):
        if node == trans_fxn[i][0]:
            if trans_fxn[i][2] not in valid_states:
                valid_states.append(trans_fxn[i][2])
                dfs(trans_fxn[i][2])
                
for i in range(len(start_states)):
    dfs(start_states[i])


# creating P0 for final and non-final state
for i in range(len(valid_states)):
    if valid_states[i] in final_states:
        f_state.append(valid_states[i])
    else:
        nf_state.append(valid_states[i])
        
    
eq_set.append([])
eq_set[0].append(f_state)
eq_set[0].append(nf_state)


# ideally for each set we should find the node which do not transist to states belonging to same set for a particular letter. But same can be accomplished if we take the first state 
# of a set and find all states which can be combined with it, lastly we will check if every state macthes with the first state then no partition is needed.

count = 0
should_continue = 1
while(should_continue):
    should_continue = 0
    for i in range(len(eq_set[count])):
        
        if len(eq_set[count][i]) > 1:

            s1 = []
            s1.append(eq_set[count][i][0])
            s2 = []
            for pos in range(1,len(eq_set[count][i])):
                
                should_add = 1
                for l in range(len(letters)):
                    
                    node1 = ''
                    node2 = ''
                    for t_f in range(len(trans_fxn)):
                        if trans_fxn[t_f][0] == eq_set[count][i][0] and trans_fxn[t_f][1] == letters[l]:
                            node1 = trans_fxn[t_f][2]
        
                        if trans_fxn[t_f][0] == eq_set[count][i][pos] and trans_fxn[t_f][1] == letters[l]:
                            node2 = trans_fxn[t_f][2]    
                    
                    flag = 1
                    for eq in range(len(eq_set[count])):
                        if (node1 in eq_set[count][eq]) and (node2 in eq_set[count][eq]):
                            flag = 0   
                            
                    if flag == 1:   
                        should_add = 0
                        break
                    
                if should_add == 1:
                    s1.append(eq_set[count][i][pos])
                else:
                    s2.append(eq_set[count][i][pos])
            
            if (len(s1) == len(eq_set[count][i])) or (len(s2) == len(eq_set[count][i])):
                continue
            else:
                eq_set.append([])
                for itr in range(i):
                    eq_set[count+1].append(eq_set[count][itr])
                    
                eq_set[count+1].append(s1)
                eq_set[count+1].append(s2)
                
                for itr in range(i+1,len(eq_set)):
                    eq_set[count+1].append(eq_set[count][itr])
                
                count+=1
                should_continue = 1
                break
            
            
# new states of minimized dfa
min_states = eq_set[count]


# reading data from file(Again because facing some issue with start states)
with open(sys.argv[1], 'r') as f_read:
    data = json.load(f_read)
    start_states = data['start_states']

# start states of minimized dfa   
for i in range(len(eq_set[count])):
    for j in range(len(eq_set[count][i])):
        if eq_set[count][i][j] in start_states:
            min_start_states.append(eq_set[count][i])
            break
            
# final states of minimized states
for i in range(len(eq_set[count])):
    for j in range(len(eq_set[count][i])):
        if eq_set[count][i][j] in final_states:
            min_final_states.append(eq_set[count][i])
            break
 
# transition fxn for minimized dfa    
for l in range(len(letters)):
    for i in range(len(eq_set[count])):
        reached_state = ''
        for t_f in range(len(trans_fxn)):
            if trans_fxn[t_f][0] == eq_set[count][i][0] and trans_fxn[t_f][1] == letters[l]:
                reached_state = trans_fxn[t_f][2]
                break
            
        for j in range(len(min_states)):
            if reached_state in min_states[j]:
                min_tra_fxn.append([eq_set[count][i],letters[l],min_states[j]])
                break


output_json['states'] = min_states
output_json['letters'] = letters
output_json['transition_matrix'] = min_tra_fxn
output_json['start_states'] = min_start_states
output_json['final_states'] = min_final_states

with open(sys.argv[2], 'w') as f_write:
    json.dump(output_json, f_write, indent=1)