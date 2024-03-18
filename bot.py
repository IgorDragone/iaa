import pysmile
import pysmile_license
import random


states = ["Atacar", "recoger_arma", "recoger_energ_a", "explorar", "huir",  "detectar_peligro" ]

def botStateProbability(stValue = "Atacar" ):
    net = pysmile.Network()
    net.read_file("BotIaa.xdsl")
    st = stValue
    h = "si"
    w = "si"
    ow = "si"
    hn = "si"
    ne = "si"
    pw = "si"
    ph = "si"
    evidence = { "Estado_Actual": st,  "H": h, "Copy_2_of_H": w, "Copy_5_of_H": ow, "Copy_of_H": hn, "Copy_3_of_H": ne, "Copy_4_of_H": pw, "Copy_6_of_H": ph }
    for node_name, value in evidence.items():
        net.set_evidence(node_name, value)
    net.update_beliefs()
    return net.get_node_value("Copy_of_Estado_Actual")

def selectPosition(probabilities):
  indexes = list(range(len(probabilities)))
  return random.choices(indexes, weights=probabilities, k=1)[0]

if __name__ == "__main__":
    print("Bot's probability at t+1 is:")
    print(states)
    prob = botStateProbability()
    newState = selectPosition(prob)
    for i in range(10):
        prob = botStateProbability(states[newState])
        newState = selectPosition(prob)