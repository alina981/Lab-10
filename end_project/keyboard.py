from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# тут делаем кнопочки

main = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Сбербанк')],
                                       [KeyboardButton(text = 'Tinkoff')]],
                           resize_keyboard=True, input_field_placeholder='Выберите свой банк')
cards = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Дебетовая', callback_data='Дебетовая')],
                                              [InlineKeyboardButton(text = 'Кредитная', callback_data='Кредитная')],
                                              [InlineKeyboardButton(text = 'Счёт', callback_data='Счёт')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Отправить номер телефона', request_contact=True)]],
                                 resize_keyboard=True)

# Категории
EXPENSE_CATEGORIES = ["Еда", "Транспорт", "Жильё", "Учёба", "Развлечения", "Медицина", "Другое"]
INCOME_CATEGORIES = ["Стипендия", "Подработка", "Подарок", "Другое"]

# Удаление клавиатуры
remove_keyboard = ReplyKeyboardRemove()

# Клавиатура выбора типа операции
operation_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Доход"), KeyboardButton(text="Расход")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Функция для получения клавиатуры категорий
def get_categories_keyboard(operation_type):
    categories = INCOME_CATEGORIES if operation_type == "доход" else EXPENSE_CATEGORIES
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=item)] for item in categories],
        resize_keyboard=True,
        one_time_keyboard=True
    )