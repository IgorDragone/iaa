import pysmile
import pysmile_license
import random

def selectPosition(probabilities):
    indexes = list(range(len(probabilities)))
    index = random.choices(indexes, weights=probabilities, k=1)[0]
    return index

def botStateProbability(stValue = "Atacar" ):
    # Cargar la red bayesiana desde un archivo
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

    evidence = {
        "Estado_Actual": st,
        "H": h,
        "Copy_2_of_H": w, # W
        "Copy_5_of_H": ow, # OW
        "Copy_of_H": hn, # HN
        "Copy_3_of_H": ne, # NE
        "Copy_4_of_H": pw, # PW
        "Copy_6_of_H": ph # PH
    }
    
    for node_name, value in evidence.items():
        net.set_evidence(node_name, value)
    net.update_beliefs()
    belief = net.get_node_value("Copy_of_Estado_Actual")
    print(belief)
    return belief


states = ["Atacar", "recoger_arma", "recoger_energ_a", "explorar", "huir",  "detectar_peligro" ]

if __name__ == "__main__":
    print("Bot's probability at t+1 is:")
    print("       Atacar       ", "     Recoger_arma        ", "    Recoger_energia     ", "      Explorar        ", "        Huir        ",  "   Detectar_peligro")
    prob = botStateProbability()
    newState = selectPosition(prob)
    for i in range(10):
        prob = botStateProbability(states[newState])
        newState = selectPosition(prob)