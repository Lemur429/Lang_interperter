class Error:
    def __init__(self,pos_start,pos_end,name,detail):
        self.name=name
        self.detail=detail
        self.pos_start=pos_start
        self.pos_end=pos_end

    def __str__(self):
        return f'Error! {self.name} , {self.detail}\nIn File {self.pos_start.fn}, line {self.pos_start.ln+1}'
    
class IllegalChracterError(Error):
    def __init__(self,pos_start,pos_end,detail):
        super().__init__(pos_start,pos_end,'Illegal Character',detail)