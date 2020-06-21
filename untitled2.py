from tkinter import *
from tkinter import messagebox
import random
import copy
import time

#    init:      goal:
#    7 2 4      0 1 2
#    5 0 6      3 4 5
#    8 3 1      6 7 8

_goal_state = '012345678'
_init_state = '724506831'


_neighbors = {0: [1,3],
              1: [0,2,4],
              2: [1,5],
              3: [0,4,6],
              4: [1,3,5,7],
              5: [2,4,8],
              6: [3,7],
              7: [4,6,8],
              8: [5,7]}


_distance = [[0,1,2,1,2,3,2,3,4],
             [1,0,1,2,1,2,3,2,3],
             [2,1,0,3,2,1,4,3,2],
             [1,2,3,0,1,2,1,2,3],
             [2,1,2,1,0,1,2,1,2],
             [3,2,1,2,1,0,3,2,1],
             [2,3,4,1,2,3,0,1,2],
             [3,2,3,2,1,2,1,0,1],
             [4,3,2,3,2,1,2,1,0]]


_algo = {1:"Breadth-First Search", 
         }

class EightPuzzle(object):

    def __init__(self, input_state=None):
        if input_state:
            self.state = copy.deepcopy(input_state)
        else:       
           
            self.state = copy.deepcopy(_goal_state)
            self.shuffle()
            
   
    def shuffle(self):
        pos0 = self.state.index('0')
        for i in range(100):
            choices = _neighbors[pos0]
            pos = choices[random.randint(0, len(choices)-1)]
            self.swap(pos)
            pos0 = self.state.index('0')

    def swap(self, pos):
        pos0 = self.state.index('0')
        l = list(self.state)
        l[pos0], l[pos] = l[pos], l[pos0]
        self.state = ''.join(l)

    
    def get_next(self, current):
        pos0 = current.index('0')
        nextStates = []

        for pos in _neighbors[pos0]:
            l = list(current)
            l[pos0], l[pos] = l[pos], l[pos0]
            step = ''.join(l)
            nextStates.append(step)
        return nextStates  

    def solve_by_BFS(self):

        root = self.state
        goal = '012345678'
        previous = {root: None}
        visited = {root: True}
        solved = (root == goal)
        q = [root]
        while q and not solved:
            current = q.pop(0)
            for next_node in self.get_next(current):
                if not next_node in visited:
                    visited[next_node] = True
                    previous[next_node] = current
                    q.append(next_node)
                if next_node == goal:
                    solved = True
                    break
        
       
        if solved:
            return self.retrieve_path(goal, previous), len(visited)
        return None, len(visited)


 
    
    def retrieve_path(self, goal, previous):
        path = [goal]
        current = goal
        while previous[current]:
            path.insert(0, previous[current])
            current = previous[current]
        return path


puzzle = EightPuzzle(_init_state)

def display():
    color = 'DeepPink' if puzzle.state != _goal_state else 'green'

    for i in range(9):
        if puzzle.state[i] != '0':
            var[i].set(str(puzzle.state[i]))
            label[i].config(bg=color)
        else:
            var[i].set('')
            label[i].config(bg='white')


def solve():
    for b in button:
        b.configure(state='disabled')
    option.configure(state='disabled')

    run = {1: puzzle.solve_by_BFS,
        
    }

    temp = select.get()
    index = 1
    for k,e in _algo.items():
        if e == temp:
            index = k
            break
    
    print('Solving...')
    
    
    stime = time.time()
    path, n = run[index]()
    ttime = time.time()

   
    if not path:    
        print('This 8-puzzle is unsolvable!')
        for i in range(9):
            label[i].config(bg='DeepPink' if puzzle.state[i] != '0' else 'white')
        for b in button:
            b.configure(state='normal')
        option.configure(state='normal')
        return

    info = 'Algorithm: '+_algo[index]+'\n' \
         + 'Time: '+str(round(ttime-stime, 6))+'s\n' \
         + 'States Explored: '+str(n)+'\n' \
         + 'Shortest Path: '+str(len(path)-1)+' steps.'
    print(info)
    display_procedure(path)    


def display_procedure(path):
    if not path:
        for b in button:
            b.configure(state='normal')
        option.configure(state='normal')
        return
    puzzle.state = path.pop(0)
    display()
    win.after(500, lambda: display_procedure(path)) 


def shuffle():
    puzzle.shuffle()
    display()


def reset():
    puzzle.state = copy.deepcopy(_init_state)
    display()


def move(event):
    text = event.widget.cget('text')
    if not text:
        return
    
    pos = puzzle.state.index(text)
    pos0 = puzzle.state.index('0')
    if _distance[pos0][pos] > 1:
        return

    puzzle.swap(pos)
    display()


win = Tk()
win.geometry('+300+100')
win.title('8-Puzzle')
algoFrame = Frame(win, width=260, relief=RAISED)
algoFrame.pack()
select = StringVar(algoFrame)
select.set(_algo[1]) 
option = OptionMenu(algoFrame, select, _algo[1])
option.pack()
board = Frame(win, width=260, height=260, relief=RAISED)
board.pack()
var = [StringVar() for i in range(9)]
label = [Label(board, textvariable=var[i], bg='gray', font=('Calibri', 48)) for i in range(9)]
for i in range(3):
    for j in range(3):
        label[i*3+j].bind("<Button-1>", lambda event: move(event))
        label[i*3+j].place(x=85*j+5,y=85*i+5, width=80, height=80)
        
buttonFrame = Frame(win, relief=RAISED, borderwidth=1)
buttonFrame.pack(fill=X, expand=True)
button = []
button.append(Button(buttonFrame, width='8', relief=RAISED, text="Reset", command=reset))
button.append(Button(buttonFrame, width='8', relief=RAISED, text="Random", command=shuffle))

button.append(Button(buttonFrame, width='8', relief=RAISED, text="Solve", command=solve)) 
for b in button:
    b.pack(side=LEFT, padx=6, pady=7)


def main():
    display()
    win.mainloop()

if __name__ == "__main__":
    main()
