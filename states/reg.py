from aiogram.dispatcher.filters.state import State, StatesGroup


class RegOneChild(StatesGroup):
	step1 = State()
	step2 = State()
	step3 = State()
	step4 = State()
	step5 = State()
	step6 = State()
	step7 = State()
	step8 = State()
	additive = State()

class RegManyChild(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
    step5 = State()