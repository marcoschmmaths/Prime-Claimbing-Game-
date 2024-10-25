from game import Game, choice, OPERATIONS, Player
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import json


"""posibles mejoras:
    1- evitar que 2 piezas del mismo jugador se coman entre si (se deben usar 
  bloques try xq frecuentemente se presenta que la unica jugada de ciertas listas
  es la que se come al otro peon)
    2- comerse al contrario 
    3- niveles de dificultad  y juego contra la computadora desde la consola 
    4- interfaz con pygame(creo)"""

with open('probabilidad.json','r') as f:
    lista_de_probabilidades = json.load(f)



lista_de_posiciones=[]
lista_de_op = []
diccionario_de_jugadas = {'+':0,'-':0,'*':0,'/':0}

dice = Game.roll_dice()
operations = ['+', '-', '*', '/']

def operacion(a: int, b: int, op: str) -> int:
    if op == '+' and a+b <= 101 and a+b >= 0:
        return a+b
    elif op == '-' and a-b <= 101 and a-b >= 0:
        return a-b
    elif op == '*' and a*b <= 101 and a*b >= 0:
        return a*b
    elif op == '/' and a/b <= 101 and a/b >= 0 and int(a/b) == a/b:
        return int(a/b)

def jugadas(posicion: int, dice: list) -> list:
    """true en la posicion 2 significa que el primer dado que se uso es el 1, false que se uso el 0 """
    list_j_d0 = [(operacion(posicion, dice[0], op), False, op)
                 for op in operations if operacion(posicion, dice[0], op) != None]
    list_j_d1 = [(operacion(posicion, dice[1], op), True, op)
                 for op in operations if operacion(posicion, dice[1], op) != None]

    list_aux0 = deepcopy(list_j_d0)
    list_aux1 = deepcopy(list_j_d1)

    list_j_d0 = list_j_d0 + [(operacion(new[0], dice[1], op), False, new[2], op)
                             for new in list_aux0 for op in operations if operacion(new[0], dice[1], op) != None]

    list_j_d1 = list_j_d1 + [(operacion(new[0], dice[0], op), True, new[2], op)
                             for new in list_aux1 for op in operations if operacion(new[0], dice[0], op) != None]

    return list_j_d0 + list_j_d1

def dobles(posicion: int, dice: list) -> list:
    list_j = [(operacion(posicion, dice[0], op), op)
              for op in operations if operacion(posicion, dice[0], op) != None]
    list_aux1 = deepcopy(list_j)

    list_j = list_j + [(operacion(new[0], dice[1], op), new[1], op)
                       for new in list_aux1 for op in operations if operacion(new[0], dice[1], op) != None]

    list_aux2 = deepcopy(list_j)
    list_j = list_j + [(operacion(new[0], dice[2], op), new[1], op)
                       for new in list_aux2 for op in operations if operacion(new[0], dice[2], op) != None and len(new) == 2]

    list_j = list_j + [(operacion(new[0], dice[2], op), new[1], new[2], op)
                       for new in list_aux2 for op in operations if operacion(new[0], dice[0], op) != None and len(new) == 3]

    list_aux3 = deepcopy(list_j)

    list_j = list_j + [(operacion(new[0], dice[2], op), new[1], op)
                       for new in list_aux3 for op in operations if operacion(new[0], dice[2], op) != None and len(new) == 2]

    list_j = list_j + [(operacion(new[0], dice[2], op), new[1], new[2], op)
                       for new in list_aux3 for op in operations if operacion(new[0], dice[2], op) != None and len(new) == 3]

    list_j = list_j + [(operacion(new[0], dice[2], op), new[1], new[2], new[3], op)
                       for new in list_aux3 for op in operations if operacion(new[0], dice[2], op) != None and len(new) == 4]
    return list_j

def probabilidades(x) -> dict:
    """x = distancia al objetivo
    ahora solo hace las operaciones simples, agregar los resultados de las dobles"""
    
    di = lista_de_probabilidades[x]
    return di

def objetivo(player_id):
    if game.current_player.f1.stops < 2 and game.current_player.f2.stops < 2:
        return [31, 37, 41, 43, 47, 53, 57, 61, 67, 71, 73, 79], [31, 37, 41, 43, 47, 53, 57, 61, 67, 71, 73, 79]
    elif game.current_player.f1.stops >= 2 and game.current_player.f2.stops < 2:
        return [101], [31, 37, 41, 43, 47, 53, 57, 61, 67, 71, 73, 79]
    elif game.current_player.f1.stops < 2 and game.current_player.f2.stops >= 2:
        return [31, 37, 41, 43, 47, 53, 57, 61, 67, 71, 73, 79], [101]
    elif game.current_player.f1.stops >= 2 and game.current_player.f2.stops >= 2:
        return [101], [101]

def suma_de_probabilidades(obj: list, jugadas: list) -> list:
    
    #suma de probabilidad para dependencia de la posicion 
    suma_prob = []
    for i in jugadas:
        suma = 0
        probabilidad = probabilidades(i[0])
        for j in obj:
            for k in probabilidad.items():
                if j == int(k[0]):
                    suma = suma + k[1]
        suma_prob.append(suma)
    return suma_prob
   
def metrica_segun_ob(jugadas_posibles, objetiv):
    prob_x_jugada = dict()

    if dice[0] != dice[1]:
        suma_prob = suma_de_probabilidades(objetiv, jugadas_posibles)

        for i in range(len(suma_prob)):
            if suma_prob[i] in prob_x_jugada:
                prob_x_jugada[suma_prob[i]].append(jugadas_posibles[i])
            else:
                prob_x_jugada[suma_prob[i]] = [jugadas_posibles[i]]
        return prob_x_jugada

    else:
        suma_prob = suma_de_probabilidades(objetiv, jugadas_posibles)

        for i in range(len(suma_prob)):
            if suma_prob[i] in prob_x_jugada:
                prob_x_jugada[suma_prob[i]].append(jugadas_posibles[i])
            else:
                prob_x_jugada[suma_prob[i]] = [jugadas_posibles[i]]
        return prob_x_jugada

def complementarias_simples(jugada,lista_de_jugadas):
    """sea jugada = (pos,True,op) el conjunto de complementarias de esta jugada
    son las jugadas de la forma (pos,False,op) donde op son operaciones definidas cualesquiera,
    se exige que la jugada complementaria lleve a la otra ficha a una posicion distitna 
    a la que lleva a la primera la otra,sino acabaran comiendose entre ellas """
    if len(jugada)==4:
        return None 
    else:
        return [t for t in lista_de_jugadas if len(t)==3 and int(jugada[1])==int(not t[1]) ]

def complementarias_dobles(jugada,lista_de_jugadas):
    """la misma idea pero con dobles, no tengo ganas de definirlo"""
    return [t for t in lista_de_jugadas if len(t)+len(jugada)==6 ]

def mayor_coincidencia(coincidencia:list)->tuple:
    """esta funcion puede ser sustituida por otras abstracciones mas complejas de 
    la idea de mejor jugada; ya sea tomar coincidencias que posibiliten el logro 
    mas consecuente de los objetivos de alguna forma o algo asi en funcion de cuantos 
    primos falten por lograr ect"""
    mayor = [0]
    for i in coincidencia:
        if mayor[0]<i[0]:
            mayor = i
    return mayor


def decide(player_id: int, board: list, dice: list):
    objetiv = objetivo(game.current_player.id)
    if dice[0] != dice[1]:
        jugadas_posibles_F1 = jugadas(game.current_player.f1.loc, dice)
        jugadas_posibles_F2 = jugadas(game.current_player.f2.loc, dice)

        if game.current_player.f1.loc == 101:
            print('f1 gano')
            print('stops=',game.current_player.f2.stops)
            jugadas_posibles = [i for i in jugadas_posibles_F2 if len(i) == 4]
            if game.current_player.f2.stops<2:
                jugadas_posibles = [i for i in jugadas_posibles if i[0]!=101]
            coincidencias = [i for i in jugadas_posibles if objetiv[1]==i[0] and i[0]!=game.current_player.f2.loc]
            if len(coincidencias) !=0:
                mayor = mayor_coincidencia(coincidencias)
                return None,mayor
            else:
                pesos = metrica_segun_ob(jugadas_posibles, objetiv[1])
                maxi = max(pesos.keys())
                return None,pesos[maxi][0]
        if game.current_player.f2.loc == 101:
            print('f2 gano')
            jugadas_posibles = [i for i in jugadas_posibles_F1 if len(i) == 4]
            if game.current_player.f1.stops<2:
                jugadas_posibles = [i for i in jugadas_posibles if i[0]!=101]
            coincidencias = [i for i in jugadas_posibles if objetiv[0]==i[0] and game.current_player.f1.loc !=i[0]]
            if len(coincidencias) !=0:
                mayor = mayor_coincidencia(coincidencias)
                return mayor,None
            else:
                pesos = metrica_segun_ob(jugadas_posibles, objetiv[0])
                maxi = max(pesos.keys())
                return pesos[maxi][0],None
        
        coincidenciasF1 = [i for i in jugadas_posibles_F1 for j in objetiv[0] if i[0] == j ]
        coincidenciasF2 = [i for i in jugadas_posibles_F2 for j in objetiv[1] if i[0] == j ]

        coincidencias_simplesF1 = [i for i in coincidenciasF1 if len(i) == 3]
        coincidencias_simplesF2 = [i for i in coincidenciasF2 if len(i) == 3]

        Pesos_jugadasF1 = metrica_segun_ob(jugadas_posibles_F1, objetiv[0])
        Pesos_jugadasF2 = metrica_segun_ob(jugadas_posibles_F2, objetiv[1])
        if len(coincidencias_simplesF1) > 0 and len(coincidencias_simplesF2) > 0:
            #print('coincidencias simplesf1>0 and coincidencias simples f2>0')
            #se chequea la existencia de objetivos complementarios
            for i in coincidencias_simplesF1:
                for j in coincidencias_simplesF2:
                    if int(i[1]) == int(not j[1]):
                        return i, j
            #si no hay objetivos complementarios pasamos a buscar la mayor entre todas las coincidencias 
            maxi1 = mayor_coincidencia(coincidencias_simplesF1)
            maxi2 = mayor_coincidencia(coincidencias_simplesF2)
            #dada la mayor coincidencia se retorna la jugada mas beneficiosa con la otra ficha
            if maxi1>=maxi2:
                complementariasF2 = complementarias_simples(maxi1, jugadas_posibles_F2)
                
                pesos_complementariasF2 = metrica_segun_ob(complementariasF2, objetiv[1])
                maximo = max(pesos_complementariasF2.keys())
                return maxi1, pesos_complementariasF2[maximo][0]
            else:
                complementariasF1 = complementarias_simples(maxi2, jugadas_posibles_F1)
                pesos_complementariasF1 = metrica_segun_ob(complementariasF1, objetiv[0])
                maximo = max(pesos_complementariasF1.keys())
                return pesos_complementariasF1[maximo][0],maxi2
    
        if len(coincidencias_simplesF1) > 0 and len(coincidencias_simplesF2) == 0:
            #print('coincidencias simplesf1>0 and coincidencias simples f2=0')
            maxi1 = mayor_coincidencia(coincidencias_simplesF1)
            complementariasF2 = complementarias_simples(maxi1, jugadas_posibles_F2)
            pesos_complementariasF2 = metrica_segun_ob(complementariasF2, objetiv[1])
            maximo = max(pesos_complementariasF2.keys())
            return maxi1, pesos_complementariasF2[maximo][0]

        if len(coincidencias_simplesF1) == 0 and len(coincidencias_simplesF2) > 0:
            #print('coincidencias simplesf1=0 and coincidencias simples f2>0')
            maxi2 = mayor_coincidencia(coincidencias_simplesF2)
            complementariasF1 = complementarias_simples(maxi2, jugadas_posibles_F1)
            pesos_complementariasF1 = metrica_segun_ob(complementariasF1, objetiv[0])
            maximo = max(pesos_complementariasF1.keys())
            return pesos_complementariasF1[maximo][0], maxi2

        if len(coincidenciasF1) > 0:
            maxi1 = mayor_coincidencia(coincidenciasF1)
            if maxi1[0]!=game.current_player.f2.loc:
                return maxi1, None
            elif maxi1[0]==game.current_player.f2.loc and len(coincidenciasF1)>1:
                coincidenciasF1.remove(maxi1)
                maxi1 = mayor_coincidencia(coincidenciasF1)
                return maxi1, None

        if len(coincidenciasF2) > 0:
            maxi2 = mayor_coincidencia(coincidenciasF2)
            if maxi2[0]!=game.current_player.f1.loc:
                return None, maxi2
            elif maxi2[0]== game.current_player.f1.loc and len(coincidenciasF2)>1:
                coincidenciasF2.remove(maxi2)
                maxi2 = mayor_coincidencia(coincidenciasF2)
                return None,maxi2
            
        #print('no hubieron coincidencias')
        MaximoF1 = max(Pesos_jugadasF1)
        MaximoF2 = max(Pesos_jugadasF2)
        if MaximoF1 >= MaximoF2:
            con_2_dados = [i for i in Pesos_jugadasF1[MaximoF1] if len(i)==4]
            simples = [i for i in Pesos_jugadasF1[MaximoF1] if len(i)==3]
            
            if len(simples)!=0:
                Comp_simples = complementarias_simples(simples[0], Pesos_jugadasF1[MaximoF1])
                complementariasF2_simples = complementarias_simples(simples[0], jugadas_posibles_F2)
                if len(complementariasF2_simples)>0:
                    pesos_complementariasF2_simples = metrica_segun_ob(complementariasF2_simples, objetiv[1])
                    try:
                        maximo_simples = max(pesos_complementariasF2_simples.keys())
                    except:
                        return con_2_dados[0],None
                if len(Comp_simples)!=0:
                    complementariasF2_Comp = complementarias_simples(Comp_simples[0], jugadas_posibles_F2)
                    pesos_complementariasF2_Comp = metrica_segun_ob(complementariasF2_Comp, objetiv[1])
                    try:
                        maximo_Comp = max(pesos_complementariasF2_Comp.keys())
                    except:
                        return con_2_dados[0],None
    
                    if maximo_simples>=maximo_Comp:
                        return simples[0],pesos_complementariasF2_simples[maximo_simples][0]
                    else:
                        return Comp_simples[0],pesos_complementariasF2_Comp[maximo_Comp][0]
                return simples[0],pesos_complementariasF2_simples[maximo_simples][0]
                
            else:
                return con_2_dados[0], None
        elif MaximoF2 > MaximoF1:
            con_2_dados = [i for i in Pesos_jugadasF2[MaximoF2] if len(i)==4]
            simples = [i for i in Pesos_jugadasF2[MaximoF2] if len(i)==3]
                
            if len(simples)!=0:
                Comp_simples = complementarias_simples(simples[0], Pesos_jugadasF2[MaximoF2])
                    
                complementariasF1_simples = complementarias_simples(simples[0], jugadas_posibles_F1)
                pesos_complementariasF1_simples = metrica_segun_ob(complementariasF1_simples, objetiv[0])
                try:
                    maximo_simples = max(pesos_complementariasF1_simples.keys())
                except:
                    return None,con_2_dados[0]
                if len(Comp_simples)!=0:
                    complementariasF1_Comp = complementarias_simples(Comp_simples[0], jugadas_posibles_F1)
                    pesos_complementariasF1_Comp = metrica_segun_ob(complementariasF1_Comp, objetiv[0])
                    try:
                        maximo_Comp = max(pesos_complementariasF1_Comp.keys())
                    except:
                        return None,con_2_dados[0]
                    if maximo_simples>=maximo_Comp:
                        return pesos_complementariasF1_simples[maximo_simples][0],simples[0]
                    else:
                        return pesos_complementariasF1_Comp[maximo_Comp][0],Comp_simples[0]
                return pesos_complementariasF1_simples[maximo_simples][0],simples[0]
            else:
                return  None,con_2_dados[0]
                
    elif dice[0]==dice[1]:
        # hay coincidencias simples
        jugadas_posibles_F1 = dobles(game.current_player.f1.loc, dice)
        jugadas_posibles_F2 = dobles(game.current_player.f2.loc, dice)
                
        if game.current_player.f1.loc == 101:
            jugadas_posibles = [i for i in jugadas_posibles_F2 if len(i) == 5]
            if len(objetiv[1])==12:
                jugadas_posibles = [i for i in jugadas_posibles if i[0]!=101]
            coincidencias = [i for i in jugadas_posibles if objetiv[1]==i[0] and game.current_player.f2.loc!= i[0]]
            if len(coincidencias) !=0:
                return None,coincidencias[0]
            else:
                pesos = metrica_segun_ob(jugadas_posibles, objetiv[1])
                maxi = max(pesos.keys())
                return None,pesos[maxi][0]
        if game.current_player.f2.loc == 101:
            jugadas_posibles = [i for i in jugadas_posibles_F1 if len(i) == 5]
            if len(objetiv[0])==12:
                jugadas_posibles = [i for i in jugadas_posibles if i[0]!=101 and game.current_player.f2.loc!= i[0]]
            coincidencias = [i for i in jugadas_posibles if objetiv[0]==i[0]]
            if len(coincidencias) !=0:
                return coincidencias[0],None
            else:
                pesos = metrica_segun_ob(jugadas_posibles, objetiv[1])
                maxi = max(pesos.keys())
                return pesos[maxi][0],None
        
        coincidenciasF1 = [i for i in jugadas_posibles_F1 for j in objetiv[0] if i[0] == j and game.current_player.f1.loc!= i[0]]
        coincidenciasF2 = [i for i in jugadas_posibles_F2 for j in objetiv[1] if i[0] == j and game.current_player.f2.loc!= i[0]]

        # hay coincidencias con alguna de las 2 fichas
        if len(coincidenciasF1)>0:
            for i in coincidenciasF1:
                if len(coincidenciasF2) == 0:
                    complementariasF2 = complementarias_dobles(i, jugadas_posibles_F2)  
                    if len(complementariasF2) == 0:
                        return i, None
                    else:
                        pesos_complementariasF2 = metrica_segun_ob(complementariasF2, objetiv[1])
                        maxi = max(pesos_complementariasF2.keys())
                        return i, pesos_complementariasF2[maxi][0]
                else:
                    for j in coincidenciasF2:
                        if len(i)+len(j) == 6:
                            return i, j
                        else:
                            complementariasF2 = complementarias_dobles(i, jugadas_posibles_F2)  
                            if len(complementariasF2) == 0:
                                return i, None
                            pesos_complementariasF2 = metrica_segun_ob(complementariasF2, objetiv[1])
                            maxi = max(pesos_complementariasF2.keys())
                            return i, pesos_complementariasF2[maxi][0]

        if len (coincidenciasF2)>0:
            #cambiar la seleccion aqui aunq haga el codigo mas largo xq no esta pinchando
            for j in coincidenciasF2:
                if len(coincidenciasF1) == 0:
                    complementariasF1 = complementarias_dobles(j, jugadas_posibles_F1)  
                    if len(complementariasF1) == 0:
                        return None, j
                    pesos_complementariasF1 = metrica_segun_ob(complementariasF1, objetiv[1])
                    maxi = max(pesos_complementariasF1.keys())
                    return pesos_complementariasF1[maxi][0], j
                for i in coincidenciasF1:
                    if len(i)+len(j) == 6:
                        return i, j
                    else:
                        complementariasF1 = complementarias_dobles(j, jugadas_posibles_F1)  
                        pesos_complementariasF1 = metrica_segun_ob(complementariasF1, objetiv[0])
                        maxi = max(pesos_complementariasF1.keys())
                        return i, pesos_complementariasF1[maxi][0]
                    
        if len(coincidenciasF1) == 0 and len(coincidenciasF2) == 0:
            Pesos_jugadasF1 = metrica_segun_ob(jugadas_posibles_F1, objetiv[0])
            Pesos_jugadasF2 = metrica_segun_ob(jugadas_posibles_F2, objetiv[1])
            MaximoF1 = max(Pesos_jugadasF1.keys())
            MaximoF2 = max(Pesos_jugadasF2.keys())

            if MaximoF1 >= MaximoF2:
                # hacer que tome la jugada con len() mas bajo
                complementariasF2 = complementarias_dobles(Pesos_jugadasF1[MaximoF1][0], jugadas_posibles_F2)  
                if len(complementariasF2) == 0:
                    return Pesos_jugadasF1[MaximoF1][0], None
                else:
                    pesos_complementariasF2 = metrica_segun_ob(complementariasF2, objetiv[1])
                    maxi = max(pesos_complementariasF2.keys())
                    return Pesos_jugadasF1[MaximoF1][0], pesos_complementariasF2[maxi][0]
            elif MaximoF2>MaximoF1:
                complementariasF1 = complementarias_dobles(Pesos_jugadasF2[MaximoF2][0], jugadas_posibles_F1)  
                if len(complementariasF1) == 0:
                    return None, Pesos_jugadasF2[MaximoF2][0]
                else:
                    pesos_complementariasF1 = metrica_segun_ob( complementariasF1, objetiv[0])
                    maxi = max(pesos_complementariasF1.keys())
                    return pesos_complementariasF1[maxi][0], Pesos_jugadasF2[MaximoF2][0]
             
def my_move(player_id: int, board: list, dice: list):
    loot = decide(player_id, board, dice)
    lista_de_op.append(loot)
    #print(loot)
    lista_de_posiciones.append((board[0][0],board[0][1]))
    for i in loot:
        if i!=None:
            for j in i:
                for op in operations:
                    if op == j:
                        diccionario_de_jugadas[op]+=1
    if dice[0]!=dice[1]:
        if loot[0] != None and loot[1] != None and len(loot[0]) == 3:
            return [(int(loot[0][1]), loot[0][2])], [(int(not loot[0][1]), loot[1][2])]
        if loot[0] != None and len(loot[0]) == 4:
            return [(int(loot[0][1]), loot[0][2]), (int(not loot[0][1]), loot[0][3])], [None]
        if loot[1] != None and len(loot[1]) == 4:
            return [None], [(int(loot[1][1]), loot[1][2]), (int(not loot[1][1]), loot[1][3])]

    if dice[0]==dice[1]:
        if loot[0] == None and loot[1] != None:
            return [None], [(0, loot[1][1]), (1, loot[1][2]), (2, loot[1][3]), (3, loot[1][4])]
        elif loot[0] != None and loot[1] == None:
            return [(0, loot[0][1]), (1, loot[0][2]), (2, loot[0][3]), (3, loot[0][4])], [None]
        elif len(loot[0]) == 2:
            return [(0, loot[0][1])], [(1, loot[1][1]), (2, loot[1][2]), (3, loot[1][3])]
        elif len(loot[0]) == 3:
            return [(0, loot[0][1]), (1, loot[0][2])], [(2, loot[1][1]), (3, loot[1][2])]
        elif len(loot[0]) == 4:
            return [(0, loot[0][1]), (1, loot[0][2]), (2, loot[0][3])], [(3, loot[1][1])]
turnos_finales = []


def Jugar(player_id: int, board: list, dice: list):
    """hay que explicar los comandos para cada jugada xd"""
    print("turno del jugador ", player_id)
    print("Las posiciones en el tablero son",  board)
    print("los dados son ", dice)
    print("paradas",game.current_player.f1.stops,game.current_player.f2.stops)
    while True:
        jugada_peon1 = input("entre la jugada para el peon 1 ")
        jugada_peon2 = input("entre la jugada para el peon 2 ")
        if dice[0]!=dice[1]:
            
            if len(jugada_peon1)==2 and len(jugada_peon2)==2:
                jugada = [(int(jugada_peon1[0]),jugada_peon1[1])],[(int(jugada_peon2[0]),jugada_peon2[1])]
            if jugada_peon1=='':
                jugada = [None],[(int(jugada_peon2[0]),jugada_peon2[1]),(int(not( bool(jugada_peon2[0]))),jugada_peon2[2])]
            if len(jugada_peon2)==2:
                jugada = [None],[(int(jugada_peon2[0]),jugada_peon2[1]),(int(not( bool(jugada_peon2[0]))),jugada_peon2[2])]
            if jugada_peon2 == '':
                print(int(jugada_peon1[0]))
                print(int(bool(jugada_peon1[0])))
                jugada = [(int(jugada_peon1[0]),jugada_peon1[1]),(int(not (bool(jugada_peon1[0]))),jugada_peon1[2])],[None]
            if len(jugada_peon1 )== 2:
                jugada = [(int(jugada_peon1[0]),jugada_peon1[1]),(int(not (bool(jugada_peon1[0]))),jugada_peon1[2])],[None]
        if dice[0]==dice[1]:
            if len(jugada_peon1)==0:
                jugada = [None], [(0, jugada_peon2[0]), (1, jugada_peon2[1]), (2, jugada_peon2[2]), (3, jugada_peon2[3])]
            if len(jugada_peon1)==1:
                jugada = [(0, jugada_peon1[0])], [(0, jugada_peon2[0]), (1, jugada_peon2[1]), (2, jugada_peon2[2])]
            if len(jugada_peon1)==2:
                jugada = [(0, jugada_peon1[0]),(1, jugada_peon1[1])], [(0, jugada_peon2[0]), (1, jugada_peon2[1])]
            if len(jugada_peon1)==3:
                jugada = [(0, jugada_peon1[0]),(1, jugada_peon1[1]),(1, jugada_peon1[2])], [(0, jugada_peon2[0])]
            if len(jugada_peon1)==4:
                jugada =  [(0, jugada_peon1[0]), (1, jugada_peon1[1]), (2, jugada_peon1[2]), (3, jugada_peon1[3])],[None]
        print('jugada= ',jugada)
        try:
            if Game.check_move(game, dice, jugada)!=True:
                continue
            return jugada
        except:
            continue


"""Comentado para llamarlo desde pygame_file"""
game = Game(players=2)
game.players[0].move = my_move
game.players[1].move = Jugar
game.play()

turnos_finales.append(game.turn)
print(sum(turnos_finales)/10000)
print(min(turnos_finales))
print(max(turnos_finales))

#print(lugares)

def histograma(lista_de_posiciones):
    posiciones = [0 for i in range(102)]
    for i in lista_de_posiciones:
        for j in i:
            posiciones[j]+=1
    plt.bar(range(102),posiciones)
    plt.xlabel('Casillas')
    plt.ylabel('Ocupación')
    plt.title('Histograma de Ocupación de Casillas')
    plt.show()
#histograma(lista_de_posiciones)
def graficas_peones(lista_de_posiciones):
    lugares = {}
    c=0
    for i in lista_de_posiciones:
        if i == (0,0):
            c=c+1
        if c not in lugares:
            lugares[c]=[i]
        else:
            lugares[c].append(i)
    for i in lugares.keys():
        lugares[i].append((101,101))
        
    minimo = [i for i in range(100) ]
    for i in lugares.keys():
        if len(lugares[i])<len(minimo):
            minimo =lugares[i]
    
    maximo = [ ]
    for i in lugares.keys():
        if len(lugares[i])>len(maximo):
            maximo =lugares[i]
    
    
    
    fig, ax = plt.subplots(2,2, figsize = (10,8))
    plt.suptitle('mejor y peor partida')
    
    #grafico minimo peon 1 
    x1 = list(np.arange(len(minimo)))
    y1 = [i[0] for i in minimo]
    ax[0,0].plot(x1, y1, color = 'g', label= "Peon 1 de la secuencia min", marker = ".")
    ax[0,0].legend()
    ax[0,0].grid()
    ax[0,0].set_ylabel('Posiciones')
    
    #grafico maximo peon 1 
    x2 = list(np.arange(len(maximo)))
    y2 = [i[0] for i in maximo]
    ax[0,1].plot(x2, y2, color = 'r', label= "Peon 1 de la secuencia max", marker = ".")
    ax[0,1].legend()
    ax[0,1].grid()
    ax[0,1].set_ylabel('Posiciones')
    
    #grafico minimo peon 2
    x3 = list(np.arange(len(minimo)))
    y3 = [i[1] for i in minimo]
    ax[1,0].plot(x3, y3, color = 'g', label= "Peon 2 de la secuencia min", marker = ".")
    ax[1,0].legend()
    ax[1,0].grid()
    ax[1,0].set_ylabel('Posiciones')

    #grafico maximo peon 2
    x4 = list(np.arange(len(maximo)))
    y4 = [i[1] for i in maximo]
    ax[1,1].plot(x4, y4, color = 'r', label= "Peon 2 de la secuencia max", marker = ".")
    ax[1,1].legend()
    ax[1,1].grid()
    ax[1,1].set_ylabel('Posiciones')

    
    
def lista_de_operaciones(lista_de_op,lista_de_posiciones):
    lugares = {}
    operaciones = {}
    diccionario_max = {'+':0,'-':0,'*':0,'/':0}
    diccionario_min = {'+':0,'-':0,'*':0,'/':0}

    c=0
    for i in lista_de_posiciones:
        if i == (0,0):
            c=c+1
        if c not in lugares:
            lugares[c]=[i]
        else:
            lugares[c].append(i)
    for i in lugares.keys():
        lugares[i].append((101,101))
        
        
        
    for i in lugares.keys():
        if i == max(lugares.keys()):
            operaciones[i]= [lista_de_op[t] for t in range(len(lista_de_op)) if sum([len(lugares[j])-1 for j in lugares if j<i])<t]
        else:
            operaciones[i]=[lista_de_op[t] for t in range(len(lista_de_op)) if sum([len(lugares[j])-1 for j in lugares if j<i] )<t<sum([len(lugares[j])-1 for j in lugares if j<i+1] )]
    minimo = [i for i in range(1000) ]
        
    for i in operaciones.keys():
        if len(operaciones[i])<len(minimo):
            minimo =operaciones[i]
    maximo = [ ]
    for i in operaciones.keys():
        if len(operaciones[i])>len(maximo):
            maximo =operaciones[i]
    

    for i in maximo:
        for y in i:
            if y!=None:
                for j in y:
                    for op in operations:
                        if op == j:
                            diccionario_max[op]+=1
    for i in minimo:
        for y in i:
            if y!=None:
                for j in y:
                    for op in operations:
                        if op == j:
                            diccionario_min[op]+=1
    return diccionario_min, diccionario_max
#print(lista_de_operaciones(lista_de_op, lista_de_posiciones))
#graficas_peones( lista_de_posiciones)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    