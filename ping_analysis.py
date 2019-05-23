import re

#C:/Users/shady/Desktop/PING/libertyIP.txt
def main():
    analyze_file(get_path())

    print("Analyze another file? (y/n)")
    answer = input()
    
    if (answer.lower() == "y"):
        main()
    else:
        return 1

def get_path():
    print("Enter the full path to the desired text file:")
    file_path = input()
    print("Analyzing " + file_path)
    return file_path

def analyze_file(file_path):
    text_file = open(file_path, "r")
    ping_list = []
    ping_count = 0
    average_ping = 0
    above_average_ping_count = 0
    tiny_ping_count = 0
    small_ping_count = 0
    medium_ping_count = 0
    large_ping_count = 0
    extreme_ping_count = 0

    for line in text_file:
        if (line[0:5] == "Reply"):
            ping_count += 1
            ping_list.append(int(re.split("[ ]", line)[4][5:][:-2]))

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

    for ping in ping_list:
        if (ping > average_ping):
            above_average_ping_count += 1

    print("====================================================")
    print("Tiny ping count:", tiny_ping_count, "(>1ms)")
    print("Small ping count:", small_ping_count, "(>25ms)")
    print("Medium ping count:", medium_ping_count, "(>75ms)")
    print("Large ping count:", large_ping_count, "(>100ms)")
    print("Extreme ping count:", extreme_ping_count, "(>200ms)")
    print("MAXIMUM ping:", max(ping_list))
    print("MINIMUM ping:", min(ping_list))
    print("AVERAGE ping:", average_ping)
    print("Pings above the average occured", above_average_ping_count, "out of", ping_count, "times")
    print("====================================================")

    return 1

if __name__ == "__main__":
    main()
