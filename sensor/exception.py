# handling errors and helps customize error messages
import sys
import os

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info() #func in sys library
    filename = exc_tb.tb_frame.f_code.co_filename #tell us which file has error
    
    error_message = "error occured in file name [{0}] in line number [{1}] : [{2}]".format(
    filename, exc_tb.tb_lineno, str(error))

    return error_message

class SensorException(Exception): #Exception is a super class
    def __init__(self, error_message, error_detail:sys): # sys library for error detail(the file which has error, line number)
                                                         # error message

        super().__init__(error_message) # use the Exception class

        self.error_message = error_message_detail(error_message, error_detail = error_detail)


    def __str__(self): #since error message is not in a string format we create this function
        return self.error_message 
