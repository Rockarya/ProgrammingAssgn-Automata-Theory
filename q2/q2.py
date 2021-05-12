import sys, json

# reading data from file
with open(sys.argv[1], 'r') as f_read:
    nfa_data = json.load(f_read)
    nfa_trans_fxn = nfa_data['transition_function']
    nfa_states = nfa_data['states']
    nfa_letters = nfa_data['letters']
    nfa_start_states = nfa_data['start_states']
    nfa_final_states = nfa_data['final_states']
    

dfa_states = []
dfa_letters = []
dfa_start_states = []
dfa_final_states = []
dfa_trans_fxn = []

# creating all possible states for dfa
for i in range(pow(2,len(nfa_states))):
    dfa_states.append([])
    for j in range(len(nfa_states)):
        if (i & 1<<j):
            dfa_states[i].append(nfa_states[j])
            
# transitions from null states  
for i in range(len(nfa_letters)):
    dfa_trans_fxn.append([[],nfa_letters[i],[]])

# transitions from non-null states
for d_s in range(len(dfa_states)):
    if len(dfa_states[d_s]) != 0:
        
        # traverse over all letters
        for n_l in range(len(nfa_letters)):
            start_state = []
            final_state = []
            
            # looking at each character of a state in dfa
            for st in range(len(dfa_states[d_s])):
                start_state.append(dfa_states[d_s][st])
                # taking union of final states
                for t_f in range(len(nfa_trans_fxn)):
                    if nfa_trans_fxn[t_f][0] == dfa_states[d_s][st] and nfa_trans_fxn[t_f][1] == nfa_letters[n_l]:
                        final_state.append(nfa_trans_fxn[t_f][2])
                        
            #finally appending start and end state in dfa transition fxn   
            dfa_trans_fxn.append([start_state,nfa_letters[n_l],final_state])
        
                
# all dfa_states having nfa_final_states are final states
for i in range(len(dfa_states)):
    flag = 0
    for j in range(len(nfa_final_states)):
        if nfa_final_states[j] in dfa_states[i]:
            flag = 1
            dfa_final_states.append(dfa_states[i])
            break          

# start states and letters are same
dfa_start_states = nfa_start_states
dfa_letters = nfa_letters


output_json = {}
output_json['states'] = dfa_states
output_json['letters'] = dfa_letters
output_json['transition_matrix'] = dfa_trans_fxn
output_json['start_states'] = dfa_start_states
output_json['final_states'] = dfa_final_states

with open(sys.argv[2], 'w') as f_write:
    json.dump(output_json, f_write, indent=1)
