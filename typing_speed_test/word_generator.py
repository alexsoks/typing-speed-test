#class that takes in the word_canvas and prints out a series of randomely selected words

from tkinter import Canvas
from wonderwords import RandomSentence


#constants for canvas function
window_height = 500
window_width = 1000
word_canv_height = window_height / 7
font_name = "Courier"
font = 35


class WordGenerator:

    def __init__(self, canvas: Canvas):
        self.canvas_obj = canvas


        self.pointer = 0

        #word bank will be the 7 words that will be displayed per line of typing
        self.word_bank = []

        self.attempt_bank = ['*', '*', '*', '*']

        #the first thing that will be done upon initiation is fill the word bank
        self.bank_refresh()

        self.print_words()

        self.correct_words = 0





    #function that fills the word bank with new random words
    def bank_refresh(self):
        #set the pointer back to 0
        self.pointer = 0

        #clear the word canvas
        self.canvas_obj.delete('all')

        #refresh the attempt bank
        self.attempt_bank = ['*', '*', '*', '*']

        #refresh the word bank
        self.word_bank = []

        # create a RandomSentence object
        r = RandomSentence()

        #creates a simple sentence string
        sentence = r.sentence()

        #break down the sentence into an array of words
        sentence = sentence.split(" ")

        # ensures that the last word in the list has no full stop
        sentence[-1] = sentence[-1].split(".")[0]

        #appends all the sentence words into the word bank (2nd to 5th only), ensuring each word is in lower case
        for i in sentence[1:5]:

            self.word_bank.append(i.lower())



    def print_words(self):

        #in the case that the pointer becomes 4, reset word bank and attempt bank
        if self.pointer == 4:
            self.bank_refresh()




        x = (window_width/2)-300


        for i in range(4):


            #for each word we'll compare against corresponding entry in the attempt bank. if its a '*' leave word
            #as whaite as pointer hasn't reached word yet. If the pointer is at the word, leave as orange as typing
            #process is still occuring. If there's a corresponding entry in attempt bank, compare against it and change
            #color parameter accordingly

            if self.attempt_bank[i] == "*":
                color = "white"

            #whatever the word_generator 'pointer' attribute is will determine which word is orange
            if i == self.pointer:
                color = "orange"

            if self.attempt_bank[i] != "*":
                if self.attempt_bank[i] == self.word_bank[i]:
                    color = "#39FF14"
                    self.correct_words += 1
                else:
                    color = "red"

            font_size = 25

            if len(self.word_bank[i]) > 7:
                font_size = 20



            self.canvas_obj.create_text(x, word_canv_height/2, text=self.word_bank[i], font=(font_name, font_size, 'bold'), fill=color)

            #increase x to create spacing between each of the words
            x += 200








