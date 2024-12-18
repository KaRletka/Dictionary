import flet as ft
from views.logic import upload_main_db, download_main_db
from views import InputView, RandomCardsView, StructuredCardsView, SearchView, EditView


def open_app():  # downloading data before launching the application
    download_main_db()


def main(page: ft.Page):
    # creating application page objects, when calling get_view, returns an object of type flet.View
    inp_view = InputView(page)
    ran_words_view = RandomCardsView(page)
    str_words_view = StructuredCardsView(page)
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

    def upload_db():
        upload_main_db()

    def plug(*args, **kwargs):
        pass

    # Functions for adjusting window sizes are stored here
    resize_func = {
        '/input': inp_view.update_size,
        '/dictionary': ran_words_view.update_size,
        '/pages': str_words_view.update_size,
        '/search': search_view.update_size,
        '/detail': edit_view.update_size,
        '/upload': plug,
    }

    def route_change(route):
        page.views.clear()
        if page.route == '/input':
            page.views.append(inp_view.get_view())
        elif page.route == '/dictionary':
            page.views.append(ran_words_view.get_view())
            ran_words_view.l_cards.controls = ran_words_view.update_l_cards('random', size=15)
            # It is used for cases when a word has been added/deleted/changed.
            # In the future, I will figure out how to get rid of this code.
        elif page.route == '/pages':
            page.views.append(str_words_view.get_view())
            str_words_view.l_cards.controls = str_words_view.update_l_cards('pagination', size=15, page=1)
            # It is used for cases when a word has been added/deleted/changed.
            # In the future, I will figure out how to get rid of this code.
        elif page.route == '/search':
            page.views.append(search_view.get_view())
        elif page.route.startswith('/detail'):
            query_params = page.query.to_dict
            edit_view.set_info(query_params)
            page.views.append(edit_view.get_view())
        elif page.route == '/upload':
            upload_db()
            page.views.append(inp_view.get_view())
        page.update()
        resized()

    def resized(*args, **kwargs):
        nonlocal resize_func
        for key in resize_func:
            if page.route.startswith(key):
                resize_func[key]()
                return
        print(f"No resize function found for route: {page.route}")

    page.on_route_change = route_change
    page.on_resized = resized
    page.go('/input')


open_app()

ft.app(main)
