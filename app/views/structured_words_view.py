from .base_view import *


class StructuredCardsView(ListCards):
    def __init__(self, page):
        super().__init__(page)

        self.l_cards = self.create_l_cards('pagination', size=15, page=1)
        self.page_num = ft.TextField(value='1', col=4, width=20, on_submit=lambda _: self.change_page())
        self.nav_bar = self.create_pagination_interface()

        self.interface = [self.l_cards, self.nav_bar]

        self.view.controls = self.interface
        self.view.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def btn_pagination_click(self, direction):
        if int(self.page_num.value) + direction != 0:
            self.page_num.value = str(int(self.page_num.value) + direction)
        self.change_page()
        self.notification.content = ft.Text(f'Window size {str(self.page.width)}, {str(self.page.height)} | Page: {self.page}')
        self.notification.open = True
        self.page.update()

    def change_page(self):
        self.l_cards.controls = self.update_l_cards('pagination', size=15, page=int(self.page_num.value))
        self.view.update()

    def create_pagination_interface(self):
        container = ft.Container(
            content=ft.ResponsiveRow(width=400),
            # padding=ft.padding.only(top=-7)
        )

        btn_next = ft.IconButton(icon='ARROW_RIGHT', icon_size=20, col=4,
                                 on_click=lambda _: self.btn_pagination_click(1))
        btn_back = ft.IconButton(icon='ARROW_LEFT', icon_size=20, col=4,
                                 on_click=lambda _: self.btn_pagination_click(-1))

        container.content.controls = [btn_back, self.page_num, btn_next]

        return container


    def get_view(self):
        return self.view
