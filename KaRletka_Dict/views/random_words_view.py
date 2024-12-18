from .base_view import *


class RandomCardsView(ListCards):
    def __init__(self, page):
        super().__init__(page)

        self.interface = []

        self.l_cards = self.create_l_cards('random', size=15)
        self.btn_update = ft.IconButton(icon='UPDATE', icon_size=20, on_click=self.btn_update_click)
        self.interface = [self.l_cards, self.btn_update]

        self.view.controls = self.interface
        self.view.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def btn_update_click(self, e):
        self.l_cards.controls = self.update_l_cards('random', size=15)
        self.view.update()

    def get_view(self):
        return self.view
