import os, zipfile, json
from multiprocessing import Process, Queue, Event
from itertools import product
from Package.simple_func import create_folder

TYPE_FILE = "FILE"
TYPE_HASH = "HASH"
METHOD_RAINBOW= "RAINBOW"
METHOD_BRUTE_FORCE = "BRUTE_FORCE"

class PWD_Cracker:
    def __init__(self, threads = 4) -> None:
        self.__saveFilePath = os.path.join(os.getcwd(),"ExtractionProcess")
        self.__numOfThreads = threads
        self.__foundPassword = Queue()
        self.__password_found_event = Event()

        with open("Settings.json") as sf:
            data = json.load(sf)
            self.type = data["TYPE"]
            self.method = data["METHOD"]
            self.__rTablePath = data["DICTIONARY"] 
            self.__filePath  = data["FILE_PATH"]
            self.__bf_length = data["BRUTE_FORCE_LENGTH"]
        pass

    # Simple inputs to before beginning cracking the password
    def begin(self) -> None:
        create_folder(self.__saveFilePath)

    def _crack_file(self,pwd) -> tuple:
        try:
            # Extracting file using data
            # Tested testzip but it only reads the zipfile, doesn't decrypt
            with zipfile.ZipFile(self.__filePath) as f: 
                f.extractall(pwd=bytes(pwd, "utf-8"), path=self.__saveFilePath)
            return True
        except Exception as e:
            if __name__ == "__main__":
                print(f"Error occured at file test_thread.py line 33: {e}")
            return False

    def thread_worker(self, queue) -> None:
        while not self.__password_found_event.is_set():
            try:
                pwd = queue.get(timeout=1)
                if pwd is None:
                    break
            except Exception as e:
                if __name__ == "__main__":
                    print(f"Error occured at file test_thread.py line 44: {e}")
                break
            result = self._crack_file(pwd)
            if result:
                self.__foundPassword.put(pwd)
                self.__password_found_event.set()
                break
        self.__foundPassword.put(None)

    def main(self) -> dict:
        processes = []
        queues = [Queue()] * self.__numOfThreads
        
        for i in range(self.__numOfThreads):
            proc = Process(target=self.thread_worker, args=(queues[i],))
            processes.append(proc)
            proc.start()

        if self.method == METHOD_RAINBOW:
            with open(self.__rTablePath,"r") as rtf:
                for i, pwd in enumerate(rtf):
                    queues[i % self.__numOfThreads].put(pwd.strip())
        elif self.method == METHOD_BRUTE_FORCE:
            charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for i, combination in enumerate(product(charset, repeat=self.__bf_length)):
                pwd = ''.join(combination)
                queues[i % self.__numOfThreads].put(pwd.strip())

        for que in queues:
            que.put(None)

        for proc in processes:
            proc.join()

        for proc in processes:
            proc.terminate()

        create_folder(self.__saveFilePath)
        return pwd
        
    def get_found_password(self) -> str:
        pwd = self.__foundPassword.get(timeout = 1)
        if pwd != None:
            self._crack_file(pwd)
        return pwd
