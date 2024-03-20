


class MenuItem:
    def __init__(self, text, url):
        self.text = text
        self.url = url
        self.css_class = 'link-body-emphasis'
class Menu:
    def __init__(self, items):
        self.items = [MenuItem(item['text'], item['url']) for item in items]
        self.active = items[0].url
        self.set_active_item(items[0].url)

    def set_active_item(self, url):
        for item in self.items:
            item.css_class = 'active' if item.url == url else 'link-body-emphasis'
        self.active=url

upper_menu = [
    {"text": "Home", "url": "#"},
    {"text": "Features", "url": "#"},
    {"text": "Pricing", "url": "#"},
    {"text": "FAQs", "url": "#"},
    {"text": "About", "url": "#"}
]

sidebar_menu = [
    {"text": "Teachers", "url": "/teachers"},
    {"text": "Dashboard", "url": "/teachers/create"},
    {"text": "Orders", "url": "/teachers/1/update"},
    {"text": "Products", "url": "/teachers/1/delete"},
    {"text": "Customers", "url": "/teachers/1/read"}
]

for item in upper_menu:
    item['class'] = 'link-body-emphasis'