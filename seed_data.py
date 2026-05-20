import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from university.models import Region, University, AdditionalResource

def seed_data():
    # 1. Add 5 Regions
    regions_data = [
        {"name_uz": "Toshkent shahri", "name_ru": "Город Ташкент", "name_en": "Tashkent City"},
        {"name_uz": "Samarqand viloyati", "name_ru": "Самаркандская область", "name_en": "Samarkand Region"},
        {"name_uz": "Buxoro viloyati", "name_ru": "Бухарская область", "name_en": "Bukhara Region"},
        {"name_uz": "Farg'ona viloyati", "name_ru": "Ферганская область", "name_en": "Fergana Region"},
        {"name_uz": "Xorazm viloyati", "name_ru": "Хорезмская область", "name_en": "Khorezm Region"},
    ]

    regions = []
    for r_data in regions_data:
        region, created = Region.objects.get_or_create(
            name_en=r_data['name_en'],
            defaults={
                'name_uz': r_data['name_uz'],
                'name_ru': r_data['name_ru'],
            }
        )
        regions.append(region)
        print(f"Region added/exists: {region.name_uz}")

    # 2. Add 5 Universities
    universities_data = [
        {
            "region": regions[0],
            "name_uz": "O'zbekiston Milliy Universiteti",
            "name_ru": "Национальный университет Узбекистана",
            "name_en": "National University of Uzbekistan",
            "postal_address_uz": "Toshkent shahri, Universitet ko'chasi 4",
            "postal_address_ru": "город Ташкент, улица Университетская 4",
            "postal_address_en": "Tashkent city, University street 4",
            "phone_number": "+998 71 246 02 24",
            "email": "info@nuu.uz",
            "website": "https://nuu.uz",
            "latitude": 41.3468,
            "longitude": 69.2066
        },
        {
            "region": regions[1],
            "name_uz": "Samarqand Davlat Universiteti",
            "name_ru": "Самаркандский государственный университет",
            "name_en": "Samarkand State University",
            "postal_address_uz": "Samarqand shahri, Universitet xiyoboni 15",
            "postal_address_ru": "город Самарканд, Университетский бульвар 15",
            "postal_address_en": "Samarkand city, University boulevard 15",
            "phone_number": "+998 66 239 11 40",
            "email": "devonxona@samdu.uz",
            "website": "https://samdu.uz",
            "latitude": 39.6465,
            "longitude": 66.9602
        },
        {
            "region": regions[2],
            "name_uz": "Buxoro Davlat Universiteti",
            "name_ru": "Бухарский государственный университет",
            "name_en": "Bukhara State University",
            "postal_address_uz": "Buxoro shahri, M.Iqbol ko'chasi 11",
            "postal_address_ru": "город Бухара, улица М.Икбола 11",
            "postal_address_en": "Bukhara city, M.Iqbol street 11",
            "phone_number": "+998 65 221 29 14",
            "email": "info@buxdu.uz",
            "website": "https://buxdu.uz",
            "latitude": 39.7747,
            "longitude": 64.4286
        },
        {
            "region": regions[3],
            "name_uz": "Farg'ona Davlat Universiteti",
            "name_ru": "Ферганский государственный университет",
            "name_en": "Fergana State University",
            "postal_address_uz": "Farg'ona shahri, Murabbiylar ko'chasi 19",
            "postal_address_ru": "город Фергана, улица Мураббийлар 19",
            "postal_address_en": "Fergana city, Murabbiylar street 19",
            "phone_number": "+998 73 244 44 02",
            "email": "fdu@fdu.uz",
            "website": "https://fdu.uz",
            "latitude": 40.3864,
            "longitude": 71.7828
        },
        {
            "region": regions[4],
            "name_uz": "Urganch Davlat Universiteti",
            "name_ru": "Ургенчский государственный университет",
            "name_en": "Urgench State University",
            "postal_address_uz": "Urganch shahri, Hamid Olimjon ko'chasi 14",
            "postal_address_ru": "город Ургенч, улица Хамида Алимджана 14",
            "postal_address_en": "Urgench city, Hamid Olimjon street 14",
            "phone_number": "+998 62 224 67 00",
            "email": "info@urdu.uz",
            "website": "https://urdu.uz",
            "latitude": 41.5501,
            "longitude": 60.6300
        }
    ]

    for u_data in universities_data:
        uni, created = University.objects.get_or_create(
            name_en=u_data['name_en'],
            defaults=u_data
        )
        print(f"University added/exists: {uni.name_uz}")

    # 3. Add 5 Resources
    resources_data = [
        {
            "title_uz": "Oliy ta'lim, fan va innovatsiyalar vazirligi",
            "title_ru": "Министерство высшего образования, науки и инноваций",
            "title_en": "Ministry of Higher Education, Science and Innovations",
            "description_uz": "O'zbekiston Respublikasi Oliy ta'lim muassasalari haqida rasmiy ma'lumotlar portal",
            "description_ru": "Официальный портал информации о высших учебных заведениях Республики Узбекистан",
            "description_en": "Official information portal about higher educational institutions of the Republic of Uzbekistan",
            "url": "https://edu.uz",
            "icon_class": "fas fa-university"
        },
        {
            "title_uz": "Bilim va malakalarni baholash agentligi (UzBMB)",
            "title_ru": "Агентство по оценке знаний и квалификаций (UzBMB)",
            "title_en": "Knowledge and Skills Assessment Agency (UzBMB)",
            "description_uz": "Oliy ta'lim muassasalariga qabul test sinovlari haqida ma'lumot",
            "description_ru": "Информация о вступительных тестовых испытаниях в высшие учебные заведения",
            "description_en": "Information about admission test exams to higher educational institutions",
            "url": "https://uzbmb.uz",
            "icon_class": "fas fa-clipboard-check"
        },
        {
            "title_uz": "Lex.uz - Qonunchilik ma'lumotlari milliy bazasi",
            "title_ru": "Lex.uz - Национальная база данных законодательства",
            "title_en": "Lex.uz - National Database of Legislation",
            "description_uz": "Ta'limga oid barcha qonun hujjatlari va qarorlar",
            "description_ru": "Все законодательные акты и постановления, касающиеся образования",
            "description_en": "All legislative acts and resolutions related to education",
            "url": "https://lex.uz",
            "icon_class": "fas fa-gavel"
        },
        {
            "title_uz": "ZiyoNET ta'lim tarmog'i",
            "title_ru": "Образовательная сеть ZiyoNET",
            "title_en": "ZiyoNET Educational Network",
            "description_uz": "Yoshlar va talabalar uchun yagona axborot-ta'lim tarmog'i",
            "description_ru": "Единая информационно-образовательная сеть для молодежи и студентов",
            "description_en": "Unified educational and informational network for youth and students",
            "url": "https://ziyonet.uz",
            "icon_class": "fas fa-book-open"
        },
        {
            "title_uz": "Yagona interaktiv davlat xizmatlari portali (my.gov.uz)",
            "title_ru": "Единый портал интерактивных государственных услуг (my.gov.uz)",
            "title_en": "Single Portal of Interactive State Services (my.gov.uz)",
            "description_uz": "Abituriyentlar uchun hujjat topshirish va boshqa davlat xizmatlari",
            "description_ru": "Подача документов для абитуриентов и другие государственные услуги",
            "description_en": "Document submission for applicants and other public services",
            "url": "https://my.gov.uz",
            "icon_class": "fas fa-laptop-house"
        }
    ]

    for res_data in resources_data:
        res, created = AdditionalResource.objects.get_or_create(
            url=res_data['url'],
            defaults=res_data
        )
        print(f"Resource added/exists: {res.title_uz}")

if __name__ == '__main__':
    seed_data()
