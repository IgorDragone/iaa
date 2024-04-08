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

def main():
    print("Bot's probability at t+1 is:")
    print(states)
    prob = botStateProbability()
    newState = selectPosition(prob)
    for i in range(10):
        prob = botStateProbability(states[newState])
        print(prob)
        newState = selectPosition(prob)
main()