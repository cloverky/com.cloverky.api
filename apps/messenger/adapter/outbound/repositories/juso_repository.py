from __future__ import annotations

import logging

from messenger.adapter.outbound.orm.juso_orm import ContactOrm
from messenger.app.dtos.juso_dto import (
    ContactUploadCommand,
    ContactUploadResult,
    JusoMessengerQuery,
    JusoMessengerResponse,
    JusoSearchCommand,
    JusoSearchResult,
)
from messenger.app.ports.output.juso_repository_port import JusoRepositoryPort
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class JusoPgRepository(JusoRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def search(self, cmd: JusoSearchCommand) -> JusoSearchResult:
        logger.info("[JusoPgRepository] search 진입 | keyword=%r", cmd.keyword)
        # TODO: 행정안전부 주소 API 또는 DB 연동 후 구현
        return JusoSearchResult(total_count=0, results=[])

    async def upload_contacts(self, cmd: ContactUploadCommand) -> ContactUploadResult:
        logger.info(
            "[JusoPgRepository] upload_contacts 진입 | 총 %d건", len(cmd.records)
        )
        saved = skipped = 0
        for record in cmd.records:
            if not record.email_1_value:
                skipped += 1
                continue
            orm = ContactOrm(
                first_name=record.first_name or None,
                middle_name=record.middle_name or None,
                last_name=record.last_name or None,
                phonetic_first_name=record.phonetic_first_name or None,
                phonetic_middle_name=record.phonetic_middle_name or None,
                phonetic_last_name=record.phonetic_last_name or None,
                name_prefix=record.name_prefix or None,
                name_suffix=record.name_suffix or None,
                nickname=record.nickname or None,
                file_as=record.file_as or None,
                organization_name=record.organization_name or None,
                organization_title=record.organization_title or None,
                organization_department=record.organization_department or None,
                birthday=record.birthday or None,
                notes=record.notes or None,
                photo=record.photo or None,
                labels=record.labels or None,
                email_1_label=record.email_1_label or None,
                email_1_value=record.email_1_value,
                phone_1_label=record.phone_1_label or None,
                phone_1_value=record.phone_1_value or None,
            )
            self.session.add(orm)
            saved += 1

        await self.session.commit()
        logger.info(
            "[JusoPgRepository] 저장 완료 | saved=%d skipped=%d", saved, skipped
        )
        return ContactUploadResult(saved=saved, skipped=skipped)

    async def introduce_myself(
        self, query: JusoMessengerQuery
    ) -> JusoMessengerResponse:
        logger.info("[JusoPgRepository] introduce_myself 진입 | request_data=%s", query)
        return JusoMessengerResponse(
            id=query.id,
            name=query.name,
            description=(
                "저는 주소 검색 서비스입니다. "
                "행정안전부 도로명주소 API를 통해 주소를 검색하고 "
                "우편번호, 도로명, 지번 주소를 제공합니다."
            ),
        )
