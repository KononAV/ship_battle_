from random import randint
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from functools import partial
from abc import abstractclassmethod


d = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5,
         'g' : 6, 'h' : 7, 'i' : 8, 'j' : 9, 'k' : 10, 'l' : 11,
         'm' : 12, 'n' : 13, 'o' : 14}


class Ship:
    __slots__ = '_length', '_tp', '_x', '_y', '_cells'



    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y

        self._cells = [1 for i in range(self._length)]


    def set_start_coords(self, x):


        try:

            if x and type(x) == str:
                x = x.split()

                x = [int(x[1]),d.get(x[0].lower()) ]

                if str(self.__class__) == '<class \'__main__.Pole\'>':
                    return x


            elif type(x)!=tuple:
                x = [None,None]


            self._x = x[0]

            self._y = x[1]

        except ValueError:


            self._x = None
            self._y = None
            showerror("type error", 'coords must be integers')




    def get_start_coords(self):
        return self._x, self._y

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):

        self._cells[key] = value




class Pole:
    __slots__ = '_size', '_ships', 'pc_ships', 'win', 'pc_xp', \
    'xp', 'pc_random', 'pole', 'pc_pole', 'attack_list', 'entry_true'


    def __init__(self, size=15):
        self._size = size
        self._ships = []
        self.pc_ships = []
        self.win = 0
        self.pc_xp = self.xp = 20
        self.pc_random = 0
        self.pole = [[0 for i in range(self._size)] for j in range(self._size)]
        self.pc_pole = [[0 for i in range(self._size)] for j in range(self._size)]
        self.attack_list = []

        self.entry_true = False



    def init(self):
        n = 4
        for i in range(1, 5):
            for j in range(1, i + 1):
                self._ships.append(Ship(n, tp=randint(1, 2)))
                self.pc_ships.append(Ship(n, tp=randint(1, 2)))
            n -= 1

    def get_ships(self):
        return self._ships



    def get_pole(self):
        self.entry_true = False
        self.pole = [[0 for j in i] for i in self.pole]

        try:

            for i in range(10):#################
                for x in range(len(self._ships[i]._cells)):


                    if self._ships[i]._tp == 1:
                        self.pole[self._ships[i]._x][self._ships[i]._y+x] += 1#self._ships[i]._cells[0]

                    else:
                        self.pole[self._ships[i]._x+ x][self._ships[i]._y ] += 1#self._ships[i]._cells[0]


        except (TypeError, IndexError):
                showerror('coords error','check your coords2')
                self.entry_true = True

        if sorted([item for sublist in self.pole for item in sublist])[-1]>1:
            showerror('coords error', 'check your coords')
            self.entry_true = True

        if self.entry_true == True:
            print(False)

            self.entry_true = False
        else:
            self.entry_true = True

    def set_coords_pc_label(self):
        for i in range(10):

            self.pc_ships[i].set_start_coords((randint(0, self._size-1), randint(0, self._size-1)))


    def get_pc_pole(self):
        self.pc_pole = [[0 for i in range(self._size)] for j in range(self._size)]
        try:

            for i in range(10):
                if sorted([item for sublist in self.pc_pole for item in sublist])[-1] > 1:
                    self.pc_ships[i-1].set_start_coords((randint(0, self._size-1), randint(0, self._size-1)))
                    i-=1
                else:
                    for x in range(len(self.pc_ships[i]._cells)):


                        if self.pc_ships[i]._tp == 1:

                            self.pc_pole[self.pc_ships[i]._x][self.pc_ships[i]._y+x] += 1
                        else:


                            self.pc_pole[self.pc_ships[i]._x+ x][self.pc_ships[i]._y ] += 1


        except (IndexError):

            self.pc_ships[-i].set_start_coords((randint(0, self._size-1), randint(0, self._size-1)))
            i-=1
            self.get_pc_pole()

        if sorted([item for sublist in self.pc_pole for item in sublist])[-1] > 1:
            self.get_pc_pole()



    def print_pole(self):
        self.win_update()

        x = ''
        for i in self.pole:
            x += '  '.join(map(lambda x: str(x)+' ' if x !='*' else '*', i))

            x += ' \n'

        return x


    def print_pc_pole(self):
        print(self.pc_pole)
        print(self.pole)
        self.win_update()
        x=''
        for i in self.pc_pole:

            x+='  '.join(map(lambda x: '*' if x not in (0,1) else '0 ', i))

            x+='\n'
        return x

    def get_attack(self, x):
        x = Ship.set_start_coords(self, x)
        if self.pc_pole[x[0]][x[1]]==1:
            try:
                self.pc_pole[x[0]][x[1]]='* '
                self.pc_xp-=1
            except TypeError:
                return



    def get_attack_by_pc(self):
        x = randint(0,self._size-1)
        y = randint(0,self._size-1)
        print(x,y)
        self.attack_list.append((x,y))
        if self.attack_list.count((x,y))==2:
            print('==========================================================')
            self.attack_list.remove((x,y))
            self.get_attack_by_pc()


        if self.pole[x][y]==1:
            self.pole[x][y]= '* '
            self.xp-=1

    def win_update(self):
        if self.xp == 0:
            self.win = 1
        if self.pc_xp == 0:
            self.win = 2

    @property
    def pc_win(self):
        return self.win == 2

    @property
    def pc_win(self):
        return self.win == 1

    def __bool__(self):
        return self.win == 0 and self.win not in (1,2)


class FirstWindow:
    __slots__ = 'root'

    def __init__(self):
        self.root = Tk()
        self.root.title('ship')
        self.root.geometry('600x200')
        self.root.resizable(False, False)

        lab_text = open('win.txt', 'r')

        lab = ttk.Label(self.root, text=lab_text.read())
        lab.place(x = 10, y = 10)

        but = ttk.Button(self.root, text='start', width=20, command=self.start)
        but.place(x = 240, y = 120)

        self.root.mainloop()

    def start(self):

        self.root.destroy()
        self.root = None

    def __bool__(self):
        return True if self.root !=None else False


class Window:
    __slots__ = 's', 'wich_window'

    def __init__(self, s):
        self.s = s
        self.wich_window = None


    def creat_creat(self, r = None):
        if r!=None:
            r.destroy()
            self.play_ground.root.destroy()

        start = WindowCreate()

        start.start_window()
        start.start()



    def verch(self, r):
        self.main_menu = Menu(r)
        self.main_menu.add_cascade(label="leading", command= self.leading)
        self.main_menu.add_cascade(label="exit", command= self.exit)
        if self.__class__ == WindowPlay:
            self.main_menu.add_cascade(label="reset", command= partial(self.creat_creat, r))

        r.config(menu=self.main_menu)

    def leading(self):
        root = Tk()
        root.title('leading')
        root.geometry('600x400')
        root.resizable(False, False)

        leading = open('leading.txt', 'r')

        label = ttk.Label(root, text=leading.read())
        label.place(x = 0, y= 0)




    def exit(self):
        self.root.destroy()
        if self.__class__ == WindowPlay:
            self.play_ground.root.destroy()




    @abstractclassmethod
    def start_window(cls):
        pass


    def start(self):

        self.root.mainloop()


    def place_label_matrix(self, root, x1,y1,x2,y2):
        x = ''
        for i in range(self.s._size):
            x += ''.join(str(i))
            if i<10:
                x += '''  .\n'''
            else:
                x += ''' .\n'''



        self.label_matrix1 = ttk.Label(root, text=x)

        self.label_matrix1.place(x = x1,y = y1)
        if self.__class__ == WindowCreate:
            self.label_pole(root, 30, 40)




        y = ' '
        keys = [*d.keys()]
        print(keys)
        for i in range(self.s._size):
            y += ''.join(str(keys[i]).upper())
            if i in (2, 5, 11, 12, 14, 13):
                y += '''  '''
            else:
                y += '''   '''

        y+='\n'+'  '.join('.  ' if i<10 else '.   ' for i in range(self.s._size) )

        self.label_matrix = ttk.Label(root, text=y)
        self.label_matrix.place(x = x2,y = y2)


    def pole_update(self):
        self.s.pole = [[0 for j in range(self.s._size)] for i in range(self.s._size)]


    def label_pole(self, root, x, y):
        if self.__class__ == WindowCreate:
            self.label_my_pole = ttk.Label(root, text=f'{self.s.print_pole()}')
            self.label_my_pole.place(x =x,y = y)
        else:
            self.label_my_pole = ttk.Label(root, text=f'{self.s.print_pole()}')
            self.label_my_pole.place(relx=0.98, rely=0.1, anchor = NE )

    def __bool__(self):
        return True



class WindowCreate(Window):
    __slots__ = 'second_window', 'd', 'taps', 'root', 'main_menu', 'label_matrix1',\
    'label_my_pole', 'label_matrix', 'select', 'button'


    def __init__(self):
        super().__init__(s)
        self.second_window = ' 8'
        self.d = {}
        self.taps = 0


    def start_window(self):

        self.root = Tk()
        self.root.title('ship')
        self.root.geometry('600x400')
        self.root.resizable(False, False)

        self.verch(self.root)

        self.s.init()
        self.place_label_matrix(self.root,10, 40,
                                          25, 10)
        self.entry()


        self.instruck_label(True)



        self.radiobutton()
        self.button = ttk.Button(width=10, text= 'create', command=self.click_entry)
        self.button.place(x=520, y=240 )





    def click_entry(self):

        try:
            for i in range(10):
                self.s.get_ships()[i].set_start_coords(str(self.d.get(f'entry{i}').get()))
                self.label_my_pole.destroy()#print(s.get_ships()[i].set_start_coords(list(self.d.get(f'entry{i}').get())))
        except IndexError:
            showwarning('info','enter your coords')
            self.s.entry_true = False


        self.s.get_pole()
        self.label_pole(self.root, 30, 40)

        if self.s.entry_true:
            self.taps+=1
            self.button['text'] = 'start game'
            if self.taps == 2:
                self.taps = 0
                self.recurse()
                self.root.destroy()
                play = WindowPlay()
                play.start_window()
                play.start()

        else:
            self.taps=0
            self.button['text'] = 'create'

    def recurse(self):
        try:
            self.s.set_coords_pc_label()
            self.s.get_pc_pole()
        except RecursionError:
            self.recurse()



    def matrix_destroy(self):
        self.label_matrix.destroy()
        self.label_matrix1.destroy()


    def set_long(self, i):
        self.matrix_destroy()
        self.label_my_pole.destroy()
        setattr(self.s, '_size', i)

        self.pole_update()
        self.place_label_matrix(self.root, 10, 40,
                                25, 10)


    def radiobutton(self):
       dradio = {}
       self.select = IntVar()
       for i in range(10,16):
            dradio[f"{i}"] = ttk.Radiobutton( value=i, command=partial(self.set_long, i))
            dradio.get(f'{i}').place(x=10+i*35,y=5)
            dradio_label = ttk.Label(text=f'{i}')
            dradio_label.place(x=10+i*35, y= 30)


    def instruck_label(self, exist):
        file = open('instraction.txt', 'r')

        instruckt = ttk.Label(text=file.read())
        instruckt.place(x=350,y=80)
        if exist == False:
            instruckt.destroy()


    def entry(self):
        z = 0
        for i in range(2):
            for j in range(5):

                self.d[f'entry{z}'] = ttk.Entry(width=9)
                self.d.get(f'entry{z}').place(x=10+j*120, y=300+i*60)

                if self.s._ships[z]._tp == 1:

                    label_orient = ttk.Label(text='--')
                else:
                    label_orient = ttk.Label(text='|')
                label_orient.place(x=80+j*120, y=300+i*60)

                label = ttk.Label(text=f'{len(self.s._ships[z]._cells)} палубный')
                label.place(x=10+j*120, y=280+i*60)


                z+=1


    def __bool__(self):
        return False if self.s.entry_true and self.taps==2 else True
        
        
class WindowPlay(Window):
    _instanse = None

    def __init__(self):
        super().__init__(s)
        self.correct_clicks = 1
        self.second_window = ''




    def start_window(self):

        self.root = Tk()
        self.root.title('ship')
        self.root.geometry('600x370')



        self.verch(self.root)

        self.place_label_matrix(self.root, 10, 40,
                                            25, 10)

        self.label_pc_pole = ttk.Label(self.root, text=f'{self.s.print_pc_pole()}')
        self.label_pc_pole.place(x=30, y=40)


        self.label_pole(self.root, 300, 40)



        self.attack_entry = ttk.Entry(self.root, width=9)
        self.attack_entry.place(anchor = NE, relx=0.126, rely=0.77)

        enter_coords_label = ttk.Label(self.root, text='''  /\\/\\/\\/\\/\\
enter coords''')
        enter_coords_label.place(anchor = NE, relx=0.138, rely=0.84)



        self.play_ground = YourPlaygroundWindow(self.second_window)
        self.rules_label = ttk.Label(self.root, text=f'''To attack enter coords.
Blow all enemy ships to win
    
>>you have notebook of your attack coords''')
        self.rules_label.place(relx = 0.99, rely = 0.78, anchor = NE)
        self.button_attack = ttk.Button(self.root,width=10, text='attack', command=self.click_attack)
        self.button_attack.place(relx = 0.97, rely = 0.79, anchor = E)
    def click_attack(self):

        try:
            try:
                self.play_ground.root.destroy()
            except TclError:
                pass
            self.second_window = self.second_window + (str(self.attack_entry.get())) + '|'
            if len(self.second_window.split('|'))%13==0:
                self.second_window +='\n'


            self.play_ground = YourPlaygroundWindow(self.second_window)

            try:
                self.s.get_attack(self.attack_entry.get())
            except ValueError:
                return

            self.label_pc_pole.destroy()
            self.label_pc_pole = ttk.Label(self.root, text=f'{self.s.print_pc_pole()}')
            self.label_pc_pole.place(x = 30, y = 40)



            self.label_my_pole.destroy()
            self.s.get_attack_by_pc()
            print(self.s.print_pc_pole())
            self.correct_clicks+=1

            self.label_pole(self.root, 300, 40)
            print(self.s.print_pole())
        except (IndexError):
            showerror('coords error', 'check your coords')

        if self.s.win!=0:
            self.button_attack.destroy()
            if self.s.win == 1:
                showinfo('win update', 'computer win')
            else:
                showinfo('win update', 'you win')
            self.win_label = ttk.Label(self.root, text='''
>>press reset to continue                                                                           
>>press exit to stop game                                                                                 ''')
            self.win_label.place(anchor=CENTER)
            self.win_label.place(x=300, y=200)


class YourPlaygroundWindow(WindowPlay):
    __slots__ = 'second_window', 'dic'


    def __init__(self, second):
        super().__init__()
        self.second_window = second
        self.dic = {}
        self.start_window1()

    def start_window1(self):
        self.root = Tk()
        self.root.title('ship2')
        self.root.geometry('250x300')
        self.root.resizable(False, False)

        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=RIGHT, fill=Y)


        self.label_play = ttk.Label(self.root, text=f'{self.second_window}')
        self.label_play.place(x=1, y=1)
        self.label_play = Listbox(self.root, yscrollcommand = scrollbar.set )
        scrollbar.config(command=self.label_play.yview)




    def start(self):
        self.root.mainloop()


first = FirstWindow()

if not first:
    s = Pole()
    s.init()


    s.print_pc_pole()

    first = Window(s)
    first.creat_creat()



