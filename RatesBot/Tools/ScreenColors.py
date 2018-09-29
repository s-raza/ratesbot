class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'
    
    def blue(self,txt):
        return self.BLUE + txt + self.ENDC

    def green(self,txt):
        return self.GREEN + txt + self.ENDC
        
    def red(self,txt):
        return self.RED + txt + self.ENDC
        
    def yellow(self,txt):
        return self.YELLOW + txt + self.ENDC
        
    def fail(self,txt):
        return self.FAIL + txt + self.ENDC
        
    def bold(self,txt):
        return self.BOLD + txt + self.ENDC
        
    def bgred(self,txt):
        return self.BGRED + txt + self.ENDC
        
    def white(self,txt):
        return self.WHITE + txt + self.ENDC
        
       
clr = bcolors()