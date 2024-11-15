import aiohttp
import re
from bs4 import BeautifulSoup
from data import load_user_group


async def get_schedule(user_id):
    group = await load_user_group(user_id)
    if not group:
        return None

    url = "https://timetable.vsuet.ru/index.php"
    payload = {"select_group": group}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            if response.status == 200:
                html_content = await response.text()
                return parse_schedule(html_content)
            else:
                print("Ошибка при получении расписания:", response.status)
                return None


def parse_schedule(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    tables = soup.find_all('table', {'class': 'table table-hover table-bordered table-sm'})

    schedule = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['th', 'td'])
            if cols:
                day = cols[0].get_text(strip=True).capitalize()
                time = cols[1].get_text(strip=True)
                week_type = cols[2].get_text(strip=True).lower()
                raw_details = cols[3]

                details_text = raw_details.get_text(strip=True, separator=' ')
                if details_text.lower().startswith('практические занятия:'):
                    details_text = details_text[len('практические занятия:'):].strip()

                lecturer_tag = raw_details.find('a')
                lecturer = lecturer_tag.get_text(strip=True) if lecturer_tag else ''

                room_match = re.search(r'\(а\.\d+\)', details_text)
                room = room_match.group(0) if room_match else ''

                lesson_name = details_text
                if lecturer:
                    lesson_name = lesson_name.replace(lecturer, '').strip()
                if room:
                    lesson_name = lesson_name.replace(room, '').strip()
                lesson_name = re.sub(r',\s*гр\.\S+$', '', lesson_name).strip()

                additional_details = ', '.join(filter(None, [lecturer, room]))

                schedule.append({
                    'day': day,
                    'time': time,
                    'week_type': week_type,
                    'lesson_name': lesson_name,
                    'details': additional_details
                })
    return schedule


async def check_group_exists(group):
    url = "https://timetable.vsuet.ru/index.php"
    payload = {"select_group": group}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                error_message = soup.find('table', class_='table table-hover table-bordered table-sm mb-0')
                if error_message and "Данные не найдены! Попробуйте с другими параметрами..." in error_message.get_text():
                    return False
                return True
            return False, f"Невозможно получить данные с сайта. Код ответа: {response.status}"
