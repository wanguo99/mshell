"""复选框图标生成器"""

from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF


def create_checkmark_icon(size=18, color="#0e639c"):
    """创建勾选标记图标

    Args:
        size: 图标大小
        color: 勾选标记颜色

    Returns:
        QPixmap对象
    """
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # 设置画笔
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    painter.setPen(pen)

    # 绘制勾选标记
    # 短边
    painter.drawLine(
        QPointF(size * 0.25, size * 0.5),
        QPointF(size * 0.45, size * 0.7)
    )
    # 长边
    painter.drawLine(
        QPointF(size * 0.45, size * 0.7),
        QPointF(size * 0.75, size * 0.3)
    )

    painter.end()
    return pixmap
