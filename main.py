import tkinter
from word_generator import WordGenerator
from wpm_calculator import WpmCalculator






# ----------------------- CONSTANTS ----------------------------
window_height = 500
window_width = 1000
background_col = "#BADA55"
font_name = "Courier"
stats_canv_height = window_height / 6
word_canv_height = window_height / 7
wpm = 0
timer_running = False

#variable used to first store the window.after() that runs the timer. This variable will then be referenced by the
#wind.after_cancel() method to stop the timer upon call of refresh function.
recursion = 0




#tkinter window object
window = tkinter.Tk()
window.title("typing speed test")

#initialise wpm calculator object
wpm_calc = WpmCalculator()




def game():


    #key pressed event
    def key_pressed(event):
        global timer_running
        global wpm

        #temporarily gets rid of instruction label once typing begins, indicating the start of the game
        instructions.grid_forget()


        #changes timer text to green as soon as a key is pressed
        stats_canvas.itemconfig(timer_text, fill="#39FF14")

        #ensures that function can't be called again due to key being pressed after initial calling
        if timer_running == False:
            #starts the timer as soon as a key is pressed
            timer_start(60)

        key_pushed = event.keysym

        if key_pushed in ["space", "Return"]:
            # update the wpm on the stats canvas
            stats_canvas.itemconfig(wpm_text, text=f"WPM: {str(wpm)}")

            #insert word entry into designated position in WordGenerator object's  attempt_bank (determined by current pointer)
            wg.attempt_bank[wg.pointer] = get_text()
            wg.pointer += 1
            wg.print_words()



    # upon entering a key, game begins running
    window.bind('<KeyRelease>', key_pressed)



    # funtion to extract text entered into Text widget
    def get_text():
        # retrieve entered text
        retrieved_txt = text_input.get("1.0", tkinter.END)
        # ignores any spaces before text entry
        retrieved_txt = retrieved_txt.strip()

        # clear the Text widget for next entry
        text_input.delete("1.0", tkinter.END)

        return retrieved_txt

    # assigns Enter key triggers get_text function
    # window.bind('<Return>', get_text)



    # function that controls timer
    def timer_start(time):
        global timer_running
        global recursion
        global wpm

        timer_running = True


        #every second we're going to update the wpm value
        wpm = wpm_calc.calculate_wpm(wg.correct_words, time)


        stats_canvas.itemconfig(timer_text, text=f"time left: {str(time)}")
        time -= 1

        if time >= 0:
            recursion = window.after(1000, timer_start, time)

        else:
            timer_running = False
            stats_canvas.itemconfig(timer_text, fill="black")
            results()



    def refresh():
        global recursion

        #reset the word_generator object's correct words attribute to 0
        wg.correct_words = 0

        # always set the timer running to false when game is restarted
        global timer_running
        timer_running = False
        window.after_cancel(recursion)

        game()

    ######## UI SETUP #######
    window.minsize(width=window_width, height=window_height)
    window["bg"] = background_col

    # Title, Stats, Word Display, Input Bar

    # create label for title
    title = tkinter.Label(text="Typing Speed Test", fg="blue", bg=background_col, font=(font_name, 35, 'bold'))
    title.grid(column=1, row=0, pady=20)


    #instructions clarifying that game begins once anything is typed
    instructions = tkinter.Label(text="Start typing to being test!", fg="black", bg=background_col, font=(font_name, 20, 'bold'))
    instructions.grid(column=1, row=5, pady=10)


    # create stats canvas
    stats_canvas = tkinter.Canvas(width=window_width, height=stats_canv_height, bg="grey")
    stats_canvas["highlightthickness"] = 0
    stats_canvas.grid(column=1, row=1)

    # stats canvas words
    wpm_text = stats_canvas.create_text(window_width / 2 - 300, stats_canv_height / 2, text=f"WPM: {str(wpm)}",
                                        fill="black", font=(font_name, 20, 'bold'))

    timer_text = stats_canvas.create_text(window_width / 2 + 300, stats_canv_height / 2,
                                          text=f"time left: 60", fill="black",
                                          font=(font_name, 20, 'bold'))

    # word canvas generation
    word_canvas = tkinter.Canvas(width=window_width, height=word_canv_height, bg="black")
    word_canvas["highlightthickness"] = 0

    word_canvas.grid(column=1, row=2, pady=10)


    #initiate our WordGenerator object to control this word canvas
    wg = WordGenerator(word_canvas)


    # text input bar
    text_input = tkinter.Text(height=3, width=20, font=(font_name, 20, 'bold'))
    # ensures that upon app start, widget doesn't have to be clicked before it's active
    text_input.focus_set()

    text_input.grid(column=1, row=3)

    # reset button
    reset_button = tkinter.Button(text="Restart", width=8, height=2, fg="blue", font=(font_name, 15, 'bold'), command=refresh)
    reset_button.grid(column=1, row=4, pady=20)





    window.mainloop()



def results():
    global wpm

    widgets = window.grid_slaves()
    for i in widgets:
        i.destroy()


    def back_to_game():

        #get rid of result widgets before returning back to game
        results_label_1.destroy()
        results_label_2.destroy()
        reset_button_2.destroy()


        game()







    #label showing results
    results_label_1 = tkinter.Label(text=f"Your typing speed is", fg="blue", bg=background_col, font=(font_name, 35, 'bold'))
    results_label_1.place(x=300, y=80)

    results_label_2 = tkinter.Label(text=f"{wpm} WPM", fg="blue", bg=background_col,font=(font_name, 100, 'bold'))
    results_label_2.place(x=360, y=160)

    reset_button_2 = tkinter.Button(text="Try Again", width=16, height=4, fg="blue", font=(font_name, 15, 'bold'), command=back_to_game)
    reset_button_2.place(x=450, y=400)




game()
