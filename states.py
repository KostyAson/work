import aiogram
import aiogram.fsm
import aiogram.fsm.context
import aiogram.fsm.state


class SupportState(aiogram.fsm.state.StatesGroup):
    messaging = aiogram.fsm.state.State()


class ErrorState(aiogram.fsm.state.StatesGroup):
    messaging = aiogram.fsm.state.State()


class AddInstructionState(aiogram.fsm.state.StatesGroup):
    add = aiogram.fsm.state.State()
