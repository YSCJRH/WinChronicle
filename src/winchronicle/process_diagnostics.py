from __future__ import annotations


def format_process_exit_failure(process_name: str, returncode: int) -> str:
    message = f"{process_name} failed with exit code {returncode}"
    windows_status = _windows_status_hex(returncode)
    if windows_status:
        return f"{message} (windows_status={windows_status})"
    return message


def _windows_status_hex(returncode: int) -> str:
    if -255 <= returncode <= 255:
        return ""
    return f"0x{returncode & 0xFFFFFFFF:08X}"
