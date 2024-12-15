import flet as ft
from logic import get_option
from logic import get_words


class BaseView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = ft.View()
        self.platform = page.platform.value
        self.appbar = ft.AppBar(
            actions=[
                ft.TextButton(text='Input', on_click=lambda _: page.go('/input')),
                ft.TextButton(text='Dictionary', on_click=lambda _: page.go('/dictionary')),
                ft.TextButton(text='Search', on_click=lambda _: page.go('/search')),
                ft.TextButton(text='Pages', on_click=lambda _: page.go('/pages')),
            ]
        )
        self.view.appbar = self.appbar


    def get_view(self):
        pass


class CreateCard:
    def create_card(self, data: dict):
        def on_click(data):
            self.page.go(
                f'/detail?word={data['word']}&transcription={data['transcription']}&translate={data['translate']}&addition={data['addition']}&word_id={data['id']}')

        card = ft.Card(
            content=ft.Container(
                padding=15,
                border_radius=10,
                bgcolor=ft.colors.GREY,
                shadow=ft.BoxShadow(
                    spread_radius=1, blur_radius=3, color=ft.colors.BLACK12
                ),
                on_click=lambda _: on_click(data)
            ),
            margin=ft.margin.only(top=5, bottom=5),
        )
        contentCard = ft.Column(
            [
                ft.Text(data['word'], weight=ft.FontWeight.BOLD, size=20, color='black'),
                ft.Text(f"[{data['transcription']}]", color="black", size=14),
                ft.Text(f"Перевод: {data['translate']}", size=16, color='black'),
                ft.Divider(),
                ft.Column(
                    [
                        ft.Text(data['addition'], size=14, color="black")
                    ],
                    spacing=5,
                ),
            ],
            spacing=8,
        )

        card.content.content = contentCard

        return card


class ListCards(BaseView, CreateCard):
    def __init__(self, page):
        super().__init__(page)

    def create_l_cards(self, mod, **kwargs):
        l_cards = ft.ListView(
            spacing=10,
            width=self.get_width_for_l_cards(),
            height=self.get_height_for_l_cards(),
        )

        data = get_words(mod, kwargs)

        l_cards.controls = [
            self.create_card(info)
            for info in data
        ]

        return l_cards

    def update_l_cards(self, mod, **kwargs):
        data = get_words(mod, kwargs)

        new_l_cards = [
            self.create_card(info)
            for info in data
        ]

        return new_l_cards

    def update_size(self, *args):
        self.l_cards.width = self.get_width_for_l_cards()
        self.l_cards.height = self.get_height_for_l_cards()
        self.view.update()

    def get_width_for_l_cards(self):
        if self.page.width > 700:
            return self.page.width * get_option('ListCards_interface', self.platform, 'width',
                                                0)  # l_cards определяется в дочерних классах
        else:
            return self.page.width * get_option('ListCards_interface', self.platform, 'width', 1)

    def get_height_for_l_cards(self):
        return self.page.height * get_option('ListCards_interface', self.platform, 'height', 0)