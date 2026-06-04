from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository

class WalterRoasterPgRepository(WalterRoasterRepository):
    '''PostgreSQL을 사용하는 월터의 승객 명단 관리 저장소'''

    def __init__(self):
        pass

    def introduce_myself(self):
        ''' 승객 명단을 가져오는 메소드'''
        # PostgreSQL에서 승객 명단을 가져오는 로직 구현
        pass