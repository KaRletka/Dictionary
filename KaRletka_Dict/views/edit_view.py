from .input_view import *
from .logic import edit_word, del_word


class EditView(InputView):
    def __init__(self, page, data):
        super().__init__(page)

        self.btn_delete = ft.ElevatedButton('Delete', on_click=lambda _: self.delete_word())
        self.btns_wrapper.controls.append(self.btn_delete)

    def show_notification(self):
        self.notification.content = ft.Text(f'Изменено слово {self.word.value}, {self.word.value}')
        self.notification.open = True
        self.page.update()

    def btn_click(self):
        edit_word(
            {
                'word_id': self.word_id,
                'word': self.word.value,
                'transcription': self.transcription.value,
                'translate': self.translate.value,
                'addition': self.addition.value
             }
        )
        self.show_notification()
        self.update_controls()

    def set_info(self, data: dict):
        self.word_id = data['word_id']
        self.word.value = data['word']
        self.transcription.value = data['transcription']
        self.translate.value = data['translate']
        self.addition.value = data['addition']

    def delete_word(self):
        del_word(
            {
                'word_id': self.word_id,
                'word': ' ',
                'translate': ' ',
            },
        )
        self.show_notification()
        self.update_controls()