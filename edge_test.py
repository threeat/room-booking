"""문제지 규칙 + 확인표 + 경계값 자체 검증 (python edge_test.py)"""
import time
from solution import RoomBooking

fails = 0
def t(label, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"[{'통과' if ok else '실패'}] {label}: {got!r}" + ("" if ok else f" (정답 {want!r})"))

# 문제지 예시
rb = RoomBooking()
t("예시 book", rb.book("A101", "월", 10, 12, "김철수"), True)
t("예시 겹침", rb.book("A101", "월", 11, 13, "이영희"), False)
t("예시 이어붙이기", rb.book("A101", "월", 12, 14, "이영희"), True)
t("예시 시간표", rb.get_schedule("A101", "월"), [(10, 12, "김철수"), (12, 14, "이영희")])
t("예시 남의 취소", rb.cancel("A101", "월", 10, "이영희"), False)
t("예시 본인 취소", rb.cancel("A101", "월", 10, "김철수"), True)

# 확인표 10줄
rb = RoomBooking()
t("확인1", rb.book("A102", "화", 13, 15, "김민수"), True)
t("확인2", rb.book("A102", "화", 14, 16, "박지은"), False)
t("확인3", rb.book("A102", "화", 15, 16, "박지은"), True)
t("확인4", rb.book("A102", "일", 10, 11, "박지은"), False)
t("확인5", rb.book("A102", "수", 19, 22, "박지은"), False)
t("확인6", rb.book("A102", "수", 9, 13, "박지은"), False)
t("확인7a", rb.book("B201", "화", 9, 10, "김민수"), True)
t("확인7b", rb.book("A101", "화", 16, 17, "김민수"), False)
t("확인8", rb.cancel("A102", "화", 13, "박지은"), False)
t("확인9", rb.cancel("A102", "화", 13, "김민수"), True)
t("확인10", rb.get_schedule("A102", "화"), [(15, 16, "박지은")])

# 경계값·예외
rb = RoomBooking()
t("없는 강의실", rb.book("C999", "월", 10, 11, "a"), False)
t("소문자 강의실", rb.book("a101", "월", 10, 11, "a"), False)
t("영문 요일", rb.book("A101", "Mon", 10, 11, "a"), False)
t("None 강의실", rb.book(None, "월", 10, 11, "a"), False)
t("리스트 강의실(해시 불가)", rb.book(["A101"], "월", 10, 11, "a"), False)
t("소수 시작", rb.book("A101", "월", 10.5, 12, "a"), False)
t("10.0 실수", rb.book("A101", "월", 10.0, 12, "a"), False)
t("문자열 시각", rb.book("A101", "월", "10", "12", "a"), False)
t("True/False", rb.book("A101", "월", True, 2, "a"), False)
t("end=True", rb.book("A101", "월", 9, True, "a"), False)
t("None 시각", rb.book("A101", "월", None, 12, "a"), False)
t("시작=끝", rb.book("A101", "월", 10, 10, "a"), False)
t("시작>끝", rb.book("A101", "월", 12, 10, "a"), False)
t("9시 이전", rb.book("A101", "월", 8, 10, "a"), False)
t("음수", rb.book("A101", "월", -1, 1, "a"), False)
t("21시 초과", rb.book("A101", "월", 20, 22, "a"), False)
t("9시 시작 경계", rb.book("A101", "월", 9, 12, "a"), True)   # 정확히 3시간
t("21시 종료 경계", rb.book("A101", "월", 18, 21, "b"), True)
t("4시간", rb.book("A102", "월", 9, 13, "c"), False)
t("21~22", rb.book("A102", "월", 21, 22, "c"), False)
t("기존 안쪽 포함 겹침", rb.book("A101", "월", 10, 11, "c"), False)
t("기존 감싸는 겹침", rb.book("A101", "월", 17, 20, "c"), False)
t("같은 시간 동일", rb.book("A101", "월", 9, 12, "c"), False)
t("앞에 바로 붙이기", rb.book("A101", "월", 12, 13, "c"), True)
t("다른 강의실 같은 시간", rb.book("A102", "월", 9, 12, "d"), True)
t("다른 요일 같은 시간", rb.book("A101", "화", 9, 12, "d"), True)
t("실패는 저장 안 함", rb.get_schedule("A101", "월"), [(9, 12, "a"), (12, 13, "c"), (18, 21, "b")])

# 빈 이름
rb = RoomBooking()
t("빈 이름", rb.book("A101", "화", 10, 11, ""), False)
t("띄어쓰기만 이름", rb.book("A101", "화", 10, 11, "   "), False)
t("None 이름", rb.book("A101", "화", 10, 11, None), False)
t("숫자 이름", rb.book("A101", "화", 10, 11, 123), False)
t("빈 이름 실패는 저장 안 함", rb.get_schedule("A101", "화"), [])
t("정상 이름은 가능", rb.book("A101", "화", 10, 11, "김"), True)

# 하루 2건
rb = RoomBooking()
t("2건-1", rb.book("A101", "목", 9, 10, "홍"), True)
t("2건-2", rb.book("A102", "목", 9, 10, "홍"), True)
t("3건째 다른 강의실", rb.book("B201", "목", 9, 10, "홍"), False)
t("다른 요일은 가능", rb.book("B201", "금", 9, 10, "홍"), True)
t("다른 사람은 가능", rb.book("B201", "목", 9, 10, "김"), True)
t("취소 후 다시 가능", rb.cancel("A101", "목", 9, "홍"), True)
t("취소 후 3번째 예약", rb.book("A101", "목", 10, 11, "홍"), True)
t("2건 실패 시 저장 안 함", rb.get_schedule("B201", "목"), [(9, 10, "김")])

# 취소
rb = RoomBooking()
rb.book("A101", "수", 10, 12, "x")
t("없는 예약 취소", rb.cancel("A101", "수", 11, "x"), False)
t("다른 강의실 취소", rb.cancel("A102", "수", 10, "x"), False)
t("없는 요일 취소", rb.cancel("A101", "토", 10, "x"), False)
t("남의 이름 취소", rb.cancel("A101", "수", 10, "y"), False)
t("남의 취소 후 유지", rb.get_schedule("A101", "수"), [(10, 12, "x")])
t("본인 취소", rb.cancel("A101", "수", 10, "x"), True)
t("두 번 취소", rb.cancel("A101", "수", 10, "x"), False)
t("취소 후 빈 시간표", rb.get_schedule("A101", "수"), [])
t("취소 시간대 재예약", rb.book("A101", "수", 10, 12, "y"), True)

# 시간표
rb = RoomBooking()
t("빈 시간표", rb.get_schedule("A101", "월"), [])
t("없는 강의실 시간표", rb.get_schedule("C999", "월"), [])
t("없는 요일 시간표", rb.get_schedule("A101", "일"), [])
for s in (18, 9, 15, 12):
    rb.book("B201", "금", s, s + 1, f"n{s}")
sch = rb.get_schedule("B201", "금")
t("정렬", sch, [(9, 10, "n9"), (12, 13, "n12"), (15, 16, "n15"), (18, 19, "n18")])
t("튜플 타입", all(type(x) is tuple for x in sch) and type(sch) is list, True)
sch.clear()
t("반환값 수정해도 내부 유지", len(rb.get_schedule("B201", "금")), 4)

# 인스턴스 독립
a, b = RoomBooking(), RoomBooking()
a.book("A101", "월", 10, 11, "z")
t("인스턴스 독립", b.get_schedule("A101", "월"), [])

# 성능
t0 = time.time()
rb = RoomBooking()
for i in range(20000):
    rb.book("A101", "월", 9 + i % 12, 10 + i % 12, f"p{i}")
    rb.get_schedule("A101", "월")
t("2만 회 호출 1초 이내", time.time() - t0 < 1, True)

print(f"\n실패 {fails}개")
