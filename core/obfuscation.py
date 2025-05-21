import subproccess
import sys
import os
    
def obfuscate_payload():
    file_input = input("Enter the file path")

    obfuscation_type = input("Enter the obfuscation method you wamt to apply: ")
    if obfuscation_type == None:
        print("wrong answer")
        pass
    elif obfuscation_type == "jigsaw":
        print("you chose the jigsaw obfuscation method")
    
    elif obfuscation_type == "jargon":
        print("ypu chose the jargon obfuscation method")


    isValid = False
    
    def file_input():
        if != file_input:
            print("No filepath specified!")
            isValid = True
            return
        else:
            print("Failed!")
            isValid = False
            
    def check_file(file_input):
        pass