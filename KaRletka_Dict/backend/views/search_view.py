from .base_view import *
from ..logic import get_search


class SearchView(BaseView, CreateCard):
    def __init__(self, page):
        super().__init__(page)

        self.interface = []

        self.menu = ft.Column(
            expand=True if self.platform != 'android' else False
        )
        self.word = ft.TextField(label="Word", on_change=lambda _: self.change_text_fields())
        self.translate = ft.TextField(label="Translate", on_change=lambda _: self.change_text_fields())
        self.btn_submit = ft.ElevatedButton("Search", on_click=lambda _: self.btn_click())
        self.l_cards = ft.ListView(
            spacing=10,
            expand=True,
        )

        self.menu.controls.append(self.word)
        self.menu.controls.append(self.translate)
        self.menu.controls.append(self.btn_submit)
        self.menu.controls.append(self.l_cards)

        self.interface.append(self.menu)

        self.view.controls = self.interface
        self.view.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def update_size(self):
        if self.platform != 'android':
            self.menu.width = self.get_width_for_menu()
            self.menu.height = self.get_height_for_menu()
        self.view.update()

    def btn_click(self):
        data = get_search(word=self.word.value, translate=self.translate.value)
        self.update_l_results(data)

    def change_text_fields(self):
        if len(self.word.value) > 4 or len(self.translate.value) > 4:
            data = get_search(word=self.word.value, translate=self.translate.value)
            self.update_l_results(data)
        else:
            self.l_cards.controls.clear()
            self.view.update()

    def update_l_results(self, data):
        new_l_cards = [
            self.create_card(info)
            for info in data
        ]

        self.l_cards.controls = new_l_cards
        self.view.update()

    def get_width_for_menu(self):
        if self.page.width > 700:
            return self.page.width * get_option('Search_interface', self.platform, 'width',
                                                0)
        else:
            return self.page.width * get_option('Search_interface', self.platform, 'width', 1)

    def get_height_for_menu(self):
        return self.page.height * get_option('Search_interface', self.platform, 'height', 0)



    def get_view(self):
        return self.view
