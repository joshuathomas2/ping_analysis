import os
import re
import sys

def main():
    analyze_file(choose_file())

    print("Analyze another file? (y/n)")
    answer = input()
    
    if (answer.lower() == "y"):
        main()
    else:
        return 1

def choose_file():
    data = os.listdir("data")
    file_count = list(range(len(data)))
    user_choices = list(zip(file_count, data))

    for choice in user_choices:
        print(choice)

    print("Enter the number of the file you wish to anaylze:")
    choice = user_choices[int(input())][1]
    return choice

def analyze_file(file_name):
    ping_list = []
    ping_count = 0
    average_ping = 0
    tiny_ping_count = 0
    small_ping_count = 0
    medium_ping_count = 0
    large_ping_count = 0
    extreme_ping_count = 0

    print("Attempting to analyze... " + file_name)

    try:
        text_file = open("data/" + file_name, "r")
    except FileNotFoundError:
        print("Incorrect directory or not a text file")
        main()
    except PermissionError:
        print("Directory did not point to a specific file or permission was denied")
        main()
        
    for line in text_file:
        if (line[0:5] == "Reply"):
            ping_count += 1
            ping_list.append(int(re.split("[ ]", line)[4][5:][:-2]))

    if (len(ping_list) == 0):
        print("Error with text file: found no ping data")
        main()
    else:
        average_ping = int((sum(ping_list)/len(ping_list)))
    
    for ping in ping_list:
        if (ping > 200):
            extreme_ping_count += 1
        elif (ping > 100):
            large_ping_count += 1
        elif (ping > 75):
            medium_ping_count += 1
        elif (ping > 25):
            small_ping_count += 1
        elif (ping > 1):
            tiny_ping_count += 1

    print("====================================================")
    print("Total ping count: ", ping_count)
    print("====================================================")
    print("Tiny ping count:", tiny_ping_count, "(>1ms)")
    print("Small ping count:", small_ping_count, "(>25ms)")
    print("Medium ping count:", medium_ping_count, "(>75ms)")
    print("Large ping count:", large_ping_count, "(>100ms)")
    print("Extreme ping count:", extreme_ping_count, "(>200ms)")
    print("MAXIMUM ping:", max(ping_list))
    print("MINIMUM ping:", min(ping_list))
    print("AVERAGE ping:", average_ping)
    print("====================================================")

    return 1

if __name__ == "__main__":
    main()
