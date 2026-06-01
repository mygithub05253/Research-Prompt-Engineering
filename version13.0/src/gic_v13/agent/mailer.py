"""무료 SMTP(Gmail 등) 메일 발송.

표준 라이브러리(smtplib, email)만 사용한다. 유료 메일 API에 의존하지 않는다.
인증값은 코드에 저장하지 않고 환경변수로만 받는다.

필요 환경변수:
- GIC_SMTP_HOST     (기본 smtp.gmail.com)
- GIC_SMTP_PORT     (기본 465, SSL)
- GIC_SMTP_USER     (보내는 Gmail 주소)
- GIC_SMTP_PASSWORD (Gmail '앱 비밀번호' 16자리)
- GIC_MAIL_TO       (받는 사람, 쉼표로 여러 명)
"""

from __future__ import annotations

import os
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path

from gic_v13.agent.batch import AgentRunResult

_STATUS_EMOJI = {"PASS": "✅", "WARNING": "⚠️", "FAIL": "❌", "ERROR": "🚫"}


@dataclass
class SmtpConfig:
    host: str
    port: int
    user: str
    password: str
    recipients: list[str]

    @classmethod
    def from_env(cls) -> "SmtpConfig | None":
        """환경변수에서 SMTP 설정을 읽는다. 필수값이 없으면 None을 반환한다."""
        user = os.environ.get("GIC_SMTP_USER", "").strip()
        password = os.environ.get("GIC_SMTP_PASSWORD", "").strip()
        recipients_raw = os.environ.get("GIC_MAIL_TO", "").strip()
        if not (user and password and recipients_raw):
            return None
        recipients = [addr.strip() for addr in recipients_raw.split(",") if addr.strip()]
        return cls(
            host=os.environ.get("GIC_SMTP_HOST", "smtp.gmail.com").strip(),
            port=int(os.environ.get("GIC_SMTP_PORT", "465")),
            user=user,
            password=password,
            recipients=recipients,
        )


def build_summary(results: list[AgentRunResult]) -> str:
    """메일 본문(텍스트) 요약을 만든다."""
    lines = [
        "GIC v13 리서치 에이전트 자동 실행 결과",
        "=" * 40,
        "",
    ]
    for result in results:
        emoji = _STATUS_EMOJI.get(result.qa_status, "")
        lines.append(f"{emoji} [{result.qa_status}] {result.entity} ({result.run_id})")
        if result.error:
            lines.append(f"    - 오류: {result.error}")
        for warning in result.warnings:
            lines.append(f"    - 경고: {warning}")
        for fatal in result.fatal_errors:
            lines.append(f"    - 치명: {fatal}")
    lines.extend(
        [
            "",
            "-" * 40,
            "주의: 이 초안은 QA gate 통과 전 자료입니다.",
            "사람 검토 전에는 release-ready(최종본)가 아닙니다.",
            "첨부된 preview.html을 브라우저로 열어 확인하세요.",
        ]
    )
    return "\n".join(lines)


def build_message(results: list[AgentRunResult], config: SmtpConfig, subject_prefix: str = "[GIC v13]") -> EmailMessage:
    """첨부파일이 포함된 EmailMessage를 만든다."""
    message = EmailMessage()
    pass_count = sum(1 for r in results if r.qa_status == "PASS")
    message["Subject"] = f"{subject_prefix} 리서치 초안 {len(results)}건 (PASS {pass_count})"
    message["From"] = config.user
    message["To"] = ", ".join(config.recipients)
    message.set_content(build_summary(results))

    for result in results:
        for path in (result.preview_path, result.qa_report_path):
            if path and Path(path).exists():
                data = Path(path).read_bytes()
                subtype = "html" if path.suffix == ".html" else "markdown"
                filename = f"{result.run_id}_{path.name}"
                message.add_attachment(data, maintype="text", subtype=subtype, filename=filename)
    return message


def send_report_email(
    results: list[AgentRunResult],
    config: SmtpConfig | None = None,
    subject_prefix: str = "[GIC v13]",
) -> bool:
    """결과를 메일로 발송한다.

    config가 없고 환경변수도 비어 있으면 발송을 건너뛰고 False를 반환한다(에이전트는 죽지 않는다).
    """
    config = config or SmtpConfig.from_env()
    if config is None:
        return False

    message = build_message(results, config, subject_prefix=subject_prefix)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config.host, config.port, context=context) as server:
        server.login(config.user, config.password)
        server.send_message(message)
    return True
