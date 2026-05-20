import os
import polib

translations = {
    "Universitetlar ro‘yxati": {"ru": "Список университетов", "en": "List of Universities"},
    "Universitetlar": {"ru": "Университеты", "en": "Universities"},
    "Viloyat bo‘yicha filtrlash va tezkor qidiruv.": {"ru": "Фильтрация по регионам и быстрый поиск.", "en": "Filter by region and quick search."},
    "Qidirish (nom, email, sayt, manzil)": {"ru": "Поиск (имя, email, сайт, адрес)", "en": "Search (name, email, site, address)"},
    "Qidirish": {"ru": "Поиск", "en": "Search"},
    "Natija topilmadi": {"ru": "Результатов не найдено", "en": "No results found"},
    "Qidiruv yoki filterni o‘zgartirib ko‘ring.": {"ru": "Попробуйте изменить поиск или фильтр.", "en": "Try changing your search or filter."},
    "Oldingi": {"ru": "Предыдущий", "en": "Previous"},
    "Keyingi": {"ru": "Следующий", "en": "Next"},
    "Sahifa": {"ru": "Страница", "en": "Page"},
    "Barchasi": {"ru": "Все", "en": "All"},
    "Manbalar": {"ru": "Ресурсы", "en": "Resources"},
    "Qo‘shimcha manbalar": {"ru": "Дополнительные ресурсы", "en": "Additional Resources"},
    "O‘zbekistondagi universitetlar va ta'lim tizimi haqida foydali havolalar.": {"ru": "Полезные ссылки об университетах и системе образования в Узбекистане.", "en": "Useful links about universities and the education system in Uzbekistan."},
    "Manbalar mavjud emas": {"ru": "Ресурсов нет", "en": "No resources available"},
    "Tez orada bu yerda foydali havolalar paydo bo'ladi.": {"ru": "Скоро здесь появятся полезные ссылки.", "en": "Useful links will appear here soon."},
    "O'tish": {"ru": "Перейти", "en": "Go"},
    "Tafsilot": {"ru": "Детали", "en": "Details"},
    "Universitet": {"ru": "Университет", "en": "University"},
    "Joylashuv": {"ru": "Расположение", "en": "Location"},
    "Xaritada universitet": {"ru": "Университет на карте", "en": "University on the map"},
    "Orqaga": {"ru": "Назад", "en": "Back"},
    "O'zbekistonning eng yaxshi universitetlari": {"ru": "Лучшие университеты Узбекистана", "en": "Best universities in Uzbekistan"},
    "Kelajagingiz uchun eng to'g'ri tanlovni biz bilan qiling. Minglab imkoniyatlar, barcha Oliy ta'lim muassasalari bir joyda.": {"ru": "Сделайте правильный выбор для своего будущего с нами. Тысячи возможностей, все высшие учебные заведения в одном месте.", "en": "Make the right choice for your future with us. Thousands of opportunities, all higher education institutions in one place."},
    "Universitetlarni izlash": {"ru": "Поиск университетов", "en": "Search universities"},
    "Xaritada ko'rish": {"ru": "Посмотреть на карте", "en": "View on map"},
    "Hududlar": {"ru": "Регионы", "en": "Regions"}
}

def update_po_file(lang):
    po_path = os.path.join('locale', lang, 'LC_MESSAGES', 'django.po')
    if os.path.exists(po_path):
        po = polib.pofile(po_path)
        existing_msgids = [entry.msgid for entry in po]
        
        for msgid, trans_dict in translations.items():
            if msgid not in existing_msgids:
                entry = polib.POEntry(
                    msgid=msgid,
                    msgstr=trans_dict.get(lang, msgid)
                )
                po.append(entry)
            else:
                for entry in po:
                    if entry.msgid == msgid and not entry.msgstr:
                        entry.msgstr = trans_dict.get(lang, msgid)
        
        po.save()
        po.save_as_mofile(po_path[:-3] + '.mo')
        print(f"Updated and compiled {lang} translations.")
    else:
        print(f"PO file not found for {lang}")

update_po_file('ru')
update_po_file('en')
