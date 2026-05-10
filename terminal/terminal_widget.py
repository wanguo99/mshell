"""Terminal Display Widget

Full-featured terminal emulator using pyte for VT100/xterm emulation.
Supports cursor control, line editing, colors, and all shell features.
"""

import pyte
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QKeyEvent, QTextCursor

from mshell_platform import get_platform
from terminal.color_scheme import ColorSchemeManager


class TerminalWidget(QTextEdit):
    """Full-featured terminal display widget with VT100 emulation"""

    # Signal: send data to connection
    data_to_send = pyqtSignal(bytes)

    def __init__(self, parent=None, rows=24, cols=80):
        super().__init__(parent)

        self.platform = get_platform()
        self.color_scheme_manager = ColorSchemeManager()

        # Terminal dimensions
        self.rows = rows
        self.cols = cols

        # Create pyte screen and stream
        self.screen = pyte.Screen(cols, rows)
        self.stream = pyte.Stream(self.screen)

        # Setup terminal
        self._setup_terminal()

        # Refresh timer for rendering
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._render_screen)
        self.refresh_timer.start(50)  # 20 FPS

        # Track if screen needs redraw
        self.dirty = False

    def _setup_terminal(self):
        """Setup terminal attributes"""
        # Read-only mode, all display from remote
        self.setReadOnly(True)

        # Set default font
        font_family, font_size = self.platform.ui.get_default_font()
        self.set_font(font_family, font_size)

        # Set color scheme
        self.set_color_scheme("default")

        # Disable word wrap for proper terminal display
        self.setLineWrapMode(QTextEdit.NoWrap)

        # Set cursor style
        self.setCursorWidth(8)

        # Accept focus for keyboard events
        self.setFocusPolicy(Qt.StrongFocus)

    def write_output(self, data: str):
        """Write output to terminal

        Args:
            data: Text data to display
        """
        if not data:
            return

        # Feed data to pyte stream
        self.stream.feed(data)
        self.dirty = True

    def _render_screen(self):
        """Render pyte screen to QTextEdit"""
        if not self.dirty:
            return

        self.dirty = False

        # Get color scheme
        scheme = self.color_scheme_manager.get_current_scheme()
        default_fg = QColor(*scheme.get_foreground())
        default_bg = QColor(*scheme.get_background())

        # Clear document
        self.clear()
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)

        # Render each line
        for y in range(self.screen.lines):
            line = self.screen.buffer[y]

            for x in range(self.screen.columns):
                char = line[x]

                # Create character format
                char_format = QTextCharFormat()

                # Set foreground color
                if char.fg != 'default':
                    fg_color = self._convert_color(char.fg)
                    char_format.setForeground(QColor(*fg_color))
                else:
                    char_format.setForeground(default_fg)

                # Set background color
                if char.bg != 'default':
                    bg_color = self._convert_color(char.bg)
                    char_format.setBackground(QColor(*bg_color))

                # Set text styles
                if char.bold:
                    char_format.setFontWeight(QFont.Bold)
                if char.italics:
                    char_format.setFontItalic(True)
                if char.underscore:
                    char_format.setFontUnderline(True)

                # Reverse video
                if char.reverse:
                    fg = char_format.foreground().color()
                    bg = char_format.background().color()
                    char_format.setForeground(bg)
                    char_format.setBackground(fg)

                # Insert character
                cursor.insertText(char.data, char_format)

            # Add newline except for last line
            if y < self.screen.lines - 1:
                cursor.insertText('\n')

        # Position cursor at pyte cursor position
        cursor.movePosition(QTextCursor.Start)
        for _ in range(self.screen.cursor.y):
            cursor.movePosition(QTextCursor.Down)
        for _ in range(self.screen.cursor.x):
            cursor.movePosition(QTextCursor.Right)

        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def _convert_color(self, color):
        """Convert pyte color to RGB tuple

        Args:
            color: pyte color (string or int)

        Returns:
            RGB tuple
        """
        # Standard 16 colors
        color_map = {
            'black': (0, 0, 0),
            'red': (205, 0, 0),
            'green': (0, 205, 0),
            'brown': (205, 205, 0),
            'blue': (0, 0, 238),
            'magenta': (205, 0, 205),
            'cyan': (0, 205, 205),
            'white': (229, 229, 229),
            # Bright colors
            'brightblack': (127, 127, 127),
            'brightred': (255, 0, 0),
            'brightgreen': (0, 255, 0),
            'brightyellow': (255, 255, 0),
            'brightblue': (92, 92, 255),
            'brightmagenta': (255, 0, 255),
            'brightcyan': (0, 255, 255),
            'brightwhite': (255, 255, 255),
        }

        if isinstance(color, str):
            return color_map.get(color, (229, 229, 229))
        elif isinstance(color, int):
            # 256 color mode
            return self._convert_256_to_rgb(color)
        else:
            return (229, 229, 229)

    def _convert_256_to_rgb(self, color_index: int):
        """Convert 256 color index to RGB

        Args:
            color_index: 0-255 color index

        Returns:
            RGB tuple
        """
        if color_index < 16:
            # Standard 16 colors
            standard = [
                (0, 0, 0), (205, 0, 0), (0, 205, 0), (205, 205, 0),
                (0, 0, 238), (205, 0, 205), (0, 205, 205), (229, 229, 229),
                (127, 127, 127), (255, 0, 0), (0, 255, 0), (255, 255, 0),
                (92, 92, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)
            ]
            return standard[color_index]
        elif color_index < 232:
            # 216 color cube (16-231)
            index = color_index - 16
            r = (index // 36) * 51
            g = ((index % 36) // 6) * 51
            b = (index % 6) * 51
            return (r, g, b)
        else:
            # 24 grayscale (232-255)
            gray = 8 + (color_index - 232) * 10
            return (gray, gray, gray)

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard input

        Args:
            event: Keyboard event
        """
        key = event.key()
        modifiers = event.modifiers()
        text = event.text()

        # Handle special keys
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.data_to_send.emit(b'\r')
        elif key == Qt.Key_Backspace:
            self.data_to_send.emit(b'\x7f')
        elif key == Qt.Key_Tab:
            self.data_to_send.emit(b'\t')
        elif key == Qt.Key_Up:
            self.data_to_send.emit(b'\x1b[A')
        elif key == Qt.Key_Down:
            self.data_to_send.emit(b'\x1b[B')
        elif key == Qt.Key_Right:
            self.data_to_send.emit(b'\x1b[C')
        elif key == Qt.Key_Left:
            self.data_to_send.emit(b'\x1b[D')
        elif key == Qt.Key_Home:
            self.data_to_send.emit(b'\x1b[H')
        elif key == Qt.Key_End:
            self.data_to_send.emit(b'\x1b[F')
        elif key == Qt.Key_PageUp:
            self.data_to_send.emit(b'\x1b[5~')
        elif key == Qt.Key_PageDown:
            self.data_to_send.emit(b'\x1b[6~')
        elif key == Qt.Key_Delete:
            self.data_to_send.emit(b'\x1b[3~')
        elif key == Qt.Key_Insert:
            self.data_to_send.emit(b'\x1b[2~')
        elif modifiers & Qt.ControlModifier:
            # Ctrl combinations
            if key == Qt.Key_C:
                self.data_to_send.emit(b'\x03')
            elif key == Qt.Key_D:
                self.data_to_send.emit(b'\x04')
            elif key == Qt.Key_Z:
                self.data_to_send.emit(b'\x1a')
            elif key == Qt.Key_L:
                self.screen.reset()
                self.dirty = True
            elif Qt.Key_A <= key <= Qt.Key_Z:
                # Ctrl+A to Ctrl+Z
                ctrl_char = chr(key - Qt.Key_A + 1)
                self.data_to_send.emit(ctrl_char.encode('ascii'))
        elif modifiers & Qt.AltModifier:
            # Alt combinations - send ESC prefix
            if text:
                self.data_to_send.emit(b'\x1b' + text.encode('utf-8'))
        elif text:
            # Normal characters
            try:
                self.data_to_send.emit(text.encode('utf-8'))
            except UnicodeEncodeError:
                pass

    def clear(self):
        """Clear terminal"""
        self.document().clear()

    def set_font(self, font_family: str, font_size: int):
        """Set font

        Args:
            font_family: Font name
            font_size: Font size
        """
        font = QFont(font_family, font_size)
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        self.setFont(font)

    def set_color_scheme(self, scheme_name: str):
        """Set color scheme

        Args:
            scheme_name: Color scheme name
        """
        try:
            self.color_scheme_manager.set_current_scheme(scheme_name)
            scheme = self.color_scheme_manager.get_current_scheme()

            # Set background and foreground
            bg = scheme.get_background()
            fg = scheme.get_foreground()

            palette = self.palette()
            palette.setColor(palette.Base, QColor(*bg))
            palette.setColor(palette.Text, QColor(*fg))
            self.setPalette(palette)

            self.setStyleSheet(f"""
                QTextEdit {{
                    background-color: rgb({bg[0]}, {bg[1]}, {bg[2]});
                    color: rgb({fg[0]}, {fg[1]}, {fg[2]});
                    border: none;
                }}
            """)
            self.dirty = True
        except KeyError as e:
            print(f"Warning: {e}")

    def get_available_color_schemes(self):
        """Get available color schemes

        Returns:
            List of color scheme names
        """
        return self.color_scheme_manager.list_schemes()

    def resize_terminal(self, cols: int, rows: int):
        """Resize terminal

        Args:
            cols: Number of columns
            rows: Number of rows
        """
        self.cols = cols
        self.rows = rows
        self.screen.resize(rows, cols)
        self.dirty = True
