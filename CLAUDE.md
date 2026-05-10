# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MShell** - A cross-platform terminal application similar to Xshell, supporting SSH and serial connections with SFTP file transfer, custom shortcuts, ANSI color rendering, and multi-tab session management.

**Tech Stack**: Python 3.8+, PyQt5, paramiko (SSH), pyserial (serial), PyYAML (config)

**Current Status**: Early scaffolding phase. Core modules are defined but not yet implemented. The project uses a modular architecture with platform abstraction layer (OSA) to handle OS-specific differences.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Run all tests
python -m pytest tests/

# Run specific module tests
python -m pytest tests/test_platform.py
python -m pytest tests/test_terminal.py
python -m pytest tests/test_ui.py
```

## Architecture

### Design Principles

1. **OS Abstraction Layer (OSA)**: Platform-specific code isolated in `platform/` module. Core business logic remains platform-agnostic.
2. **Modular Design**: Clear separation of concerns across modules with well-defined interfaces.
3. **Mock-Driven Development**: Modules can be developed independently using mock implementations in `tests/`.

### Module Structure

```
platform/          # OS abstraction layer - handles Windows/Linux/macOS differences
├── base/          # Abstract interfaces (serial, config, clipboard, filesystem, ui)
├── windows/       # Windows implementations
├── linux/         # Linux implementations  
├── macos/         # macOS implementations
└── factory.py     # Platform factory: get_platform()

config/            # Configuration management
└── config_manager.py  # Loads/saves YAML config from platform-specific paths

core/              # Connection management
├── connection_manager.py  # Abstract base class
├── ssh_connection.py      # SSH via paramiko
├── serial_connection.py   # Serial via pyserial
└── command_executor.py    # Quick command execution

terminal/          # Terminal rendering
├── terminal_widget.py  # PyQt5 terminal display widget
├── ansi_parser.py      # ANSI escape sequence parser
└── color_scheme.py     # Color scheme management

ui/                # User interface
├── main_window.py       # Main application window
├── connection_dialog.py # Connection configuration
├── settings_dialog.py   # Settings UI
└── session_tab.py       # Tab management

file_transfer/     # SFTP file transfer
├── sftp_client.py   # SFTP operations via paramiko
└── file_browser.py  # File browser UI
```

### Key Interfaces

**Platform Factory** (implemented in `platform/factory.py`):
```python
from platform.factory import get_platform
platform = get_platform()  # Returns Windows/Linux/macOS implementation

# Available interfaces:
platform.serial.get_available_ports() -> List[str]
platform.config.get_config_dir() -> str
platform.clipboard.get_text() -> str
platform.filesystem.normalize_path(path) -> str
platform.ui.get_default_font() -> Tuple[str, int]
platform.ui.get_shortcut_modifier() -> str  # "Ctrl" or "Cmd"
```

**Connection Manager** (base class in `core/connection_manager.py`):
```python
class ConnectionManager(ABC):
    on_data_received: Callable[[bytes], None]
    on_connection_changed: Callable[[bool], None]
    
    def connect(self, **kwargs) -> bool
    def disconnect(self)
    def send(self, data: bytes)
    def is_connected(self) -> bool
```

**Terminal Widget** (in `terminal/terminal_widget.py`):
```python
class TerminalWidget(QWidget):
    data_to_send = pyqtSignal(bytes)
    
    def write_output(self, data: str)
    def clear(self)
    def set_color_scheme(self, scheme_name: str)
    def set_font(self, font_family: str, font_size: int)
```

### Platform Differences

**Serial Port Naming**:
- Windows: `COM1`, `COM2`, `COM3`...
- Linux: `/dev/ttyUSB0`, `/dev/ttyACM0`, `/dev/ttyS0`...
- macOS: `/dev/tty.usbserial-*`, `/dev/cu.usbserial-*`

**Config Paths**:
- Windows: `%APPDATA%\MShell\config.yaml`
- Linux: `~/.config/mshell/config.yaml`
- macOS: `~/Library/Application Support/MShell/config.yaml`

**Default Fonts**:
- Windows: Consolas, Courier New
- Linux: Monospace, DejaVu Sans Mono
- macOS: Menlo, Monaco

**Keyboard Modifiers**:
- Windows/Linux: Ctrl
- macOS: Cmd (⌘)

**Line Endings**:
- Windows: CRLF (`\r\n`)
- Linux/macOS: LF (`\n`)

## Configuration

Configuration is stored in YAML format at `config/default_config.yaml`. Key sections:

- `connections`: SSH and serial connection profiles
- `shortcuts`: Keyboard shortcuts (e.g., `"Ctrl+T": "new_tab"`)
- `quick_commands`: Quick command definitions with shortcuts
- `terminal`: Font, color scheme, scrollback settings
- `color_schemes`: Color definitions (default, solarized_dark, monokai)
- `file_transfer`: SFTP settings
- `application`: Language, theme, session restore settings

## Development Notes

### Using Mocks

During development, use mock implementations when dependencies aren't ready:

```python
# Development - use mock
from tests.mock_platform import get_mock_platform
platform = get_mock_platform()

# Production - use real implementation
from platform.factory import get_platform
platform = get_platform()
```

Mock files: `tests/mock_platform.py`, `tests/mock_terminal.py`

### Module Dependencies

- `platform/` and `config/`: No dependencies (can be developed first)
- `core/` and `terminal/`: Depend on `platform/` interfaces
- `ui/` and `file_transfer/`: Depend on `platform/`, `core/`, and `terminal/`

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public APIs
- Commit message format: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`

## Important Documentation

- `docs/INTERFACE_CONTRACT.md` - Detailed interface specifications
- `docs/DEVELOPMENT_GUIDE.md` - Development workflow and guidelines
- `config/default_config.yaml` - Configuration file structure and examples
