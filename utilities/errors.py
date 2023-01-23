class SoupError(Exception):  # 사용자 정의 에러
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
