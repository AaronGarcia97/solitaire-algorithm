# Algoritmo Solitaire
from pathlib import Path

class Reader(object):

    @staticmethod
    def leer_archivo_arr(path: Path):
        with open(path.absolute(), 'r') as f:
            return f.read().strip().split(' ')

    @staticmethod
    def leer_archivo(path: Path):
        with open(path.absolute(), 'r') as f:
            return f.read().strip()

class Passphrase(object):

    def __init__(self, s):
        print('s')
        self.passphrase = s
        self.curr = 0
    
    def get_next_amount(self):
        if self.curr >= len(self.passphrase):
            self.curr = 0
        return ord(self.passphrase[self.curr])

class Deck(object):
    
    def __init__(self):
        tmp_cartas = [int(s) for s in Reader.leer_archivo_arr(Path("./deck.txt"))]
        self.set_deck(tmp_cartas)
        self.initial_cartas = self.cartas.copy()
        self.curr_keystream = -1
        self.keystreams = []
        self.passphrase = Passphrase(Reader.leer_archivo(Path("./passphrase.txt")).replace(' ', '').upper())
        print(f"[LOADED] Cards: {self.cartas} | Size: {self.size}")

    def set_deck(self, arr):
        self.joker_1 = 53
        self.joker_2 = 54
        self.cartas = arr
        self.size = len(arr)

    def reset_deck(self):
        self.set_deck(self.initial_cartas.copy())

    # handles swapping (0,-1) and (size-1,size), will break if both i,j >= size or both i,k < 0
    def swap(self, i, j):
        low, high = (i, j) if i < j else (j, i)   # get low and high index
        low = self.size-1 if low < 0 else low # if trying to swap with 0, swap with top of deck
        high = 1 if high >= self.size else high
        self.cartas[low], self.cartas[high] = self.cartas[high], self.cartas[low]

    # i=initial_index, n=times, these 2 fucntions could be merged
    def swap_n_times_left(self, i, n):
        # handles swapping from top when reaching swap with -1 
        while(n > 0):
            while(i >= 0 and n > 0):
                self.swap(i, i-1)
                i, n = i-1, n-1
            i = self.size-1 # start swapping from top again

    # i=initial_index, n=times, these 2 functions could be merged
    def swap_n_times_right(self, i, n):
        # handles swapping top with bot
        while(n > 0):
            while(i < self.size and n > 0):
                self.swap(i, i+1)
                i, n = i+1, n-1
            i = 0 # start swapping from bot again

    def triple_cut(self, i, j):
        fir_joker, sec_joker = (i, j) if i < j else (j, i)
        left = self.cartas[0:fir_joker]
        mid = self.cartas[fir_joker:sec_joker+1]
        right = self.cartas[sec_joker+1:self.size] # What if sec_joker is == to self.size-1? => returns []
        # print(f"L{left}\nM{mid}\nR{right}")
        self.set_deck(right + mid + left)

    # bring top N cards to bot-1
    def bring_top_n(self, amount):
        top = self.cartas[0:amount]
        mid = self.cartas[amount:-1]
        last = [self.cartas[-1]]
        self.set_deck(mid + top + last)

    def get_curr_keystream(self):
        i = self.cartas[0]
        # we don't add +1 cause it's 0 indexed
        return self.cartas[i]

    def set_curr_keystream(self, k):
        self.curr_keystream = k

    def step1(self):
        i = self.cartas.index(self.joker_1)
        self.swap(i, i+1)
    
    def step2(self):
        i = self.cartas.index(self.joker_2)
        self.swap_n_times_right(i, 2)

    def step3(self):
        joker_1_i = self.cartas.index(self.joker_1)
        joker_2_i = self.cartas.index(self.joker_2)
        self.triple_cut(joker_2_i, joker_1_i)

    def step4(self):
        self.bring_top_n(self.cartas[-1])

    def step4_5(self):
        if len(self.passphrase.passphrase) > 0:
            self.bring_top_n(self.passphrase.get_next_amount())

    def step5(self):
        self.set_curr_keystream(self.get_curr_keystream())
        self.keystreams.append(self.curr_keystream)

# UTILITY
# bp = boilerplate
def LOG_FORMAT(msg, bp=''):
    i = 0
    output = f'[+] {bp}'
    for c in msg:
        mod = i % 5
        if mod == 0:
            output += ' '
        output += c
        i += 1
    print(output)

class Runner(object):
    BASE = 26
    INITIAL_LETTER = ord('A')
    def __init__(self, deck: Deck):
        self.deck = deck
        self.alphabet = self.create_alphabet()

    def run(self):
        self.deck.step1()
        self.deck.step2()
        self.deck.step3()
        self.deck.step4()
        self.deck.step4_5() # sec passphrase
        self.deck.step5()
        # print(f"Keystream: {self.deck.get_curr_keystream()}\n{self.deck.cartas}")
    
    def generate_n_keystreams(self, n, reset_deck=False):
        if reset_deck:
            self.deck.reset_deck()
        for _ in range(n):
            self.run()
        print(f"[+] {0 if n < 0 else n} keystreams generated.")
        return self.deck.keystreams.copy()

    def create_alphabet(self):
        # create alphabet
        alph = {}
        for i in range(self.INITIAL_LETTER, self.INITIAL_LETTER+self.BASE):
           alph[chr(i)] = i-self.INITIAL_LETTER+1 #A=1, B=2 ... Z=26
        return alph
    
    # when 'B', num=2, B_ascii=INITIAL_LETTER+num-1
    def convert_to_letter(self, num):
        return chr(self.INITIAL_LETTER + num - 1)
    
    def convert_to_nums(self, msg):
        return [self.alphabet[c] for c in msg]

    def gen_missing_keystreams(self, msg_padded, gen_new_keystreams=False):
        if gen_new_keystreams:
            return self.generate_n_keystreams(len(msg_padded), reset_deck=gen_new_keystreams)
        else:
            # if diff > 0: we need more keystreams, gen them, else dont
            diff = len(msg_padded) - len(self.deck.keystreams)
            return self.generate_n_keystreams(diff)

    def convert_to_base(self, num):
        # NEW impl: ignoring pdf, using longer deck
        mod = num % self.BASE
        c = self.BASE if mod == 0 else mod
        return c
        # OLD impl: following pdf
        # sum is higher than upper limit => 26
        if num > self.BASE:
            return num - self.BASE
        # subtraction is lower than lower limit => 1
        if num < 1:
            return num + self.BASE
        return num

    def convert_to_padded_msg(self, msg):
        msg_caps = ''.join([c.upper() for c in msg if c.upper() in self.alphabet])
        LOG_FORMAT(msg_caps, bp='!Padding:')
        msg_padded = msg_caps + ''.join(['X' for _ in range(5 - len(msg_caps) % 5)])
        LOG_FORMAT(msg_padded, bp=' Padding:')
        return msg_padded

    # new_keystreams=True => resets deck and gens new keystreams
    def encode(self, msg, gen_new_keystreams=False):
        encoded_msg_arr = []
        print(f'[+] Encoding: {msg}.')
        msg_padded = self.convert_to_padded_msg(msg)
        keystreams = self.gen_missing_keystreams(msg_padded, gen_new_keystreams)
        nums_arr = self.convert_to_nums(msg_padded)
        for i in range(len(nums_arr)):
            summ = nums_arr[i] + keystreams[i]
            # convert sum to base self.BASE
            summ = self.convert_to_base(summ)
            encoded_msg_arr.append(self.convert_to_letter(summ))
        output = ''.join(encoded_msg_arr)
        LOG_FORMAT(output, bp=' Encoded:')
        return output

    def decode(self, msg, gen_new_keystreams=False):
        decoded_msg_arr = []
        nums_arr = self.convert_to_nums(msg)
        keystreams = self.gen_missing_keystreams(msg, gen_new_keystreams)
        for i in range(len(nums_arr)):
            subtr = nums_arr[i] - keystreams[i]
            # convert to base self.BASE, we convert result of substraction instead of top num, ss
            subtr = self.convert_to_base(subtr)
            decoded_msg_arr.append(self.convert_to_letter(subtr))
        output = ''.join(decoded_msg_arr)
        LOG_FORMAT(output, bp=' Decoded:')
        return output


if __name__ == "__main__":
    d = Deck()
    r = Runner(d)