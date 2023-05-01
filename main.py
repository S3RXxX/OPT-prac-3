import itertools
import copy


########
# En cas que no es vegi tot per terminal es pot reduir self.__size
########
class Automata:

    def __init__(self):
        # 1 negre / 0 blanc
        # crear noves regles

        """Select number of iterations"""
        self.__max_iterations = 120

        """Select matrix size:"""
        # 270 fullscreen, 115 terminal default
        self.__size = 270

        """Select m (number of layers):"""
        self.__m = 1

        '''Select n (number of dimensions of each layer):'''
        self.__n = 1

        '''Select k (number of main layers):'''
        self.__k = 1

        if self.__m < self.__k:
            raise Exception('NO pot haver més capes principals que capes')
        self.__layers = self.__create_layers()
        self.__r_evo = self.__create_evolution_rule()

    def __create_wolfram_rule(self, rule_number):
        """a partir d un numero [0-255] crea la regla de Wolfram corresponent"""
        cap = [(1, 1, 1), (1, 1, 0), (1, 0, 1), (1, 0, 0), (0, 1, 1), (0, 1, 0),
               (0, 0, 1), (0, 0, 0)]

        bin_rule_number = bin(rule_number).replace("0b", "").zfill(8)
        __wolfram_rule = {cap[i]: int(bin_rule_number[i]) for i in range(8)}
        return __wolfram_rule

    def __create_evolution_rule(self):
        """les primeres capes son les principals, llavors la llista de regles d evolucio ha d estar en el mateix ordre que les capes i mateix nombre,
        la funcio es pot substituir per una mes complexa si necessari"""

        __w_r = self.__create_wolfram_rule(30)

        __r_evo = [__w_r for _ in range(self.__k)]

        return __r_evo

    def __create_matrix(self):
        """metode auxiliar per crear matrius (una capa) en cas que no hi hagi input d on llegir"""
        mtx = [0 for _ in range(self.__size)]
        mid = self.__size // 2
        mtx[mid] = 1

        def __aux(mtx, n, size):
            if n == 0:
                return mtx
            else:
                mtx = [copy.deepcopy(mtx) for _ in range(size)]
                return __aux(mtx, n - 1, size)

        return __aux(mtx, self.__n - 1, self.__size)

    def __create_layers(self):
        """actualment es creen, pero s haurien de llegir d un input"""
        layers = [0 for _ in range(self.__m)]
        for i in range(self.__m):
            mtx = self.__create_matrix()
            layers[i] = mtx
        return layers

    def __get_element(self, arr, indices):
        """com no sabem les dimensions hem d accedir recursivament
        esquema d aquest metode tret de chatGPT
        si es surt per dreta o esquerra retorna 0, per tant als bordes son 00_ i 0__ per esquerra i __0 i _00 per dreta on _ pot ser 1 o 0"""
        if indices[0] < 0 or indices[0] >= self.__size:
            return 0

        elif len(indices) == 1:
            return arr[indices[0]]
        else:
            return self.__get_element(arr[indices[0]], indices[1:])

    def __set_element(self, arr, indices, value):
        """com __get_element, pero ara serveix per canviar un valor"""
        if len(indices) == 1:
            arr[indices[0]] = value
        else:
            self.__set_element(arr[indices[0]], indices[1:], value)

    def __em(self, m, idx):
        # idx es les coordenades de la posicio
        return self.__get_element(self.__layers[m], idx)

    def __funcio_combinacio(self, states):
        """funcio actual es un or entre unes coordenades per cada capa, la funcio es pot substituir per una mes complexa si necessari"""
        state = states[0]
        for s in states[1:]:
            state = state or s
        return state

    def __eg(self, idx):
        # idx es les coordenades de la posicio
        states = []
        for m in range(self.__m):
            states.append(self.__em(m=m, idx=idx))
        state = self.__funcio_combinacio(states)
        return state

    def __nucli(self, idx):
        """encarregat de retornar el nucli"""
        nucli = set()
        nucli.add(tuple(idx))
        return nucli

    def __veins(self, coords):
        """ encarregat de retornar el veinatge (llista de tuples)
        fet amb chatGPT despres versionat"""

        neighbors = []

        # Loop over the possible offsets for the Moore neighbors in each dimension
        for offsets in itertools.product([-1, 0, 1], repeat=len(coords)):
            # Skip the offset that corresponds to the center cell (i.e., the cell itself)
            # if all(offset == 0 for offset in offsets):
            #   continue

            # Calculate the coordinates of the neighbor
            neighbor_coords = tuple(coord + offset for coord, offset in zip(coords, offsets))

            # Add the neighbor's coordinates to the list of neighbors
            neighbors.append(neighbor_coords)

        # Return the list of Moore neighbors
        return neighbors

    def __evolve(self, m, veins_state, nucli):
        """metode que aplica la funcio d evolucio corresponent donat l estat dels veins i el nucli"""

        new_state = self.__r_evo[m][veins_state]
        for ncl in nucli:
            self.__set_element(self.__new_layers[m], ncl, new_state)

    def execute(self):
        """metode principal"""
        iteration = 0
        self.__mostra()
        while iteration < self.__max_iterations:
            # input(iteration)
            # al girar els bucles estalviem calcular m-1 cops els veins i els seus estats
            # pero necessitem una copia de layers o passar la layer dins de __evolve
            self.__new_layers = copy.deepcopy(self.__layers)
            for coords in itertools.product([j for j in range(self.__size)], repeat=self.__n):
                veins = self.__veins(coords=coords)

                veins_state = []
                for v in veins:
                    state = self.__eg(v)
                    veins_state.append(state)

                veins_state = tuple(veins_state)
                nucli = self.__nucli(coords)
                for m in range(self.__k):
                    self.__evolve(m, veins_state=veins_state, nucli=nucli)
            self.__layers = self.__new_layers
            self.__mostra()
            iteration += 1

    def __mostra(self):
        """encarregat de mostrar per pantalla"""
        if self.__n == 1:
            for x1 in range(self.__size):
                state = self.__eg((x1,))
                if state == 0:
                    print(' ', end='')
                else:
                    print('o', end='')
            print("")
        else:
            ga = copy.deepcopy(self.__layers[0])
            for coords in itertools.product([j for j in range(self.__size)], repeat=self.__n):
                state = self.__eg(coords)
                self.__set_element(ga, coords, state)
            print(ga)


if __name__ == '__main__':
    aa = Automata()
    aa.execute()
