from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from kivy.properties import StringProperty, ListProperty, NumericProperty

# Явно загружаем main.kv
Builder.load_file("main.kv")


class StartScreen(Screen):
    def on_enter(self):
        self.ids.start_button.disabled = True
        self.ids.date_label.text = f"Дата: {datetime.now().strftime('%d.%m.%Y')}"

    def check_input(self):
        name = self.ids.name_input.text.strip()
        self.ids.start_button.disabled = (len(name) == 0)

    def start_test(self):
        app = App.get_running_app()
        app.user_name = self.ids.name_input.text.strip()
        app.group = self.ids.group_input.text.strip()
        self.manager.current = "topic"


class TopicScreen(Screen):
    topics = ListProperty([
        "Вредоносное ПО",
        "Сетевая безопасность",
        "Пароли и аутентификация",
        "Итоговый тест"
    ])

    def on_enter(self):
        grid = self.ids.topics_grid
        grid.clear_widgets()
        from kivy.uix.button import Button
        for topic in self.topics:
            btn = Button(text=topic, size_hint_y=None, height=50)
            btn.bind(on_release=lambda instance, t=topic: self.select_topic(t))
            grid.add_widget(btn)

    def select_topic(self, topic):
        app = App.get_running_app()
        app.current_topic = topic
        self.manager.get_screen("test").load_questions(topic)
        self.manager.current = "test"


class TestScreen(Screen):
    questions = ListProperty([])
    current_question_index = NumericProperty(0)
    correct_answers = NumericProperty(0)
    selected_answers = ListProperty([])

    def load_questions(self, topic):
        sample_questions = {
            "Вредоносное ПО": [
                {"question": "Что такое троян?", "type": "single",
                 "options": ["Антивирус", "Вредоносная программа", "Брандмауэр", "Протокол"], "answer": 1},
                {"question": "Какие типы вредоносного ПО существуют?", "type": "multiple",
                 "options": ["Вирусы", "Шифровальщики", "Антивирусы", "Червяки"], "answer": [0, 1, 3]},
                {"question": "Как называется ПО, которое собирает данные без согласия пользователя?", "type": "text", "answer": "Шпионское ПО"},
                {"question": "Что из перечисленного помогает защититься от вирусов?", "type": "single",
                 "options": ["Регулярное обновление ПО", "Использование пиратского ПО", "Отключение антивируса", "Открытие неизвестных ссылок"], "answer": 0},
                {"question": "Какой тип вредоносного ПО шифрует файлы и требует выкуп?", "type": "single",
                 "options": ["Червь", "Шпионское ПО", "Рансомварь", "Троян"], "answer": 2},
            ],
            "Сетевая безопасность": [
                {"question": "Какой протокол обеспечивает шифрование данных в интернете?", "type": "single",
                 "options": ["HTTP", "FTP", "HTTPS", "SMTP"], "answer": 2},
                {"question": "Какие меры повышают сетевую безопасность?", "type": "multiple",
                 "options": ["Использование VPN", "Открытые Wi-Fi сети", "Брандмауэр", "Отключение шифрования"], "answer": [0, 2]},
                {"question": "Как называется атака, перехватывающая сетевой трафик?", "type": "text", "answer": "MITM"},
                {"question": "Что защищает от несанкционированного доступа к сети?", "type": "single",
                 "options": ["Антивирус", "Брандмауэр", "Шифровальщик", "Браузер"], "answer": 1},
                {"question": "Какой порт обычно используется для HTTPS?", "type": "single",
                 "options": ["80", "443", "21", "25"], "answer": 1},
            ],
            "Пароли и аутентификация": [
                {"question": "Какой длины должен быть минимально безопасный пароль?", "type": "single",
                 "options": ["4 символа", "8 символов", "12 символов", "16 символов"], "answer": 2},
                {"question": "Какие элементы делают пароль более безопасным?", "type": "multiple",
                 "options": ["Цифры", "Имя пользователя", "Символы", "Заглавные буквы"], "answer": [0, 2, 3]},
                {"question": "Как называется метод аутентификации с использованием пароля и кода из приложения?", "type": "text", "answer": "Двухфакторная аутентификация"},
                {"question": "Что из перечисленного является плохой практикой?", "type": "single",
                 "options": ["Использование одинаковых паролей", "Двухфакторная аутентификация", "Регулярная смена паролей", "Использование менеджеров паролей"], "answer": 0},
                {"question": "Какой метод защиты пароля использует хеширование?", "type": "single",
                 "options": ["Шифрование", "Соление", "Кодирование", "Сжатие"], "answer": 1},
            ],
            "Итоговый тест": [
                {"question": "Что из перечисленного является антивирусом?", "type": "single",
                 "options": ["WannaCry", "Kaspersky", "NotPetya", "Trojan"], "answer": 1},
                {"question": "Какие меры защищают от фишинга?", "type": "multiple",
                 "options": ["Проверка URL", "Открытие всех писем", "Ан Lilllкаждое письмо", "Антивирус"], "answer": [0, 3]},
                {"question": "Как называется атака, обманом заставляющая пользователя раскрыть данные?", "type": "text", "answer": "Фишинг"},
                {"question": "Что из перечисленного защищает от вредоносного ПО?", "type": "single",
                 "options": ["Регулярное обновление ПО", "Открытие неизвестных вложений", "Отключение брандмауэра", "Использование слабых паролей"], "answer": 0},
                {"question": "Какой тип аутентификации наиболее безопасен?", "type": "single",
                 "options": ["Пароль", "Биометрия", "Двухфакторная аутентификация", "PIN-код"], "answer": 2},
            ]
        }

        self.questions = sample_questions.get(topic, [])
        self.current_question_index = 0
        self.correct_answers = 0
        self.selected_answers = []
        self.show_question()

    def show_question(self):
        self.ids.answer_box.clear_widgets()
        if not self.questions:
            self.ids.question_label.text = "Вопросы не найдены."
            return

        q = self.questions[self.current_question_index]
        self.ids.question_label.text = f"Вопрос {self.current_question_index + 1}: {q['question']}"

        if q["type"] == "single":
            from kivy.uix.checkbox import CheckBox
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label

            self.selected_answers = [-1]
            box = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)
            box.bind(minimum_height=box.setter('height'))
            for i, option in enumerate(q["options"]):
                hl = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
                cb = CheckBox(group="single", size_hint_x=0.2)

                def on_cb_active(cb, value, idx=i):
                    if value:
                        self.selected_answers[0] = idx

                cb.bind(active=on_cb_active)
                lbl = Label(text=option, halign="left", valign="middle", size_hint_x=0.8)
                lbl.bind(size=lbl.setter('text_size'))
                hl.add_widget(cb)
                hl.add_widget(lbl)
                box.add_widget(hl)

            self.ids.answer_box.add_widget(box)

        elif q["type"] == "multiple":
            from kivy.uix.checkbox import CheckBox
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label

            self.selected_answers = []
            box = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)
            box.bind(minimum_height=box.setter('height'))
            for i, option in enumerate(q["options"]):
                hl = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
                cb = CheckBox(size_hint_x=0.2)

                def on_cb_active(cb, value, idx=i):
                    if value:
                        if idx not in self.selected_answers:
                            self.selected_answers.append(idx)
                    else:
                        if idx in self.selected_answers:
                            self.selected_answers.remove(idx)

                cb.bind(active=on_cb_active)
                lbl = Label(text=option, halign="left", valign="middle", size_hint_x=0.8)
                lbl.bind(size=lbl.setter('text_size'))
                hl.add_widget(cb)
                hl.add_widget(lbl)
                box.add_widget(hl)

            self.ids.answer_box.add_widget(box)

        elif q["type"] == "text":
            from kivy.uix.textinput import TextInput

            self.selected_answers = [""]
            ti = TextInput(multiline=False, size_hint_y=None, height=40)

            def on_text(instance, value):
                self.selected_answers[0] = value.strip()

            ti.bind(text=on_text)
            self.ids.answer_box.add_widget(ti)

    def next_question(self):
        self.check_answer()
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.show_question()
        else:
            self.manager.current = "result"

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def check_answer(self):
        q = self.questions[self.current_question_index]
        ans = self.selected_answers
        if q["type"] == "single":
            if ans and ans[0] == q["answer"]:
                self.correct_answers += 1
        elif q["type"] == "multiple":
            if sorted(ans) == sorted(q["answer"]):
                self.correct_answers += 1
        elif q["type"] == "text":
            if ans and ans[0].lower() == q["answer"].lower():
                self.correct_answers += 1

    def finish_test(self):
        self.check_answer()
        self.manager.current = "result"


class ResultScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        total = len(app.root.get_screen("test").questions)
        correct = app.root.get_screen("test").correct_answers
        self.ids.result_label.text = f"Правильных ответов: {correct} из {total}"
        self.ids.name_label.text = f"ФИО: {app.user_name}"
        self.ids.group_label.text = f"Группа: {app.group}"


class DefenceApp(App):
    user_name = StringProperty("")
    group = StringProperty("")
    current_topic = StringProperty("")

    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(TopicScreen(name="topic"))
        sm.add_widget(TestScreen(name="test"))
        sm.add_widget(ResultScreen(name="result"))
        return sm


if __name__ == "__main__":
    DefenceApp().run()
