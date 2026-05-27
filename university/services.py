"""
Service layer for career-orientation scoring and Gemini analysis.
"""

import logging
from typing import Dict, List, Optional, Tuple

import environ
from django.conf import settings
from google import genai

logger = logging.getLogger(__name__)
env = environ.Env()


DIRECTION_LABELS = {
    "Axborot texnologiyalari": {
        "uz": "Axborot texnologiyalari",
        "ru": "Информационные технологии",
        "en": "Information Technology",
    },
    "Tibbiyot": {"uz": "Tibbiyot", "ru": "Медицина", "en": "Medicine"},
    "Muhandislik": {"uz": "Muhandislik", "ru": "Инженерия", "en": "Engineering"},
    "Pedagogika": {"uz": "Pedagogika", "ru": "Педагогика", "en": "Education"},
    "Huquqshunoslik": {"uz": "Huquqshunoslik", "ru": "Юриспруденция", "en": "Law"},
    "Iqtisodiyot": {"uz": "Iqtisodiyot", "ru": "Экономика", "en": "Economics"},
    "San'at": {"uz": "San'at", "ru": "Искусство", "en": "Arts"},
    "Gumanitar fanlar": {
        "uz": "Gumanitar fanlar",
        "ru": "Гуманитарные науки",
        "en": "Humanities",
    },
}


SECTION_TITLES = {
    "uz": [
        "Shaxsiyat va kuchli tomonlar tahlili",
        "Tavsiya etilgan kasbiy yo'nalishlar",
        "O'zbekistondagi universitet mutaxassisliklari",
        "Universitetga tayyorgarlik yo'l xaritasi",
        "Harakat rejasi",
        "Motivatsion xulosa",
    ],
    "ru": [
        "Анализ личности и сильных сторон",
        "Рекомендуемые карьерные направления",
        "Специальности в университетах Узбекистана",
        "Дорожная карта подготовки к университету",
        "План действий",
        "Мотивационное резюме",
    ],
    "en": [
        "Personality & Strength Analysis",
        "Recommended Career Directions",
        "Recommended University Majors in Uzbekistan",
        "University Preparation Roadmap",
        "Action Plan",
        "Motivation Summary",
    ],
}


class GeminiAIService:
    """Gemini integration with language-aware prompts and graceful fallback."""

    LANGUAGE_NAMES = {"uz": "Uzbek", "ru": "Russian", "en": "English"}

    def __init__(self):
        self.api_key = getattr(settings, "GEMINI_API_KEY", "") or env("GEMINI_API_KEY", default="")
        self.model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as exc:
                logger.error("Failed to initialize Gemini client: %s", exc)
        else:
            logger.warning("GEMINI_API_KEY is not set. Local fallback will be used.")

    def is_configured(self) -> bool:
        return self.client is not None

    def _localized_direction(self, direction: str, language: str) -> str:
        return DIRECTION_LABELS.get(direction, {}).get(language, direction)

    def _format_scores(self, score_data: Dict, language: str) -> str:
        if not score_data:
            return "- No data"

        label = {"uz": "ball", "ru": "балл", "en": "points"}.get(language, "points")
        lines = []
        for field, score in sorted(score_data.items(), key=lambda item: item[1], reverse=True):
            name = self._localized_direction(str(field), language)
            value = int(score) if isinstance(score, (int, float)) else 0
            lines.append(f"- {name}: {value} {label}")
        return "\n".join(lines)

    def _build_prompt(self, score_data: Dict[str, float], language: str) -> str:
        language = language if language in SECTION_TITLES else "uz"
        titles = SECTION_TITLES[language]
        language_name = self.LANGUAGE_NAMES[language]
        scores_text = self._format_scores(score_data, language)

        return f"""
You are a professional career counselor and educational advisor for students in Uzbekistan.
Respond only in {language_name}.

The student completed a career-orientation test. Scores:
{scores_text}

Return clean Markdown. Keep paragraphs short. Prefer bullets. Make it easy to read on a mobile phone.
Do not add extra sections. Use exactly these headings:

## 1. {titles[0]}
- Strongest abilities
- Natural talents
- Behavioral tendencies
- Learning style

## 2. {titles[1]}
- Most suitable fields
- Why these fields match the student
- Future growth potential

## 3. {titles[2]}
- Suggest relevant university majors available or common in Uzbekistan
- Include examples such as Software Engineering, AI & Data Science, Economics, Medicine, Law, Architecture, Business, Cybersecurity, Marketing, Finance, International Relations when relevant

## 4. {titles[3]}
- Subjects to focus on
- Science or humanities priorities
- Recommended preparation level
- Preparation strategy
- Self-study recommendations

## 5. {titles[4]}
- What to learn first
- Skills to improve
- Online resources that may help
- Recommended habits

## 6. {titles[5]}
End with one short motivational paragraph.
""".strip()

    def analyze_test_results(
        self,
        score_data: Dict[str, float],
        language: str = "uz",
        timeout: Optional[int] = None,
    ) -> Tuple[bool, str]:
        if language not in SECTION_TITLES:
            language = "uz"

        if not self.is_configured():
            return True, self.build_local_recommendation(score_data, language)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=self._build_prompt(score_data, language),
            )
            if response and response.text:
                return True, response.text
            return True, self.build_local_recommendation(score_data, language)
        except Exception as exc:
            logger.error("Gemini API error: %s", exc, exc_info=True)
            return True, self.build_local_recommendation(score_data, language)

    def build_local_recommendation(self, score_data: Dict[str, float], language: str = "uz") -> str:
        """Readable fallback for development or temporary Gemini outages."""
        language = language if language in SECTION_TITLES else "uz"
        titles = SECTION_TITLES[language]
        top = sorted(score_data.items(), key=lambda item: item[1], reverse=True)[:3]
        top_labels = [self._localized_direction(name, language) for name, _ in top] or ["IT"]
        primary = top_labels[0]

        text = {
            "uz": [
                f"Sizning javoblaringiz {primary} yo'nalishiga kuchli moyillik borligini ko'rsatadi.",
                "Mantiqiy fikrlash, muammoni tahlil qilish va aniq maqsad bilan ishlash siz uchun foydali ustunlik bo'ladi.",
                "Mos yo'nalishlar: " + ", ".join(top_labels) + ". Bu sohalar qiziqishlaringiz va qaror qabul qilish uslubingizga yaqin.",
                "Dasturiy ta'minot muhandisligi, AI va Data Science, iqtisodiyot, moliya, biznes boshqaruvi yoki kiberxavfsizlik kabi yo'nalishlarni ko'rib chiqing.",
                "Matematika, ingliz tili, informatika va tanlangan yo'nalishga mos fanlarga e'tibor bering. Haftalik reja tuzib, test va amaliy topshiriqlar bilan mustahkamlang.",
                "Avval asosiy fanlarni tartibga soling, keyin kichik loyihalar qiling, onlayn kurslardan foydalaning va har kuni kamida 60-90 daqiqa muntazam o'qing.",
                "Sizda rivojlanish uchun yaxshi poydevor bor. Izchil harakat qilsangiz, tanlagan yo'nalishingizda kuchli natijaga chiqasiz.",
            ],
            "ru": [
                f"Ваши ответы показывают сильную склонность к направлению: {primary}.",
                "Логическое мышление, анализ задач и умение работать с четкой целью станут вашими сильными сторонами.",
                "Подходящие направления: " + ", ".join(top_labels) + ". Они хорошо совпадают с вашими интересами и стилем решений.",
                "Рассмотрите специальности: Software Engineering, AI & Data Science, экономика, финансы, бизнес, кибербезопасность или международные отношения.",
                "Сфокусируйтесь на математике, английском языке, информатике и профильных предметах. Готовьтесь по недельному плану и закрепляйте знания практикой.",
                "Сначала укрепите базовые предметы, затем делайте небольшие проекты, используйте онлайн-курсы и занимайтесь регулярно по 60-90 минут в день.",
                "У вас есть хорошая основа для роста. Последовательность и дисциплина помогут выйти на сильный результат.",
            ],
            "en": [
                f"Your answers show a strong fit for {primary}.",
                "Logical thinking, problem analysis, and focused work can become your strongest advantages.",
                "Suitable directions: " + ", ".join(top_labels) + ". These fields match your interests and decision-making style.",
                "Consider majors such as Software Engineering, AI & Data Science, Economics, Finance, Business, Cybersecurity, or International Relations.",
                "Focus on mathematics, English, computer science, and subjects required by your chosen field. Use a weekly plan and practice with tests and projects.",
                "Start with core subjects, then build small projects, use online courses, and study consistently for 60-90 minutes every day.",
                "You already have a strong starting point. With steady effort, you can build a confident path toward your future profession.",
            ],
        }[language]

        return "\n\n".join(
            [
                f"## 1. {titles[0]}\n- {text[0]}\n- {text[1]}",
                f"## 2. {titles[1]}\n- {text[2]}",
                f"## 3. {titles[2]}\n- {text[3]}",
                f"## 4. {titles[3]}\n- {text[4]}",
                f"## 5. {titles[4]}\n- {text[5]}",
                f"## 6. {titles[5]}\n{text[6]}",
            ]
        )


class TestAnalysisService:
    """Service for test analysis and scoring."""

    @staticmethod
    def calculate_scores(answers: Dict[int, int], options_data: List[Dict]) -> Dict[str, int]:
        scores = {}
        for _, option_id in answers.items():
            for option in options_data:
                if option.get("id") == option_id:
                    direction = option.get("direction", "Unknown")
                    score = option.get("score", 1)
                    scores[direction] = scores.get(direction, 0) + score
                    break
        return scores

    @staticmethod
    def format_scores_for_display(scores: Dict[str, int], language: str = "uz") -> List[Dict]:
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [
            {
                "rank": rank,
                "direction": DIRECTION_LABELS.get(direction, {}).get(language, direction),
                "score": score,
                "percentage": min(int((score / 20) * 100), 100) if score else 0,
            }
            for rank, (direction, score) in enumerate(sorted_scores, 1)
        ]
