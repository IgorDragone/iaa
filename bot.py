import pysmile
import pysmile_license
import random

states = ["Atacar", "Recoger_Armas", "Recoger_Energia", "Explorar", "Huir",  "Detectar_Peligro" ]

def botStateProbability(stValue = "Atacar" ):
    net = pysmile.Network()
    net.read_file("BotIaa.xdsl")
    st = stValue
    h = "Alta"
    w = "armado"
    ow = "armado"
    hn = "si"
    ne = "si"
    pw = "si"
    ph = "si"
    evidence = { "St": st,  "H": h, "W": w, "OW": ow, "HN": hn, "NE": ne, "PW": pw, "PH": ph }
    for node_name, value in evidence.items():
        net.set_evidence(node_name, value)
    net.update_beliefs()
    return net.get_node_value("st_1")

def selectPosition(probabilities):
  indexes = list(range(len(probabilities)))
  new_index = random.choices(indexes, weights=probabilities, k=1)[0]
  return new_index

def predictNextState():
    print("Bot's probability at t+1 is:")
    print(states)
    prob = botStateProbability()
    newState = selectPosition(prob)
    for i in range(10):
        prob = botStateProbability(states[newState])
        print(prob)
        newState = selectPosition(prob)


def learnFromData():
    net = pysmile.Network()
    net.read_file("BotIaa.xdsl")
    #we get the data from the txt file learning_cases.txt
    data = pysmile.learning.DataSet()
    data.read_file("learning_cases.txt")
    matching = data.match_network(net)
    #we create a learning algorithm
    algorithm = pysmile.learning.EM()
    algorithm.learn(data, net, matching)
    
    #we save the network
    net.write_file("BotIaaLearned.xdsl")
    print("The network has been learned from the data")

    #We visualize the new probability tables
    new_net = pysmile.Network()
    new_net.read_file("BotIaaLearned.xdsl")
    for h in new_net.get_all_nodes():
        print_node_info(new_net, h)
    
    

def print_node_info(net, node_handle):
    print("Node id/name: " + net.get_node_id(node_handle) + "/" +
    net.get_node_name(node_handle))
    print(" Outcomes: " + " ".join(net.get_outcome_ids(node_handle)))
    print_cpt_matrix(net, node_handle)

def print_cpt_matrix(net, node_handle):
    cpt = net.get_node_definition(node_handle) 
    parents = net.get_parents(node_handle) 
    dim_count = 1 + len(parents)

    dim_sizes = [0] * dim_count
    for i in range(0, dim_count - 1):
        dim_sizes[i] = net.get_outcome_count(parents[i]) 
        
    dim_sizes[len(dim_sizes) - 1] = net.get_outcome_count(node_handle)
    coords = [0] * dim_count
    for elem_idx in range(0, len(cpt)):
        index_to_coords(elem_idx, dim_sizes, coords)
        outcome = net.get_outcome_id(node_handle, coords[dim_count - 1])
        out_str = " P(" + outcome
        if dim_count >  1:
            out_str += " | "
            for parent_idx in range(0, len(parents)):
                if parent_idx > 0: 
                    out_str += ","
                parent_handle = parents[parent_idx]
                out_str += net.get_node_id(parent_handle) + "=" + \
                net.get_outcome_id(parent_handle, coords[parent_idx])
                
        prob = cpt[elem_idx] 
        out_str += ")=" + str(prob) 
        print(out_str)

def index_to_coords(index, dim_sizes, coords):
    prod = 1
    for i in range(len(dim_sizes) - 1, -1, -1): 
        coords[i] = int(index / prod) % dim_sizes[i] 
        prod *= dim_sizes[i]

def main():
    #predictNextState()
    learnFromData()
main()


# #The first line is the header, so we skip it
#     lines = lines[1:]
#     #we iterate over the lines of the file
#     for line in lines:
#         #we split the line by the character ","
#         values = line.split(",")
#         #we get the values of the states
#         h = values[0]
#         hn = values[1]
#         ne = values[2]
#         ow = values[3]
#         ph = values[4]
#         pw = values[5]
#         st = values[6]
#         st_1 = values[7]
#         w = values[8]
#         #the last value ends with a new line character, so we remove it
#         w = w[:-1]
#         #we set the evidence
#         evidence = { "St": st,  "H": h, "W": w, "OW": ow, "HN": hn, "NE": ne, "PW": pw, "PH": ph, "st_1": st_1 }
#         for node_name, value in evidence.items():
#             net.set_evidence(node_name, value)
#         net.update_beliefs()