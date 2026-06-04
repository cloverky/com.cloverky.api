from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
import logging
logger = logging.getLogger(__name__)

class WalterRoasterPgRepository(WalterRoasterRepository):
    '''PostgreSQL을 사용하는 월터의 승객 명단 관리 저장소'''

    def __init__(self):
        pass

    def introduce_myself(self, query: WalterRoasterQuery):
        ''' 승객 명단을 가져오는 메소드'''
        # PostgreSQL에서 승객 명단을 가져오는 로직 구현
        logger.info("##################################################")
        logger.info("💎 [월터 저장소] 월터의 자기소개글을 가져오는 메소드")
        logger.info(f"💎 ID: {query.id}")
        logger.info(f"💎 이름: {query.name}")
        logger.info(f"💎 비고: {query.memo}")
        logger.info("##################################################")
        
        pass