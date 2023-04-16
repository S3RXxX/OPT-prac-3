import itertools
import copy


class Automata:
    def __init__(self):

        # 1 negre / 0 blanc
        # crear noves regles

        self.__size = int(input('Select matrix size:\n'))
        self.__m = int(input('Select m (number of layers):\n'))
        self.__n = int(input('Select n (number of dimensions of each layer):\n'))
        self.__k = int(input('Select k (number of main layers):\n'))
        if self.__m < self.__k:
            raise Exception('NO pot haver més capes principals que capes')
        self.__layers = self.__create_layers()

        self.__r_evo = [{(1, 1, 1): 0, (1, 1, 0): 0, (1, 0, 1): 0, (1, 0, 0): 1, (0, 1, 1): 1, (0, 1, 0): 1,
                         (0, 0, 1): 1, (0, 0, 0): 0} for _ in range(self.__k)]
        self.__r_evo = [{(1, 1, 1): 0, (1, 1, 0): 1, (1, 0, 1): 0, (1, 0, 0): 1, (0, 1, 1): 1, (0, 1, 0): 1,
                         (0, 0, 1): 1, (0, 0, 0): 0} for _ in range(self.__k)]
        self.__r_evo = [{(1, 1, 1): 0, (1, 1, 0): 0, (1, 0, 1): 1, (1, 0, 0): 1, (0, 1, 1): 0, (0, 1, 0): 1,
                         (0, 0, 1): 1, (0, 0, 0): 0} for _ in range(self.__k)]
        self.__r_evo = [{(1, 1, 1): 0, (1, 1, 0): 1, (1, 0, 1): 0, (1, 0, 0): 1, (0, 1, 1): 1, (0, 1, 0): 0,
                         (0, 0, 1): 1, (0, 0, 0): 0} for _ in range(self.__k)]



        # radi pel veinatge
        # self.__r = int(input('Select radi veinatge:\n'))

    def __create_matrix(self):
        # canviar a llegir inputs de les dades que es tinguin que posar en layers
        mtx = [0 for _ in range(self.__size)]
        mid = self.__size//2
        mtx[mid] = 1

        def __aux(mtx, n, size):
            if n == 0:
                return mtx
            else:
                mtx = [copy.deepcopy(mtx) for _ in range(size)]
                return __aux(mtx, n - 1, size)

        return __aux(mtx, self.__n-1, self.__size)

    def __create_layers(self):
        layers = [0 for _ in range(self.__m)]
        for i in range(self.__m):
            mtx = self.__create_matrix()
            # en cas de que hi hagi class Layer
            # v = Layer(self.__n, self.__rule[i], self.__size)
            layers[i] = mtx
        return layers

    def __get_element(self, arr, indices):
        # tret de chatGPT
        if indices[0] < 0 or indices[0] >= self.__size:
            return 0

        elif len(indices) == 1:
            return arr[indices[0]]
        else:
            return self.__get_element(arr[indices[0]], indices[1:])

    def __set_element(self, arr, indices, value):
        if len(indices) == 1:
            arr[indices[0]] = value
        else:
            self.__set_element(arr[indices[0]], indices[1:], value)

    def __em(self, m, idx):
        # idx es les coordenades de la posicio
        return self.__get_element(self.__layers[m], idx)

    def __funcio_combinacio(self, states):
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
        nucli = set()
        nucli.add(tuple(idx))
        return nucli

    def __veins(self, coords):
        # fet amb chatGPT despres versionat
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

        new_state = self.__r_evo[m][veins_state]
        for ncl in nucli:
            self.__set_element(self.__new_layers[m], ncl, new_state)


    def execute(self):
        iteration = 0
        self.__mostra()
        while iteration < 256:
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
        # fer un diccionari num --> caracters per si no es binari
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
