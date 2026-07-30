import sys
import os
import subprocess

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.align import Align
    from rich.text import Text
    from rich import box
    from rich.table import Table
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.align import Align
    from rich.text import Text
    from rich import box
    from rich.table import Table

try:
    import pyfiglet
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet"])
    import pyfiglet

console = Console()

COLOR_BORDER = "#D4C4A8"
COLOR_TITLE = "#C4A96A"
COLOR_ACCENT = "#A68A56"
COLOR_TEXT = "#F5EBD9"
COLOR_DIM = "#8B7A5B"
COLOR_RED = "#FF5555"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()

    banner = pyfiglet.figlet_format("SERVER OFFLINE", font="standard")
    console.print(Align.center(Text(banner, style=f"bold {COLOR_TITLE}")))
    console.print(Align.center(Text("══════════════════════════════════════════", style=COLOR_BORDER)))
    console.print(Align.center(Text("◆ SERVER STATUS ◆", style=f"bold {COLOR_ACCENT}")))
    console.print(Align.center(Text("──────────────────────────────────────────", style=COLOR_DIM)))
    console.print()

    steps_lines = [
        Text("◆ SERVER IS CURRENTLY OFFLINE ◆", style=f"bold {COLOR_TITLE}"),
        Text(""),
        Text("The secure server infrastructure is temporarily unavailable.", style=f"italic {COLOR_TEXT}"),
        Text("All services have been suspended for scheduled maintenance.", style=f"italic {COLOR_TEXT}"),
        Text(""),
        Text("   ▸ Reason:  Emergency system maintenance & security update", style=COLOR_ACCENT),
        Text("   ▸ ETA:     No precise return time – we will notify you", style=COLOR_ACCENT),
        Text("   ▸ Scope:   Complete service shutdown – no endpoints active", style=COLOR_ACCENT),
        Text("   ▸ Status:  No data loss – all systems are preserved", style=COLOR_ACCENT),
        Text("   ▸ Action:  No user intervention required", style=COLOR_ACCENT),
        Text(""),
        Text("◈ Instructions for administrators:", style=f"bold {COLOR_TITLE}"),
        Text("   • Do not attempt to reconnect until the green light is given", style=COLOR_TEXT),
        Text("   • The server will not respond to any request", style=COLOR_TEXT),
        Text("   • Monitor official channels for the restoration announcement", style=COLOR_TEXT),
        Text("   • No alternative entry points are available", style=COLOR_TEXT),
        Text(""),
        Text("⌛ Server is powered down – no activity is being logged.", style=f"italic {COLOR_DIM}")
    ]

    combined_top = Text("\n").join(steps_lines)

    panel_top = Panel(
        Align.center(combined_top, vertical="middle"),
        title=Text(" SERVER STATUS ", style=f"bold {COLOR_TITLE}"),
        border_style=COLOR_BORDER,
        box=box.HEAVY,
        width=80,
        padding=(2, 4)
    )
    console.print(Align.center(panel_top))
    console.print()

    maintenance_lines = [
        Text("◆ OFFLINE MAINTENANCE MODE ◆", style=f"bold {COLOR_ACCENT}"),
        Text(""),
        Text("THE SECURE GATEWAY IS CURRENTLY TURNED OFF", style=f"bold {COLOR_TITLE}"),
        Text(""),
        Text("• Status:", style=COLOR_ACCENT) + Text(" Offline – scheduled downtime", style="yellow"),
        Text("• Reason:", style=COLOR_ACCENT) + Text(" Critical system upgrade & security audit", style=COLOR_TEXT),
        Text("• Duration:", style=COLOR_ACCENT) + Text(" To be announced – check back later", style=COLOR_TEXT),
        Text("• Scope:", style=COLOR_ACCENT) + Text(" All services are inactive", style="green"),
        Text(""),
        Text("IMPORTANT NOTICE", style=f"bold {COLOR_TITLE}"),
        Text("Your session, data, and device remain completely safe.", style=COLOR_TEXT),
        Text("This is a temporary shutdown – no unauthorised access occurred.", style=COLOR_TEXT),
        Text(""),
        Text("⌛ Server is offline – please refrain from sending requests.", style=f"italic {COLOR_DIM}"),
        Text("💡 No other gateways or fallback servers are available.", style=COLOR_ACCENT),
        Text(""),
        Text("✘ SERVER OFFLINE ✘", style=f"bold {COLOR_ACCENT}")
    ]

    combined_bottom = Text("\n").join(maintenance_lines)

    panel_bottom = Panel(
        Align.center(combined_bottom, vertical="middle"),
        title=Text(" MAINTENANCE SHUTDOWN ", style=f"bold {COLOR_TITLE}"),
        border_style=COLOR_BORDER,
        box=box.HEAVY,
        width=80,
        padding=(2, 4)
    )
    console.print(Align.center(panel_bottom))
    console.print()

    warning_lines = [
        Text("⚠ SECURITY WARNING ⚠", style=f"bold {COLOR_RED}"),
        Text(""),
        Text("Any attempt to bypass, deobfuscate, reverse engineer, or tamper with this server", style=COLOR_TEXT),
        Text("will be detected by the integrated security monitoring system and AI defence layers.", style=COLOR_TEXT),
        Text(""),
        Text("CONSEQUENCES OF UNAUTHORISED ACCESS:", style=f"bold {COLOR_RED}"),
        Text("   • Immediate device fingerprint capture and logging", style=COLOR_TEXT),
        Text("   • Automated countermeasures will be activated", style=COLOR_TEXT),
        Text("   • Network traffic will be throttled and analysed", style=COLOR_TEXT),
        Text("   • Persistent resource exhaustion may occur", style=COLOR_TEXT),
        Text("   • Further legal and administrative actions will be taken", style=COLOR_TEXT),
        Text(""),
        Text("You have been warned. Do not attempt any malicious actions.", style=f"bold {COLOR_RED}")
    ]

    combined_warning = Text("\n").join(warning_lines)

    warning_panel = Panel(
        Align.center(combined_warning, vertical="middle"),
        title=Text(" !!! UNAUTHORISED ACCESS PROHIBITED !!! ", style=f"bold {COLOR_RED}"),
        border_style=COLOR_RED,
        box=box.DOUBLE_EDGE,
        width=80,
        padding=(2, 4)
    )
    console.print(Align.center(warning_panel))
    console.print()

    info_line = Panel(
        Align.center(Text("— SERVER IS TEMPORARILY OFFLINE —", style=f"bold {COLOR_ACCENT}")),
        border_style=COLOR_BORDER,
        box=box.SQUARE,
        width=60,
        padding=(0,1)
    )
    console.print(Align.center(info_line))
    console.print()

    sys.exit(0)

if __name__ == "__main__":
    main()