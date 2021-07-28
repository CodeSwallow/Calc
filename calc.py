from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView

class RV(RecycleView):
	def __init__(self, **kwargs):
		super(RV, self).__init__(**kwargs)
		self.data=[]

	def add_label(self, result_before, second_number, result, operator):
		text=result_before+' '+operator+' '+second_number+' = '+result
		self.data.append({'text': text, 'font_size': '18', 'color': [0,0,0,1]})


class FloatInput(TextInput):
	operators=['+', '-', '*', '/']
	def insert_text(self, substring, from_undo=False):
		s=''
		if substring in self.operators:
			self.parent.parent.add_operator(substring)
		else:
			if substring=='.' and not '.' in self.text:
				s=substring
				self.parent.parent.add_number(substring)
			elif substring.isdigit():
				s=substring
				self.parent.parent.add_number(substring)
		return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class Calculator(BoxLayout):
	first_number=''
	second_number=''
	operator=''
	def __init__(self, **kwargs):
		super(Calculator, self).__init__(**kwargs)

	def answer(self, button_text):
		if button_text:
			self.first_number=button_text
			self.ids.expresion_input.text=button_text
			self.operator=''
			self.ids.operator_label.text=''
			self.ids.last_operation_label.text=''
			self.second_number=''
		self.ids.expresion_input.focus=True

	def add_operator(self, operator):
		if self.ids.expresion_input.text:
			if not self.operator:
				self.operator=operator
				if self.first_number=='.':
					self.first_number='0.0'
				self.ids.last_operation_label.text=self.first_number
				self.ids.expresion_input.text=''
				self.second_number=self.first_number
				self.first_number=''
				print("first operator assigned")
			else:
				if self.first_number=='.':
					self.first_number='0.0'
				if self.operator=='/' and not float(self.first_number):
					self.ids.warning.text="Can't divide by zero"
				else:
					result=str(self.do_operation(float(self.second_number), float(self.first_number), self.operator))
					self.ids.rvs.add_label(self.second_number, self.first_number, result, self.operator)
					self.ids.last_operation_label.text=result
					self.second_number=result
					self.first_number=''
					self.operator=operator
					self.ids.expresion_input.text=''
					self.ids.warning.text=''
					print("operation done!")
			self.ids.operator_label.text=self.operator
		elif self.ids.last_operation_label.text and self.ids.operator_label.text:
			self.operator=operator
			self.ids.operator_label.text=self.operator
		self.ids.expresion_input.focus=True

	def equal(self):
		if self.second_number and self.operator and self.first_number:
			if self.first_number=='.':
				self.first_number='0.0'
			if self.operator=='/' and not float(self.first_number):
				self.ids.warning.text="Can't divide by zero"
			else:
				result=str(self.do_operation(float(self.second_number), float(self.first_number), self.operator))
				self.ids.rvs.add_label(self.second_number, self.first_number, result, self.operator)
				self.ids.last_operation_label.text=result
				self.second_number=result
				self.first_number=''
				self.ids.expresion_input.text=''
				self.ids.warning.text=''

	def erase(self, clear_all, clear_entry=True):
		if clear_all:
			self.ids.expresion_input.text=''
			self.ids.last_operation_label.text=''
			self.ids.operator_label.text=''
			self.operator=''
			self.first_number=''
			self.second_number=''
			self.ids.warning.text=''
		else:
			if clear_entry:
				self.ids.expresion_input.text=''
				self.first_number=''
			else:
				new_input=self.ids.expresion_input.text[0:-1]
				self.first_number=new_input
				self.ids.expresion_input.text=new_input
		self.ids.expresion_input.focus=True

	def delete_history(self):
		self.ids.rvs.data=[]
		self.ids.expresion_input.focus=True

	def positive_negative(self):
		if self.ids.expresion_input.text:
			self.ids.expresion_input.text=str(float(self.ids.expresion_input.text)*(-1))
			self.first_number=self.ids.expresion_input.text
		self.ids.expresion_input.focus=True

	def multiplicative_inverse(self):
		if self.ids.expresion_input.text:
			number=self.ids.expresion_input.text
			if number=='.':
				number='0.0'
			if float(number):
				self.ids.expresion_input.text=str(1/float(number))
				self.first_number=str(1/float(number))
				self.ids.rvs.add_label('1', number, self.first_number, '/')
				self.ids.warning.text=''
			else:
				self.ids.warning.text="Can't get multiplicative inverse of zero"
		self.ids.expresion_input.focus=True


	def power_of_two(self):
		if self.ids.expresion_input.text:
			number=self.ids.expresion_input.text
			if number=='.':
				number='0.0'
			self.ids.expresion_input.text=str(float(number)*float(number))
			self.first_number=str(float(number)*float(number))
			self.ids.rvs.add_label(number, '2', self.first_number, '**')
			self.ids.warning.text=''
		self.ids.expresion_input.focus=True

	def squared(self):
		if self.ids.expresion_input.text:
			number=self.ids.expresion_input.text
			if number=='.':
				number='0.0'
			if float(number)>=0:
				self.ids.expresion_input.text=str(float(number)**(1/2))
				self.first_number=str(float(number)**(1/2))
				self.ids.rvs.add_label(number, '(1/2)', self.first_number, '**')
				self.ids.warning.text=''
			else:
				self.ids.warning.text="Can't get square root of negative number"
		self.ids.expresion_input.focus=True				


	def percent(self):
		if self.ids.expresion_input.text and self.ids.last_operation_label.text and self.ids.operator_label.text:
			percent=float(self.first_number)/100
			percent=float(self.second_number)*percent
			result=str(self.do_operation(float(self.second_number), percent, self.operator))
			self.ids.rvs.add_label(self.second_number, self.first_number+'%', result, self.operator)
			self.ids.last_operation_label.text=result
			self.second_number=result
			self.first_number=''
			self.ids.expresion_input.text=''
			self.ids.warning.text=''
		self.ids.expresion_input.focus=True


	def add_number(self, number):
		self.first_number+=number
		self.ids.expresion_input.focus=True

	def do_operation(self, first_number, second_number, operator):
		if operator=='+':
			return first_number+second_number
		elif operator=='-':
			return first_number-second_number
		elif operator=='*':
			return first_number*second_number
		elif operator=='/':
			return first_number/second_number


class CalcApp(App):
	def build(self):
		return Calculator()


if __name__=='__main__':
	CalcApp().run()