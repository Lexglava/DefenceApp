from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.config import Config

Config.set('kivy','keyboard_mode','systemanddock')
Config.set('graphics', 'resizable', True)

class StartScreen(Screen):
    def check_input(self, instance, value):
        self.ids.btn.disabled = len(value.strip()) == 0

    def start_test(self):
        self.manager.get_screen('test').reset_test()
        self.manager.current = 'test'

class QuestionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = [
            # Single-choice
            {
                'type': 'single',
                'question': 'Что такое межсетевой экран (firewall)?',
                'answers': [
                    'Аппаратное или программное решение, контролирующее сетевой трафик',
                    'Антивирусный сканер',
                    'Шифровальный протокол',
                    'Сервис резервного копирования'
                ],
                'correct': 0
            },
            # Multiple-choice
            {
                'type': 'multiple',
                'question': 'Какие из перечисленных мер помогают защитить компьютер от вредоносного ПО?',
                'answers': [
                    'Регулярное обновление ОС',
                    'Скачивание программ с неизвестных сайтов',
                    'Использование антивируса',
                    'Отключение брандмауэра'
                ],
                'correct': [0, 2]
            },
            # Text input

            {
                'type': 'text',
                'question': 'Как называется протокол для защищённой передачи данных по HTTP?',
                'correct': 'HTTPS'
            },
            # True/False
            {
                'type': 'true_false',
                'question': 'Использование сложных паролей снижает риск несанкционированного доступа.',
                'correct': True
            },
            # Single-choice
            {
                'type': 'single',
                'question': 'Какой метод защиты предотвращает физический доступ к внутренностям ПК?',
                'answers': [
                    'Шифрование данных',
                    'Установка замка на корпус',
                    'Брандмауэр',
                    'Антивирус'
                ],
                'correct': 1
            },
        ]
        self.total_questions = len(self.questions)
        self.reset_test()

    def reset_test(self):
        self.current_question = 0
        self.user_answers = [None] * self.total_questions
        self.correct_answers = 0
        self.answered_correctly = [False] * self.total_questions
        self.update_question()
        self.update_score()

    def clear_answers_container(self):
        self.ids.answers_container.clear_widgets()

    def update_question(self):
        q = self.questions[self.current_question]
        self.ids.question_label.text = q['question']
        self.ids.question_counter.text = f'Вопрос {self.current_question + 1} из {self.total_questions}'
        self.ids.prev_btn.disabled = self.current_question == 0
        self.ids.next_btn.disabled = self.current_question == self.total_questions - 1

        self.clear_answers_container()

        if q['type'] == 'single':
            self._build_single(q)
        elif q['type'] == 'multiple':
            self._build_multiple(q)
        elif q['type'] == 'text':
            self._build_text(q)
        elif q['type'] == 'true_false':
            self._build_tf(q)

    def _build_single(self, q):
        self.answer_buttons = []
        for idx, ans in enumerate(q['answers']):
            btn = Button(text=ans, size_hint=(1, 0.15),
                         background_color=(0.9, 0.9, 0.95, 1),
                         color=(0.1, 0.1, 0.2, 1))
            btn.bind(on_press=lambda inst, i=idx: self._on_single(i, q))
            self.answer_buttons.append(btn)
            self.ids.answers_container.add_widget(btn)

    def _on_single(self, idx, q):
        self.user_answers[self.current_question] = idx
        correct = idx == q['correct']
        for i, btn in enumerate(self.answer_buttons):
            if i == q['correct']:
                btn.background_color = (0.2, 0.8, 0.4, 1)
            elif i == idx:
                btn.background_color = (0.9, 0.4, 0.4, 1)
            else:
                btn.background_color = (0.9, 0.9, 0.95, 1)
        self._update_score(correct)

    def _build_multiple(self, q):
        self.checkboxes = []
        for idx, ans in enumerate(q['answers']):
            row = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
            cb = CheckBox(size_hint=(0.2, 1))
            lbl = Label(text=ans, size_hint=(0.8, 1), color=(0.1,0.1,0.2,1))
            self.checkboxes.append(cb)
            row.add_widget(cb)
            row.add_widget(lbl)
            self.ids.answers_container.add_widget(row)

    def _save_multiple(self):
        selected = [i for i, cb in enumerate(self.checkboxes) if cb.active]
        self.user_answers[self.current_question] = selected
        correct = set(selected) == set(self.questions[self.current_question]['correct'])
        self._update_score(correct)

    def _build_text(self, q):
        self.text_input = TextInput(
            hint_text='Введите ответ',
            size_hint=(1, 0.2),
            multiline=False,
            background_color=(1,1,1,1),
            foreground_color=(0.1,0.1,0.2,1)
        )
        self.ids.answers_container.add_widget(self.text_input)

    def _save_text(self):
        ans = self.text_input.text.strip()
        self.user_answers[self.current_question] = ans
        correct = ans.lower() == self.questions[self.current_question]['correct'].lower()
        self._update_score(correct)

    def _build_tf(self, q):
        self.tf_buttons = []
        btn_t = ToggleButton(text='Верно', group='tf', size_hint=(1,0.15))
        btn_f = ToggleButton(text='Неверно', group='tf', size_hint=(1,0.15))
        self.tf_buttons = [btn_t, btn_f]
        self.ids.answers_container.add_widget(btn_t)
        self.ids.answers_container.add_widget(btn_f)

    def _save_tf(self):
        ans = (self.tf_buttons[0].state == 'down')
        self.user_answers[self.current_question] = ans
        correct = ans == self.questions[self.current_question]['correct']
        self._update_score(correct)

    def _update_score(self, is_correct):
        if not self.answered_correctly[self.current_question] and is_correct:
            self.correct_answers += 1
            self.answered_correctly[self.current_question] = True
        elif self.answered_correctly[self.current_question] and not is_correct:
            self.correct_answers -= 1
            self.answered_correctly[self.current_question] = False
        self.update_score()

    def update_score(self):
        self.ids.score_label.text = f'Правильно: {self.correct_answers}/{self.total_questions}'

    def prev_question(self, *args):
        if self.current_question > 0:
            self._save_current()
            self.current_question -= 1
            self.update_question()

    def next_question(self, *args):
        if self.current_question < self.total_questions - 1:
            self._save_current()
            self.current_question += 1
            self.update_question()

    def _save_current(self):
        qtype = self.questions[self.current_question]['type']
        if qtype == 'multiple':
            self._save_multiple()
        elif qtype == 'text':
            self._save_text()
        elif qtype == 'true_false':
            self._save_tf()

    def finish_test(self, *args):
        self._save_current()
        perc = self.correct_answers / self.total_questions * 100
        self.manager.get_screen('results').show_results(perc)
        self.manager.current = 'results'

class ResultsScreen(Screen):
    def show_results(self, percentage):
        self.ids.percentage_label.text = f'{percentage:.1f}%'

        if percentage >= 80:
            self.ids.result_label.text = 'Отличный результат!'
            self.ids.result_label.color = (0.2, 0.2, 0.2, 1)
            self.ids.percentage_label.color = (0.7, 0.6, 0, 1)
        elif percentage >= 50:
            self.ids.result_label.text = 'Хороший результат!'
            self.ids.result_label.color = (0.2, 0.2, 0.2, 1)
            self.ids.percentage_label.color = (0.9, 0.7, 0, 1)
        else:
            self.ids.result_label.text = 'Попробуйте ещё раз!'
            self.ids.result_label.color = (0.2, 0.2, 0.2, 1)
            self.ids.percentage_label.color = (0.8, 0.5, 0, 1)

    def restart_test(self):
        self.manager.current = 'start'


class Main(App):
    def build(self):
        Window.clearcolor = (0.95, 0.97, 1, 1)
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(QuestionScreen(name='test'))
        sm.add_widget(ResultsScreen(name='results'))
        return sm

if __name__ == '__main__':
    Main().run()
