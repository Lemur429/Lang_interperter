class Error:
    def __init__(self,name,detail):
        self.name=name
        self.detail=detail

    def __str__(self):
        return f'Error! {self.name} , {self.detail}'
    
class IllegalChracterError(Error):
    def __init__(self,detail):
        super().__init__('Illegal Character',detail)