class WpmCalculator:

    #when the word count and time is passed in, calculates and returns the wpm at that instant

    def calculate_wpm(self, word_count, time):

        if word_count == 0:
            return 0

        if time == 60:
            return 0


        seconds_passed = 60 - time

        wps = word_count/seconds_passed

        wpm = wps * 60

        return int(wpm)

