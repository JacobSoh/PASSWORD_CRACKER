import os, zipfile, json
from multiprocessing import Process, Queue, Event, Manager
from itertools import product
from Package.simple_func import create_folder

# Variables for the Settings.json
TYPE_FILE = "FILE"
TYPE_HASH = "HASH"
METHOD_RAINBOW= "RAINBOW"
METHOD_BRUTE_FORCE = "BRUTE_FORCE"

class PWD_Cracker:
    def __init__(self, threads = 4) -> None:
        self.__saveFilePath = os.path.join(os.getcwd(),"ExtractionProcess") # The folder that we will save all the extracted files
        self.__numOfThreads = threads
        self.__foundPassword = Manager().dict() # A storage space accessible to all threads
        self.__password_found_event = Event() # Ensures that once a password is found, terminate all threads

        with open("Settings.json") as sf:
            data = json.load(sf)
            self.type = data["TYPE"]
            self.method = data["METHOD"]
            self.__rTablePath = data["DICTIONARY"] 
            self.__filePath  = data["FILE_PATH"]
            self.__bf_length = data["BRUTE_FORCE_LENGTH"] # Ref line 76
        pass

    # Simple inputs to before beginning cracking the password
    def begin(self) -> None:
        create_folder(self.__saveFilePath)

    def _crack_file(self,pwd) -> tuple:
        try:
            with zipfile.ZipFile(self.__filePath) as f:  # Test extracting with password. "testzip" only reads the contents of the zipfile
                f.extractall(pwd=bytes(pwd, "utf-8"), path=self.__saveFilePath)
            return True
        except Exception as e:
            if __name__ == "__main__":
                print(f"Error occured at file test_thread.py line 33: {e}")
            return False

    def thread_worker(self, queue) -> None:
        while not self.__password_found_event.is_set(): # The event where a password is found in line 52, stop the Queue.
            try:
                pwd = queue.get(timeout=1)
                if pwd is None: # Ensure once all the possible passwords are ran through, stop the Queue.
                    break
            except Exception as e:
                if __name__ == "__main__":
                    print(f"Error occured at file test_thread.py line 44: {e}")
                break
            result = self._crack_file(pwd)
            if result:
                self.__foundPassword["pwd"] = pwd
                self.__password_found_event.set() # Password is found, exit all the Queues
                break

    def main(self) -> dict:
        processes = []
        queues = [Queue()] * self.__numOfThreads
        
        for i in range(self.__numOfThreads): # Classic threading creation
            proc = Process(target=self.thread_worker, args=(queues[i],))
            processes.append(proc)
            proc.start()

        if self.method == METHOD_RAINBOW:
            with open(self.__rTablePath,"r") as rtf:
                for i, pwd in enumerate(rtf): # Run through each lines in the textfile
                    queues[i % self.__numOfThreads].put(pwd.strip())
        elif self.method == METHOD_BRUTE_FORCE:
            charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for i, combination in enumerate(product(charset, repeat=self.__bf_length)): # Create all possible combination of length = self.__bg_length
                pwd = ''.join(combination)
                queues[i % self.__numOfThreads].put(pwd.strip())

        for que in queues:
            que.put(None) # Once all combinations of password is done, put all None to exit all Processes

        for proc in processes:
            proc.join() # Joins all to wait for all Processes to be completed

        create_folder(self.__saveFilePath) # Delete the mess that was created in line 34
        return pwd
        
    def get_found_password(self) -> str:
        pwd = self.__foundPassword["pwd"]
        if pwd != None:
            self._crack_file(pwd)
        return pwd
