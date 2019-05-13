import json
import Locale
from Logger import Logger


class Schedule:
    def get_schedule_weekly(self, group):
        table = Schedule._get_schedule(group)
        if group not in table:
            return None

        table = table[group]
        result = Locale.TEXT_SCHEDULE_HEAD.format(group)
        for row in table:
            result += '[' + Locale.DAYS_OF_WEEK[row['day']] + '] ' + row['type'] + ' ' + row['name'] + '\n'

        return result

    def find_alike_groups(self, possible_group):
        table = self._get_schedule()
        result = Locale.TEXT_ALIKE_GROUPS_HEAD.format(possible_group)
        count = 0
        for group in table:
            if possible_group in group or possible_group.upper() in group:
                result += group + '\n'
                count += 1
        if count == 0:
            result = Locale.TEXT_ALIKE_GROUPS_NO_FOUND.format(possible_group)
        return {'text': result, 'count': count}

    def _get_schedule(self):
        with open('schedule.json', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)['timetable']
                return data
            except Exception as ex:
                Logger.error('Exception while reading schedule.json', ex)
                return None
