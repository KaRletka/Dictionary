import flet as ft
from logic import upload_main_db, download_main_db
from views import InputView, RandomCardsView, StructuredCardsView, SearchView, EditView

def open_app():
    download_main_db()


def main(page: ft.Page):
    inp_view = InputView(page)
    ran_words_view = RandomCardsView(page)  # random words view
    str_words_view = StructuredCardsView(page)  # structured words view
    search_view = SearchView(page)
    edit_view = EditView(
        page,
        {
            'word_id': 0,
            'word': '',
            'transcription': '',
            'translate': '',
            'addition': '',
        }
    )

    def close_app():
        page.window.visible = False
        page.update()
        upload_main_db()
        page.window.destroy()

    def plug(*args, **kwargs):
        pass

    resize_func = {
        '/input': inp_view.update_size,
        '/dictionary': ran_words_view.update_size,
        '/pages': str_words_view.update_size,
        '/search': search_view.update_size,
        '/detail': edit_view.update_size,
        '/close': plug,
    }

    def window_event_handler(e):
        if e.data == 'close':
            close_app()

    def route_change(route):
        page.views.clear()
        if page.route == '/input':
            page.views.append(inp_view.get_view())
        elif page.route == '/dictionary':
            page.views.append(ran_words_view.get_view())
            ran_words_view.l_cards.controls = ran_words_view.update_l_cards('random', size=15)
        elif page.route == '/pages':
            page.views.append(str_words_view.get_view())
            str_words_view.l_cards.controls = str_words_view.update_l_cards('pagination', size=15, page=1)
        elif page.route == '/search':
            page.views.append(search_view.get_view())
        elif page.route.startswith('/detail'):
            query_params = page.query.to_dict
            edit_view.set_info(query_params)
            page.views.append(edit_view.get_view())
        elif page.route == '/close':
            close_app()
        page.update()
        resized()

    def resized(*args, **kwargs):
        for key in resize_func:
            if page.route.startswith(key):
                resize_func[key]()
                return
        print(f"No resize function found for route: {page.route}")

    page.on_route_change = route_change
    page.on_resized = resized
    page.window.prevent_close = True
    page.window.on_event = window_event_handler
    page.go('/input')


open_app()

ft.app(main)
