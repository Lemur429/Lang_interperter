from strings_with_arrows import *
class Error:
    def __init__(self,pos_start,pos_end,name,detail):
        self.name=name
        self.detail=detail
        self.pos_start=pos_start
        self.pos_end=pos_end

    def __str__(self):
        msg=f'Error! {self.name} , {self.detail}'
        msg+=f'\nIn File {self.pos_start.fn}, line {self.pos_start.ln+1}'
        msg+='\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return msg
    
class IllegalChracterError(Error):
    def __init__(self,pos_start,pos_end,detail):
        super().__init__(pos_start,pos_end,'Illegal Character',detail)
class InvalidSyntax(Error):
    def __init__(self,pos_start,pos_end,detail):
        super().__init__(pos_start,pos_end,'Syntax Error',detail)
class ExpectedChar(Error):
      def __init__(self,pos_start,pos_end,detail):
        super().__init__(pos_start,pos_end,'Expected Character',detail)
class RTError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, 'Runtime Error', details)
		self.context = context

	def as_string(self):
		result  = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result
