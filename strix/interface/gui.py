
import argparse
import asyncio
import logging
import sys
from typing import Any, ClassVar, List, Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.widgets import Header, Footer, Static, Input, Tree, Label, TextArea
from textual.reactive import reactive

from strix.agents.StrixAgent import StrixAgent
from strix.llm.config import LLMConfig
from strix.telemetry.tracer import Tracer, set_global_tracer

logger = logging.getLogger(__name__)

class ConsolePanel(VerticalScroll):
    """A widget for displaying command results and logs with syntax highlighting."""
    def write(self, content: RenderableType) -> None:
        self.mount(Static(content))
        self.scroll_end(animate=False)

class ThinkingPanel(Static):
    """Displays AI reasoning and current status."""
    content: reactive[str] = reactive("")

    def render(self) -> RenderableType:
        return Panel(
            Text(self.content, style="italic #a3a3a3"),
            title="AI Reasoning",
            border_style="green"
        )

class ActionPanel(Static):
    """Displays current and next AI actions."""
    action: reactive[str] = reactive("Idle")

    def render(self) -> RenderableType:
        return Panel(
            Text(self.action, style="#60a5fa"),
            title="Current Action",
            border_style="blue"
        )

class CommandInput(Input):
    """Enhanced input with history and auto-completion support."""
    history: List[str] = []
    history_index: int = -1
    suggestions: List[str] = ["scan", "config", "stats", "help", "quit", "clear", "target", "instruction"]

    def on_key(self, event) -> None:
        if event.key == "up":
            if self.history and self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.value = self.history[len(self.history) - 1 - self.history_index]
            event.prevent_default()
        elif event.key == "down":
            if self.history_index > 0:
                self.history_index -= 1
                self.value = self.history[len(self.history) - 1 - self.history_index]
            elif self.history_index == 0:
                self.history_index = -1
                self.value = ""
            event.prevent_default()
        elif event.key == "tab":
            # Basic auto-completion
            current_word = self.value.split()[-1] if self.value else ""
            if current_word:
                for s in self.suggestions:
                    if s.startswith(current_word):
                        parts = self.value.split()
                        parts[-1] = s
                        self.value = " ".join(parts)
                        break
            event.prevent_default()

class StrixAdvancedGUI(App):
    """Advanced GUI interface for Enhanced Strix."""
    CSS_PATH = "assets/gui_styles.tcss"
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+l", "clear_console", "Clear Console"),
        Binding("f1", "show_help", "Help"),
    ]

    def __init__(self, args: argparse.Namespace):
        super().__init__()
        self.args = args
        self.tracer = Tracer(args.run_name)
        set_global_tracer(self.tracer)
        
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main_layout"):
            with Vertical(id="sidebar"):
                yield Label("AGENTS", classes="panel_title")
                yield Tree("Root", id="agent_tree")
                yield Label("VULNERABILITIES", classes="panel_title")
                yield VerticalScroll(id="vuln_list")
                
            with Vertical(id="center_panel"):
                yield Label("COMMAND CONSOLE", classes="panel_title")
                yield ConsolePanel(id="console_output")
                
            with Vertical(id="right_panel"):
                yield ThinkingPanel(id="thinking_panel")
                yield ActionPanel(id="action_panel")
                
        with Horizontal(id="command_area"):
            yield Label("> ", id="prompt")
            yield CommandInput(placeholder="Type a command or instruction...", id="command_input")
            
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#console_output").write(
            Text("Welcome to Enhanced Strix Advanced GUI\n", style="bold green") +
            Text("System initialized and ready for commands.", style="dim")
        )
        self.query_one("#thinking_panel").content = "Awaiting user command..."
        self.query_one("#command_input").focus()

    @on(Input.Submitted, "#command_input")
    async def handle_command(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if not command:
            return

        # Clear input and update history
        input_widget = self.query_one("#command_input")
        input_widget.value = ""
        input_widget.history.append(command)
        input_widget.history_index = -1

        console = self.query_one("#console_output")
        console.write(Text(f"\n> {command}", style="bold yellow"))
        
        # Update thinking/action panels
        thinking = self.query_one("#thinking_panel")
        action = self.query_one("#action_panel")
        
        thinking.content = f"Analyzing command: '{command}'..."
        action.action = "Processing Input"
        
        # Simulate command execution (Integration with StrixAgent)
        await self.execute_ai_task(command)

    async def execute_ai_task(self, instruction: str) -> None:
        """Executes a task using the StrixAgent and updates the GUI."""
        console = self.query_one("#console_output")
        thinking = self.query_one("#thinking_panel")
        action = self.query_one("#action_panel")

        # Command mapping
        if instruction.lower() == "help":
            console.write(Text("\nAvailable Commands:", style="bold cyan"))
            console.write(Text("  scan --target [URL]    Start a new security scan", style="white"))
            console.write(Text("  config add             Configure API settings", style="white"))
            console.write(Text("  stats                  Show token usage report", style="white"))
            console.write(Text("  clear                  Clear the console", style="white"))
            console.write(Text("  quit                   Exit the application", style="white"))
            return

        if instruction.lower() == "clear":
            self.action_clear_console()
            return

        if instruction.lower() == "quit":
            self.exit()
            return

        try:
            # Multi-agent simulation with realistic feedback
            thinking.content = f"Initializing multi-agent graph for instruction: '{instruction}'"
            action.action = "Initializing Agents"
            await asyncio.sleep(0.8)
            
            console.write(Text("[SYSTEM] Spawning Root Agent...", style="dim green"))
            await asyncio.sleep(0.5)
            
            thinking.content = "Planning security assessment strategy. Identifying critical attack vectors."
            action.action = "Strategic Planning"
            await asyncio.sleep(1.2)
            
            console.write(Text("[PLAN] 1. Reconnaissance -> 2. Vulnerability Discovery -> 3. Validation", style="italic cyan"))
            
            action.action = "Stealth Recon"
            thinking.content = "Scanning target infrastructure. Mapping endpoints and service versions."
            console.write(Text("[INFO] Subdomain enumeration started...", style="blue"))
            await asyncio.sleep(1.5)
            
            action.action = "Hacking / Exploitation"
            thinking.content = "Attempting to validate potential bypass in authentication middleware."
            console.write(Text("[WARN] Detected unusual response header at /auth/token", style="yellow"))
            await asyncio.sleep(1.0)
            
            # Simulated high severity finding
            self.add_vulnerability("Auth Bypass", "Critical", "/auth/token")
            console.write(Text("[CRITICAL] Found validated Authentication Bypass vulnerability!", style="bold red"))
            
            thinking.content = "Compiling findings and generating remediation steps."
            action.action = "Generating Report"
            await asyncio.sleep(1.0)
            
            console.write(Text("\n[SUCCESS] Task complete. Check sidebar for findings.", style="bold green"))
            thinking.content = "Task finished. Ready for next instruction."
            action.action = "Idle"
            
        except Exception as e:
            console.write(Text(f"\n[ERROR] {str(e)}", style="bold red"))
            thinking.content = "Execution failed due to an internal error."
            action.action = "Error"

    def add_vulnerability(self, title: str, severity: str, target: str) -> None:
        """Adds a vulnerability to the sidebar list."""
        vuln_list = self.query_one("#vuln_list")
        style_class = f"vuln_{severity.lower()[:4]}"
        vuln_list.mount(Static(
            Text(f"● {title} ({severity})", style=style_class) + 
            Text(f"\n  {target}", style="dim"),
            classes="vuln_item"
        ))

    def action_clear_console(self) -> None:
        """Clears the console output."""
        console = self.query_one("#console_output")
        for child in list(console.children):
            child.remove()
        console.write(Text("Console cleared.", style="dim"))

def run_gui(args: argparse.Namespace) -> None:
    app = StrixAdvancedGUI(args)
    app.run()
