from constants import TESTS


class LessonException(Exception):
    pass


class AttendException(Exception):
    pass


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals.get('lesson')
    pupil_attendance = intervals.get('pupil')
    tutor_attendance = intervals.get('tutor')

    # Проверка на корректность данных времени урока
    if not len(intervals.get('lesson')) > 0 or intervals.get('lesson')[0] >= intervals.get('lesson')[1]:
        raise LessonException('Не верно задано время урока!')
    # Проверка на наличие данных посещения урока
    if not len(intervals.get('pupil')) > 0 or not len(intervals.get('tutor')) > 0:
        raise AttendException('Не задано время посещений учителя или ученика')
    # Проверка на корректность данных посещения урока
    if len(pupil_attendance) % 2 != 0 or len(pupil_attendance) % 2 != 0:
        raise AttendException('Время посещений учителя или ученика задано не верно')

    def merge_intervals(inters: list[int]) -> list[int]:
        """Объединение пересекающихся интервалов посещения урока"""
        intervals = []
        for i in range(0, len(inters), 2):
            start = inters[i]
            end = inters[i + 1]
            intervals.append((start, end))

        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        result = [sorted_intervals[0]]
        for current in sorted_intervals[1:]:
            last = result[-1]
            if current[0] <= last[1]:

                new_start = last[0]
                new_end = max(last[1], current[1])
                result[-1] = (new_start, new_end)
            else:
                result.append(current)

        return [x for tup in result for x in tup]

    # Время посещения уроков после объединения интервалов
    merged_pupil_attendance = merge_intervals(pupil_attendance)
    merged_tutor_attendance = merge_intervals(tutor_attendance)

    def filter_intervals(inters: list[int], lesson_start: int, lesson_end: int) -> list[int]:
        """Проверка на вхождения времени посещения уроков во время урока"""
        result = list()
        for i in range(0, len(inters), 2):
            start = max(inters[i], lesson_start)
            end = min(inters[i + 1], lesson_end)
            if start < end:
                result.extend([start, end])
        return result

    # Время посещения уроков после корректировки (проверки на корректность)
    clear_pupil_attendance = filter_intervals(merged_pupil_attendance, lesson_start, lesson_end)
    clear_tutor_attendance = filter_intervals(merged_tutor_attendance, lesson_start, lesson_end)

    def determine_attendance(inter1: list[int], inter2: list) -> list[int]:
        """Нахождение общих пересечений интервалов для ученика и учителя"""
        result = list()
        for i in range(0, len(inter1), 2):
            for j in range(0, len(inter2), 2):
                start = max(inter1[i], inter2[j])
                end = min(inter1[i + 1], inter2[j + 1])
                if end > start:
                    result.extend([start, end])

        return result

    final_attendance = determine_attendance(clear_pupil_attendance, clear_tutor_attendance)

    def calculate_attendance(inter: list[int]) -> int:
        """Подсчет времени общих интервалов"""
        result = 0
        for i in range(0, len(inter), 2):
            result += (inter[i + 1] - inter[i])
        return result

    result = calculate_attendance(final_attendance)
    return result



