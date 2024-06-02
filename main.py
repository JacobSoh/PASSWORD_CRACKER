import sys
from Package import cracker

def main():
    # Class PWD_Cracker is stored under Package 
    pwdCrackerCls = cracker.PWD_Cracker(threads=4)
    pwdCrackerCls.begin()
    pwdCrackerCls.main()
    result = pwdCrackerCls.get_found_password()
    if result != None:
        print(f"Password is {result}")
        sys.exit()
    else:
        print("No password found")

if __name__ == "__main__":
    main()