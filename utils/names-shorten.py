import sys

for fullname in sys.stdin:
    last_name, first_name, middle_name, *_ = fullname.split(" ")
    print(f"{last_name} {first_name[0]}.{middle_name[0]}.")
