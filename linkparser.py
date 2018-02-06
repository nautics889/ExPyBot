from html.parser import HTMLParser
from urllib.request import urlopen

class LinkHTMLParser(HTMLParser):
    def __init__(self, site_name, *args, **kwargs):
        # список ссылок
        self.links = []
        # имя сайта
        self.site_name = site_name
        # вызываем __init__ родителя
        super().__init__(*args, **kwargs)
        # при инициализации "скармливаем" парсеру содержимое страницы
        self.feed(self.read_site_content())
        # записываем список ссылок в файл

    def handle_starttag(self, tag, attrs):
        # проверяем является ли тэг тэгом ссылки
        if tag == 'a':
            # находим аттрибут адреса ссылки
            for attr in attrs:
                if attr[0] == 'href':
                    # проверяем эту ссылку методом validate() (мы его еще напишем)
                    if not self.validate(attr[0]):
                        # вставляем адрес в список ссылок
                        if self.validate_link(attr[1]):
                            self.links.append(attr[1])

    def validate(self, link):
        """ Функция проверяет стоит ли добавлять ссылку в список адресов.
        В список адресов стоит добавлять если ссылка:
             1) Еще не в списке ссылок
             2) Не вызывает javascript-код
             3) Не ведет к какой-либо метке. (Не содержит #)
         """
        if link[0]=='/':
            return True
        return link in self.links or '#' in link or 'javascript:' in link

    def validate_link(self, link):
        if link[:4]=='http':
            return True
        else:
            False

    def read_site_content(self):
        return str(urlopen(self.site_name).read())

    def get_links(self):
        return '\n'.join(sorted(self.links))


    def __del__(self):
        pass