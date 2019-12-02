from app.view_models.book import BookViewModel
from . import web
from app.models.gift import Gift


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return books

