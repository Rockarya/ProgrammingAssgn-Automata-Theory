<PFA attached VIDEO>
(The size was not big so i am attaching with it only)


q1) Convert regular expression to NFA :      
-> The conversion of regular expression to NFA takes place in regex_to_nfa() fxn in q1.py.
-> We traverse through the entire sequence and process each character one at a time.
' ' : if we found a space bar, then we continue move forward.
'+' : if we found a union operation then, we call the same fxn but here passing latter part of the sequence i.e. from i+1 to end.(breaking the previous one)
'(' : if we found an opening bracket(let at pos=i) then, firstly we find the corresponding closing bracket(let at pos=j) then we call the fxn from (i+1,j-1) and moving the pointer to j+1.
'*' : if we found a kleen's closure operator then we look at the previous character of it and do the self-looping
Otherwise if we found a symbol, then firstly we include it our array containing all symbols encountered, and then add a new-node, new-edge corresponding to this symbol.
-> q1 is one of final state and those nodes from which taking $ transition makes us reach q1 are too included in final states.




q2) Convert NFA to DFA :
-> Suppose we have n states of NFA, then we need to create all 2^n states for DFA(i.e. power-set of all the states of the nfa)
-> After creating all the DFA states, we will see where the state proceeds to at each letter.(This is done using transition fxn of NFA)
-> We will obtain the transition fxn for DFA. Letters,Start states of DFA will be same as of NFA.
-> The final states of DFA will be all states containing either of the state of NFA.




q3) Convert DFA to Regular expression :
-> Firstly we are converting the given DFA to GNFA(adding new starting node and new end node)[Also handling the case when more than 1 letter transist b/w same nodes]
-> After that we are calling dfa_to_regex fxn where:-
        -> initially we are finding if there is any self-looping involved on the node(viz. passed to the fxn) and finding all letters involved in self looping
        -> After that we are finding incoming_edge's node and outgoing_edge's node and finding the indirect path from it.
        -> Also here we are also finding the direct path from incoming_edge's node and outgoing_edge's node and taking union with the expression.
        -> Also if there are self-loops involved on the node(checking by the flag raised above) we are adding the expression here only
        -> Append it in the transition fxn
-> After processing of dfa_to_regex fxn is done we are popping up the all the transitions available from this node(as they are of no use now)
-> For each node(except the start and end node), we are calling the dfa_to_regex fxn and when no valid nodes are there, we stop and the first transition of the trans_fxn array will be the required regex for the DFA





q4) Minimize a DFA :
-> Firstly removed all the dead/end states
-> Applying dfa minimize algorithm to minimize the given dfa:-
    -> So firstly we will seperate all the non-dead states into 2 sets of final states and non-final states
    -> Now for taking 2 nodes of a set at a time, we will see if for each letter they transist to the same set or not. If not then we divide them into 2 new sets, else we continue mapping till all pairs are considered and if all matches then we stop, hence the dfa we got is thus minimized dfa
-> The start states of the minimized dfa will be all nodes which have either of the start states of original dfa
-> Similarly the final states of minimized fa will be all nodes having either of the final states of original dfa.
-> For transition fxn we look at either(any one) of the state of a node of minimized dfa(as for a particular letter each will transisit to same state, that's why they are together) and we find the node in minimized dfa to which this state transist to for a particular letter.
