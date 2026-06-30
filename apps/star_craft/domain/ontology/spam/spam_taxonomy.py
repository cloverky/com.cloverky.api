from enum import Enum


class SpamCategory(Enum):
    ADVERTISING = "advertising"
    PHISHING = "phishing"
    MALWARE = "malware"
    SCAM = "scam"
    ADULT = "adult"
    POLITICAL = "political"
    UNKNOWN = "unknown"


SPAM_TAXONOMY: dict[SpamCategory, list[str]] = {
    SpamCategory.ADVERTISING: ["할인", "이벤트", "무료", "특가", "쿠폰"],
    SpamCategory.PHISHING: ["계정", "비밀번호", "인증", "로그인", "본인확인"],
    SpamCategory.MALWARE: ["첨부파일", "실행", "다운로드", "설치"],
    SpamCategory.SCAM: ["당첨", "투자", "수익", "환급", "송금"],
    SpamCategory.ADULT: ["성인", "만남", "데이트"],
    SpamCategory.POLITICAL: ["지지", "투표", "선거", "후보"],
}
