import os
import re
import sys

def main():
    analyze_file(choose_file())
    main()

def choose_file():
    data = os.listdir("data")
    file_count = list(range(len(data)))
    user_choices = list(zip(file_count, data))

    for choice in user_choices:
        print(choice[0], ":", choice[1])

    print_space(1)
        
    choice = input("Enter the number of the file you wish to analyze (enter nothing to quit): ")

    if (choice == ""):
        sys.exit()

    try:
        choice = int(choice)
    except ValueError:
        print_error("invalid_number")
        main()

    if ((choice > len(user_choices) - 1) or (choice < 0)):
        print_error("invalid_number")
        main()
    else:
        choice = user_choices[choice][1]
            
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

    print_space(14)
    print("Attempting to analyze... " + file_name)

    text_file = open("data/" + file_name, "r")
        
    for line in text_file:
        if (line[0:5] == "Reply"):
            ping_count += 1
            ping_time = int(re.split(" ", line)[4][5:][:-2])
            ping_list.append(ping_time)

    if (len(ping_list) == 0):
        print_error("no_data")
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
    print("[", file_name, "]", "Total ping count: ", ping_count)
    print("====================================================")
    
    print("Tiny ping count:", tiny_ping_count, "   (>1ms)",
    round((tiny_ping_count / ping_count) * 100,2), "%")
    
    print("Small ping count:", small_ping_count, " (>25ms)",
    round((small_ping_count / ping_count) * 100,2), "%")
    
    print("Medium ping count:", medium_ping_count, "  (>75ms)",
    round((medium_ping_count / ping_count) * 100,2), "%")
    
    print("Large ping count:", large_ping_count, "  (>100ms)",
    round((large_ping_count / ping_count) * 100,2), "%")
    
    print("Extreme ping count:", extreme_ping_count, "(>200ms)",
    round((extreme_ping_count / ping_count) * 100,2), "%")
    
    print_space(1)
    print("MAXIMUM ping:", max(ping_list))
    print("MINIMUM ping:", min(ping_list))
    print("MEAN ping:", average_ping)
    print("====================================================")
    print_space(15)

    input("Press enter to continue...")
    print_space(20)
    
    return 1

def print_error(error):
    if (error == "no_data"):
        print_space(1)
        print("Error with text file: No data found or file is not in UTF-8")
        print_space(1)
    elif (error == "invalid_number"):
        print_space(1)
        print("Invalid number")
        print_space(1)

def print_space(number):
    for i in range(number):
        print("")

if __name__ == "__main__":
    main()
