import ghmm
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
UP_RIGHT = 4
UP_LEFT = 5
DOWN_RIGHT = 6
DOWN_LEFT = 7
GESTES_COUNT = 4
OBSERVATIONS_COUNT = 8
 
gestures = [
    ([UP, RIGHT], ['/usr/bin/xdotool', 'getactivewindow', 'windowkill']),
    ([UP, LEFT], ['notify-send', '"received command"', '"Hooray!"']),
    ([DOWN], ['amixer', 'set', 'Master', '10%-']),
    ([UP], ['amixer', 'set', 'Master', '10%+']),
]
 
 
def initial_vector(gesture):
    vec = [0 for i in range(GESTES_COUNT)]
    # Take the beginning of the gesture and set probability to 1
    vec[gesture[0]] = 1
    return vec
 
def emission_matrix():
    B = [[float(1)/OBSERVATIONS_COUNT for i in range(OBSERVATIONS_COUNT)] for j in range(GESTES_COUNT)]
 
    B[UP] = [0.37, 0.04, 0.08, 0.08, 0.165, 0.165, 0.05, 0.05]
    B[DOWN] = [0.04, 0.37, 0.08, 0.08, 0.05, 0.05, 0.165, 0.165]
    B[LEFT] = [0.08, 0.08, 0.37, 0.04, 0.05, 0.165, 0.05, 0.165]
    B[RIGHT] = [0.08, 0.08, 0.04, 0.37, 0.165, 0.05, 0.165, 0.05]
    return B
 
def normalize_rows(matrix):
    new_matrix = []
 
    for row in matrix:
        div = sum(row)
        new_matrix.append([])
 
        for elem in row:
            if div != 0:
                new_matrix[-1].append(float(elem)/div)
            else:
                new_matrix[-1].append(elem)
 
    return new_matrix
 
def transition_matrix(gesture):
    A = [[0 for i in range(GESTES_COUNT)] for j in range(GESTES_COUNT)]
    # self transitions are high
    for geste in gesture:
        A[geste][geste] = 0.7
 
    first = gesture[0]
 
    for second in gesture[1:]:
        # if we have a transition, prob must be high
        A[first][second] = 0.4
        first = second
 
    # ending element has no transitions anymore, so give it one
    A[gesture[-1]][gesture[-1]] = 1
 
    return normalize_rows(A)
 
 
models = []
 
sigma = ghmm.IntegerRange(0, 8)
B = emission_matrix()
for gesture in gestures:
    A = transition_matrix(gesture[0])
    pi = initial_vector(gesture[0])
 
    m = ghmm.HMMFromMatrices(sigma, ghmm.DiscreteDistribution(sigma), A, B, pi)
    models.append((m, gesture[1]))