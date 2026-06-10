from __future__ import annotations
from typing import Optional

from clover.apps.titanic.adapter.outbound.orm.passenger_cal_tester_orm import CalTesterOrm


class CalTesterMapper:

    @staticmethod
    def to_entity(orm: CalTesterOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("CalTester 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: Optional[CalTesterOrm] = None) -> CalTesterOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("CalTester 엔티티 정의 후 구현 필요")
