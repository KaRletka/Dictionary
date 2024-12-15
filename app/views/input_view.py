from .base_view import *
from logic import inp_word


class InputView(BaseView):
    def __init__(self, page):
        super().__init__(page)

        self.interface = []

        self.interface_wrapper = ft.Column(width=self.get_width_for_column())
        self.btns_wrapper = ft.Row()
        self.word = ft.TextField(label="Word")
        self.translate = ft.TextField(label="Translate")
        self.transcription = ft.TextField(label='Transcription')
        self.addition = ft.TextField(label="Addition", multiline=True)
        self.btn_submit = ft.ElevatedButton("Enter", on_click=lambda _: self.btn_click())

        self.btns_wrapper.controls.append(self.btn_submit)

        self.interface_wrapper.controls.append(self.word)
        self.interface_wrapper.controls.append(self.transcription)
        self.interface_wrapper.controls.append(self.translate)
        self.interface_wrapper.controls.append(self.addition)
        self.interface_wrapper.controls.append(self.btns_wrapper)

        self.interface.append(self.interface_wrapper)

        self.view.controls = self.interface  # adding controls to view
        self.view.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.notification = ft.SnackBar(content=ft.Text(''), duration=3000)

    def update_size(self, *args):
        self.interface_wrapper.width = self.get_width_for_column()
        self.view.update()

    def get_width_for_column(self):
        if self.page.width > 700:
            return self.page.width * get_option('Input_interface', self.platform, 'width',
                                                0)
        else:
            return self.page.width * get_option('Input_interface', self.platform, 'width',
                                                1)

    def show_notification(self):
        self.notification.content = ft.Text(f'Добавленно слово {self.word.value}, {self.word.value}')
        self.notification.open = True

    def btn_click(self):
        inp_word(
            {
                'word_id': None,
                'word': self.word.value,
                'transcription': self.transcription.value,
                'translate': self.translate.value,
                'addition': self.addition.value
             },
        )
        self.show_notification()
        self.update_controls()

    def update_controls(self):
        self.word.value = ''
        self.transcription.value = ''
        self.translate.value = ''
        self.addition.value = ''

        self.view.update()

    def get_view(self):
        return self.view
