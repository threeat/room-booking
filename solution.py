# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN_HOUR = 9
CLOSE_HOUR = 21
MAX_HOURS = 3
MAX_PER_DAY = 2


def _is_int(value):
    # bool은 int의 하위 클래스라서 따로 걸러낸다
    return isinstance(value, int) and not isinstance(value, bool)


def _is_valid_place(room, day):
    # 튜플 비교(==)를 써서 리스트처럼 해시가 안 되는 값이 와도 에러 없이 False
    try:
        return room in ROOMS and day in DAYS
    except Exception:
        return False


def _is_valid_name(name):
    # 빈 이름·띄어쓰기만 있는 이름·글자가 아닌 이름은 거절
    return isinstance(name, str) and name.strip() != ""


class RoomBooking:
    def __init__(self):
        # (room, day) -> [(start, end, name), ...]
        self._bookings = {}

    def book(self, room, day, start, end, name):
        if not _is_valid_place(room, day):
            return False
        if not _is_valid_name(name):
            return False
        if not _is_int(start) or not _is_int(end):
            return False
        if start < OPEN_HOUR or end > CLOSE_HOUR:
            return False
        if start >= end:
            return False
        if end - start > MAX_HOURS:
            return False

        slots = self._bookings.get((room, day), [])
        for s, e, _ in slots:
            if start < e and s < end:
                return False

        count = 0
        for (_, d), items in self._bookings.items():
            if d == day:
                count += sum(1 for _, _, n in items if n == name)
        if count >= MAX_PER_DAY:
            return False

        self._bookings.setdefault((room, day), []).append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if not _is_valid_place(room, day):
            return False
        if not _is_int(start):
            return False
        slots = self._bookings.get((room, day), [])
        for i, (s, _, n) in enumerate(slots):
            if s == start:
                if n != name:
                    return False
                del slots[i]
                return True
        return False

    def get_schedule(self, room, day):
        if not _is_valid_place(room, day):
            return []
        return sorted(self._bookings.get((room, day), []), key=lambda b: b[0])
