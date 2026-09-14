import sys
import os
import json
import time
import getpass

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTreeView, QAbstractItemView, 
                             QShortcut, QMenu, QStyledItemDelegate, QDialog,
                             QListWidget, QListWidgetItem, QSplitter, QSizePolicy)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QColor, QIcon, 
                         QPixmap, QPainter, QKeySequence)
from PyQt5.QtCore import Qt, QSize, QSortFilterProxyModel, QByteArray, pyqtSignal
from PyQt5.QtSvg import QSvgRenderer

# ==============================================================================
# Constants & Enums
# ==============================================================================
ROLE_TYPE = Qt.UserRole          
ROLE_STATUS = Qt.UserRole + 2    
ROLE_CREATED = Qt.UserRole + 3   
ROLE_OLD_NAME = Qt.UserRole + 4  

# ==============================================================================
# SVGs (Codicons)
# ==============================================================================
SVGS = {
    "new_file": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M5 14C4.448 14 4 13.552 4 13V3C4 2.448 4.448 2 5 2H8V4.5C8 5.328 8.672 6 9.5 6H12V6.025C12.344 6.056 12.677 6.121 13 6.213V5.414C13 5.016 12.842 4.635 12.561 4.353L9.647 1.439C9.366 1.158 8.984 1 8.586 1H5C3.895 1 3 1.895 3 3V13C3 14.105 3.895 15 5 15H7.261C7.008 14.693 6.791 14.357 6.607 14H5ZM9 2.207L11.793 5H9.5C9.224 5 9 4.776 9 4.5V2.207ZM11.5 7C9.015 7 7 9.015 7 11.5C7 13.985 9.015 16 11.5 16C13.985 16 16 13.985 16 11.5C16 9.015 13.985 7 11.5 7ZM14 12H12V14C12 14.276 11.776 14.5 11.5 14.5C11.224 14.5 11 14.276 11 14V12H9C8.724 12 8.5 11.776 8.5 11.5C8.5 11.224 8.724 11 9 11H11V9C11 8.724 11.224 8.5 11.5 8.5C11.776 8.5 12 8.724 12 9V11H14C14.276 11 14.5 11.224 14.5 11.5C14.5 11.776 14.276 12 14 12Z"/></svg>""",
    "new_folder": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M14.5 2H7.71l-1.5-1.5H2.5A1.5 1.5 0 0 0 1 2v11a1.5 1.5 0 0 0 1.5 1.5h12a1.5 1.5 0 0 0 1.5-1.5V3.5A1.5 1.5 0 0 0 14.5 2zm-12-1h3.29l1.5 1.5H14.5a.5.5 0 0 1 .5.5v1H2V2.5a.5.5 0 0 1 .5-.5zM2 13.5V6h13v7.5a.5.5 0 0 1-.5.5h-12a.5.5 0 0 1-.5-.5z"/><path d="M8 8h1v2h2v1H9v2H8v-2H6v-1h2V8z"/></svg>""",
    "refresh": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M3 8C3 5.23858 5.23858 3 8 3C9.63527 3 11.0878 3.78495 12.0005 5H10C9.72386 5 9.5 5.22386 9.5 5.5C9.5 5.77614 9.72386 6 10 6H12.8904C12.8973 6.00014 12.9041 6.00014 12.911 6H13C13.2761 6 13.5 5.77614 13.5 5.5V2.5C13.5 2.22386 13.2761 2 13 2C12.7239 2 12.5 2.22386 12.5 2.5V4.03138C11.4009 2.78613 9.79253 2 8 2C4.68629 2 2 4.68629 2 8C2 11.3137 4.68629 14 8 14C11.1301 14 13.6999 11.6035 13.9756 8.54488C14.0003 8.26985 13.7975 8.0268 13.5225 8.00202C13.2474 7.97723 13.0044 8.1801 12.9796 8.45512C12.75 11.003 10.6079 13 8 13C5.23858 13 3 10.7614 3 8Z"/></svg>""",
    "theme": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M8 1.00195C6.61553 1.00195 5.26216 1.4125 4.11101 2.18167C2.95987 2.95084 2.06266 4.04409 1.53285 5.32317C1.00303 6.60225 0.86441 8.00972 1.13451 9.36759C1.4046 10.7255 2.07129 11.9727 3.05026 12.9517C4.02922 13.9307 5.27651 14.5974 6.63437 14.8675C7.99224 15.1375 9.3997 14.9989 10.6788 14.4691C11.9579 13.9393 13.0511 13.0421 13.8203 11.8909C14.5895 10.7398 15 9.38642 15 8.00195C15 6.14544 14.2625 4.36496 12.9498 3.05221C11.637 1.73945 9.85652 1.00195 8 1.00195ZM8 14.002V2.00195C9.5913 2.00195 11.1174 2.63409 12.2426 3.75931C13.3679 4.88453 14 6.41065 14 8.00195C14 9.59325 13.3679 11.1194 12.2426 12.2446C11.1174 13.3698 9.5913 14.002 8 14.002Z"/></svg>""",
    "error": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M8 1.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13zM.5 8a7.5 7.5 0 1 1 15 0 7.5 7.5 0 0 1-15 0zm6.98-2.97h1.04l.02 4.02h-1.1L7.48 5.03zm.52 6.06c.41 0 .74-.32.74-.72 0-.4-.33-.72-.74-.72-.4 0-.74.32-.74.72 0 .4.34.72.74.72z"/></svg>""",
    "warning": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.56 1h.88l6.54 12.26-.44.74H1.44L1 13.26 7.56 1zM8 2.28 2.28 13H13.7L8 2.28zM8.625 12v-1h-1.25v1h1.25zm-1.222-5.962l.063 4.1h1.068l.063-4.1h-1.194z"/></svg>""",
    "chevron_right": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M10.072 8.024L5.715 3.667l.618-.62L11 7.716v.618L6.333 13l-.618-.619 4.357-4.357z"/></svg>""",
    "chevron_down": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.976 10.072l4.357-4.357.62.618L8.284 11h-.618L3 6.333l.619-.618 4.357 4.357z"/></svg>""",
    "file": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M13.71 4.29l-3-3L10 1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1V5l-.29-.71zM10 2.41L12.59 5H10V2.41zM4 14V2h5v4h4v8H4z"/></svg>""",
    "circle": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><circle cx="8" cy="8" r="3.5" fill="transparent" stroke="currentColor" stroke-width="1.5"/></svg>""",
    "file_count": """<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M7.5 22.5H17.595C17.07 23.4 16.11 24 15 24H7.5C4.185 24 1.5 21.315 1.5 18V6C1.5 4.89 2.1 3.93 3 3.405V18C3 20.475 5.025 22.5 7.5 22.5ZM21 8.121V18C21 19.6545 19.6545 21 18 21H7.5C5.8455 21 4.5 19.6545 4.5 18V3C4.5 1.3455 5.8455 0 7.5 0H12.879C13.4715 0 14.0505 0.24 14.4705 0.6585L20.3415 6.5295C20.766 6.954 21 7.5195 21 8.121ZM13.5 6.75C13.5 7.164 13.8375 7.5 14.25 7.5H19.1895L13.5 1.8105V6.75ZM19.5 18V9H14.25C13.0095 9 12 7.9905 12 6.75V1.5H7.5C6.672 1.5 6 2.1735 6 3V18C6 18.8265 6.672 19.5 7.5 19.5H18C18.828 19.5 19.5 18.8265 19.5 18Z"/></svg>""",
    "folder_count": """<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M3.5 3C2.67157 3 2 3.67157 2 4.5V5H5.08579C5.21839 5 5.34557 4.94732 5.43934 4.85355L6.29289 4L5.43934 3.14645C5.34557 3.05268 5.21839 3 5.08579 3H3.5ZM1 4.44118C1 4.4252 1.00075 4.4094 1.00221 4.39381C1.05785 3.06235 2.15486 2 3.5 2H5.08579C5.48361 2 5.86514 2.15804 6.14645 2.43934L7.20711 3.5H10.5C11.8807 3.5 13 4.61929 13 6V9.5C13 10.8807 11.8807 12 10.5 12H3.5C2.11929 12 1 10.8807 1 9.5V4.44118ZM7.20711 4.5L6.14645 5.56066C5.86514 5.84196 5.48361 6 5.08579 6H2V9.5C2 10.3284 2.67157 11 3.5 11H10.5C11.3284 11 12 10.3284 12 9.5V6C12 5.17157 11.3284 4.5 10.5 4.5H7.20711ZM14.0002 6C14.6074 6.4561 15.0002 7.18227 15.0002 8.00018V9.50018C15.0002 11.9855 12.9855 14.0002 10.5002 14.0002H5.50018C4.68227 14.0002 3.9561 13.6074 3.5 13.0002H10.5002C12.4332 13.0002 14.0002 11.4332 14.0002 9.50018V6Z"/></svg>"""
}

# ==============================================================================
# QSS Themes
# ==============================================================================
DARK_THEME = """
* { outline: none; } /* Universally remove dotted focus outlines */

QWidget#MainWindow { background-color: #252526; color: #cccccc; font-family: "Segoe UI", Arial, sans-serif; font-size: 11px; }

/* Status Bar is deep sleek grey to anchor the bottom */
QWidget#StatusBar { background-color: #181818; border-top: 1px solid #333333; }
QLabel#StatusText { color: #cccccc; font-family: "Segoe UI", Arial, sans-serif; font-size: 11px; }

/* Section Headers subtly lighter than the tree to create visual depth */
QWidget#SectionHeader { background-color: #333333; border-top: 1px solid #3c3c3c; }

QPushButton { background: transparent; border: none; color: #cccccc; padding: 2px; border-radius: 3px; }
QPushButton:hover { background-color: #444444; }
QPushButton:disabled { color: #555555; background: transparent; opacity: 0.5; }

QLabel#HeaderLabel { font-size: 11px; font-weight: bold; color: #cccccc; border: none; }
QLabel#TimelineAction { color: #cccccc; font-family: "Segoe UI", Arial, sans-serif; font-size: 11px;}
QLabel#TimelineTime { color: #969696; font-family: "Segoe UI", Arial, sans-serif; font-size: 10px; }

QSplitter::handle:vertical { background: transparent; height: 1px; }

QTreeView, QListWidget { 
    background-color: #252526; 
    border: none; 
    color: #cccccc; 
    font-family: "Segoe UI", Arial, sans-serif; 
    font-size: 11px; 
    /* These three lines color the entire row uniformly */
    selection-background-color: #37373d;
    selection-color: #ffffff;
    show-decoration-selected: 1; 
}
QTreeView::item, QListWidget::item { padding: 4px 0px; margin: 0px; border: none; }
QTreeView::item:hover, QListWidget::item:hover { background-color: #2a2d2e; }
QTreeView::item:selected, QListWidget::item:selected { background-color: #37373d; color: #ffffff; border: none; }

/* Custom Editor Styling (Professional VS Code look during rename) */
QTreeView QLineEdit {
    background-color: #252526;
    color: #cccccc;
    border: 1px solid #007fd4;
    padding: 0px 2px;
    selection-background-color: #04395e;
}

QMenu { 
    background-color: #252526; 
    color: #cccccc; 
    border: 1px solid #454545; 
    font-family: "Segoe UI", Arial, sans-serif; 
    font-size: 11px; 
    padding: 4px 0px; /* <-- This is the magic line that kills the Windows gutter */
}
QMenu::item { 
    background-color: transparent;
    padding: 4px 24px 4px 20px; 
    margin: 0px;
}
QMenu::item:selected { 
    background-color: #094771; 
}
QMenu::separator { 
    height: 1px; 
    background: #454545; 
    margin: 4px 0px; 
}

QScrollBar:vertical { border: none; background: transparent; width: 12px; margin: 0px; }
QScrollBar::handle:vertical { background: rgba(121, 121, 121, 0.4); min-height: 20px; }
QScrollBar::handle:vertical:hover { background: rgba(100, 100, 100, 0.7); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
"""

LIGHT_THEME = """
* { outline: none; } /* Universally remove dotted focus outlines */

QWidget#MainWindow { background-color: #f3f3f3; color: #333333; font-family: "Segoe UI", Arial, sans-serif; font-size: 11px; }

/* Status Bar uses iconic Fluent Blue in Light Mode */
QWidget#StatusBar { background-color: #0078d4; border-top: none; }
QLabel#StatusText { color: #ffffff; font-family: "Segoe UI", Arial, sans-serif; font-size: 11px; }

/* Section Headers subtly darker than tree to create visual depth */
QWidget#SectionHeader { background-color: #e5e5e5; border-top: 1px solid #cccccc; }

QPushButton { background: transparent; border: none; color: #333333; padding: 2px; border-radius: 3px; }
QPushButton:hover { background-color: #d4d4d4; }
QPushButton:disabled { color: #a0a0a0; background: transparent; }

QLabel#HeaderLabel { font-size: 11px; font-weight: bold; color: #555555; border: none; }
QLabel#TimelineAction { color: #333333; font-family: "Segoe UI", Arial, sans-serif; font-size: 11px;}
QLabel#TimelineTime { color: #666666; font-family: "Segoe UI", Arial, sans-serif; font-size: 10px; }

QSplitter::handle:vertical { background: transparent; height: 1px; }

QTreeView, QListWidget { 
    background-color: #f3f3f3; 
    border: none; 
    color: #333333; 
    font-family: "Segoe UI", Arial, sans-serif; 
    font-size: 11px; 
    /* These three lines color the entire row uniformly */
    selection-background-color: #d7ebfa; 
    selection-color: #000000;
    show-decoration-selected: 1; 
}
QTreeView::item, QListWidget::item { padding: 4px 0px; margin: 0px; border: none; }
QTreeView::item:hover, QListWidget::item:hover { background-color: #e8e8e8; }

/* EXTREMELY SOOTHING LIGHT MODE SELECTION (Soft Blue background, Dark Text) */
QTreeView::item:selected, QListWidget::item:selected { background-color: #d7ebfa; color: #000000; border: none; }

/* Custom Editor Styling (Professional VS Code look during rename) */
QTreeView QLineEdit {
    background-color: #ffffff;
    color: #1f1f1f;
    border: none;
    padding: 1px 4px;
}

QMenu { 
    background-color: #f2f2f2; 
    color: #333333; 
    border: 1px solid #d4d4d4; 
    font-family: "Segoe UI", Arial, sans-serif; 
    font-size: 11px; 
    padding: 4px 0px; /* <-- This is the magic line that kills the Windows gutter */
}
QMenu::item { 
    background-color: transparent;
    padding: 4px 24px 4px 20px; 
    margin: 0px;
}
QMenu::item:selected { 
    background-color: #d7ebfa; 
    color: #000000; 
}
QMenu::separator { 
    height: 1px; 
    background: #d4d4d4; 
    margin: 4px 0px; 
}

QScrollBar:vertical { border: none; background: transparent; width: 12px; margin: 0px; }
QScrollBar::handle:vertical { background: rgba(100, 100, 100, 0.4); min-height: 20px; }
QScrollBar::handle:vertical:hover { background: rgba(100, 100, 100, 0.7); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
"""

# ==============================================================================
# Custom Widgets
# ==============================================================================

class EnterpriseConfirmDialog(QDialog):
    """ VS Code Style Flat Confirmation Dialog """
    def __init__(self, title, text, parent=None, is_dark_mode=True):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(380)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 15)
        layout.setSpacing(20)
        
        lbl_text = QLabel(text)
        lbl_text.setWordWrap(True)
        lbl_text.setStyleSheet("font-size: 12px;")
        layout.addWidget(lbl_text)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_delete = QPushButton("Delete")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        
        if is_dark_mode:
            self.setStyleSheet("QDialog { background-color: #252526; color: #cccccc; font-family: 'Segoe UI'; border: 1px solid #454545; } QLabel { color: #cccccc; font-family: 'Segoe UI'; }")
            btn_style = """
                QPushButton { background-color: #333333; color: #cccccc; border: 1px solid #3c3c3c; padding: 6px 16px; border-radius: 2px; }
                QPushButton:hover { background-color: #444444; }
            """
            btn_delete_style = """
                QPushButton { background-color: #007acc; color: #ffffff; border: none; padding: 6px 16px; border-radius: 2px; }
                QPushButton:hover { background-color: #005f9e; }
            """
        else:
            self.setStyleSheet("QDialog { background-color: #f3f3f3; color: #333333; font-family: 'Segoe UI'; border: 1px solid #cccccc; } QLabel { color: #333333; font-family: 'Segoe UI'; }")
            btn_style = """
                QPushButton { background-color: #e5e5e5; color: #333333; border: 1px solid #cccccc; padding: 6px 16px; border-radius: 2px; }
                QPushButton:hover { background-color: #d4d4d4; }
            """
            btn_delete_style = """
                QPushButton { background-color: #0078d4; color: #ffffff; border: none; padding: 6px 16px; border-radius: 2px; }
                QPushButton:hover { background-color: #005a9e; }
            """
            
        self.btn_cancel.setStyleSheet(btn_style)
        self.btn_delete.setStyleSheet(btn_delete_style)
        
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_delete.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)


class AdvancedItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        return QSize(size.width(), 22)

    def paint(self, painter, option, index):
        # 1. Paint the standard item background, icon, and text first
        super().paint(painter, option, index)
        
        # 2. Check for custom status mapping
        status = index.data(ROLE_STATUS)
        if status and status != "None":
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Map statuses to VS Code colors
            colors = {
                "Healthy": QColor("#89d185"),  # Green
                "Warning": QColor("#cca700"),  # Yellow
                "Error": QColor("#f48771"),    # Red
                "Running": QColor("#3794ff")   # Blue
            }
            
            color = colors.get(status)
            if color:
                radius = 4
                rect = option.rect
                
                # Align the circle purely to the right edge of the tree
                x = rect.right() - (radius * 2) - 10
                y = rect.top() + (rect.height() - (radius * 2)) // 2
                
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(x, y, radius * 2, radius * 2)
                
            painter.restore()

class ExplorerProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        return True

class TimelineItemWidget(QWidget):
    def __init__(self, action_text, time_text, username, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 2, 10, 2)
        layout.setSpacing(8)
        
        self.lbl_icon = QLabel()
        self.lbl_action = QLabel(action_text)
        self.lbl_action.setObjectName("TimelineAction")
        
        # Username and time pushed to the far right on the exact same line
        self.lbl_subtitle = QLabel(f"{username} • {time_text}")
        self.lbl_subtitle.setObjectName("TimelineTime")
        self.lbl_subtitle.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        layout.addWidget(self.lbl_icon)
        layout.addWidget(self.lbl_action)
        layout.addStretch()
        layout.addWidget(self.lbl_subtitle)
        
    def update_theme(self, get_svg_icon_func):
        self.lbl_icon.setPixmap(get_svg_icon_func("circle").pixmap(14, 14))

class SectionHeader(QWidget):
    """ VS Code style Section Header (entire widget is clickable) """
    toggled = pyqtSignal()

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("SectionHeader")
        self.setFixedHeight(24)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 5, 0)
        layout.setSpacing(2)
        
        self.btn_toggle = QPushButton()
        self.btn_toggle.setFixedSize(22, 22)
        self.btn_toggle.clicked.connect(self.toggled.emit)
        
        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("HeaderLabel")
        
        layout.addWidget(self.btn_toggle)
        layout.addWidget(self.lbl_title)
        
        self.right_layout = QHBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(2)
        
        layout.addStretch()
        layout.addLayout(self.right_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggled.emit()
            
    def add_action_button(self, btn):
        self.right_layout.addWidget(btn)
        
    def set_icon(self, icon):
        self.btn_toggle.setIcon(icon)


class VSCodeExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = "explorer_config.json"
        self.is_dark_mode = True
        
        self.init_ui()
        self.apply_theme()
        
        self.load_config()

    def get_svg_icon(self, svg_key, override_color=None):
        color = override_color if override_color else ("#cccccc" if self.is_dark_mode else "#424242")
        svg_str = SVGS.get(svg_key, "").replace("currentColor", color)
        
        renderer = QSvgRenderer(QByteArray(svg_str.encode('utf-8')))
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        renderer.render(painter)
        painter.end()
        
        return QIcon(pixmap)

    def init_ui(self):
        self.setObjectName("MainWindow")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumWidth(250)
        self.resize(300, 650)
        self.setWindowTitle("Explorer UI")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ---------------------------------------------------------
        # SPLITTER WIDGET
        # ---------------------------------------------------------
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False) 

        # --- TOP SECTION (Projects) ---
        self.proj_container = QWidget()
        proj_layout = QVBoxLayout(self.proj_container)
        proj_layout.setContentsMargins(0, 0, 0, 0)
        proj_layout.setSpacing(0)

        self.proj_header = SectionHeader("Projects")
        self.proj_header.setStyleSheet("border-top: none;") # Flush with the top of the window
        self.proj_header.toggled.connect(self.toggle_projects)
        
        self.btn_new_file = QPushButton()
        self.btn_new_folder = QPushButton()
        self.btn_refresh = QPushButton()
        self.btn_theme = QPushButton()

        for btn, tooltip, icon_type in [
            (self.btn_new_file, "New File...", "new_file"),
            (self.btn_new_folder, "New Folder...", "new_folder"),
            (self.btn_refresh, "Refresh Explorer", "refresh"),
            (self.btn_theme, "Toggle Theme", "theme")
        ]:
            if btn != self.btn_new_file:
                btn.setToolTip(tooltip)
            btn.setFixedSize(22, 22)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("icon_type", icon_type)
            self.proj_header.add_action_button(btn)
            
        proj_layout.addWidget(self.proj_header)

        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(12)
        self.tree.setRootIsDecorated(True)
        self.tree.setAnimated(True)
        self.tree.setUniformRowHeights(True)
        self.tree.setTextElideMode(Qt.ElideRight) 
        self.tree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel) 
        self.tree.setItemDelegate(AdvancedItemDelegate(self.tree))
        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        proj_layout.addWidget(self.tree)

        # --- BOTTOM SECTION (Timeline) ---
        self.timeline_container = QWidget()
        timeline_layout = QVBoxLayout(self.timeline_container)
        timeline_layout.setContentsMargins(0, 0, 0, 0)
        timeline_layout.setSpacing(0)

        self.timeline_header = SectionHeader("Timeline")
        self.timeline_header.toggled.connect(self.toggle_timeline)
        timeline_layout.addWidget(self.timeline_header)

        self.timeline_list = QListWidget()
        # Changed to SingleSelection so clicking gives a beautiful, clean VS Code selection background
        self.timeline_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.timeline_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        timeline_layout.addWidget(self.timeline_list)

        # Add containers to Splitter (Index 0 is Splitter in main_layout)
        self.splitter.addWidget(self.proj_container)
        self.splitter.addWidget(self.timeline_container)
        self.main_layout.addWidget(self.splitter) 

        # --- SPACER WIDGET (Index 1 in main_layout) ---
        self.bottom_spacer = QWidget()
        self.bottom_spacer.setStyleSheet("background-color: transparent;")
        self.bottom_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.bottom_spacer)

        # --- STATUS BAR (Index 2 in main_layout) ---
        self.status_widget = QWidget()
        self.status_widget.setAttribute(Qt.WA_StyledBackground, True) # CRITICAL for rendering QSS boundaries on QWidgets
        self.status_widget.setObjectName("StatusBar")
        self.status_widget.setFixedHeight(24)
        status_layout = QHBoxLayout(self.status_widget)
        status_layout.setContentsMargins(10, 0, 10, 0)
        status_layout.setSpacing(4) 

        self.lbl_err_icon = QLabel()
        self.lbl_err_text = QLabel("0")
        self.lbl_err_text.setObjectName("StatusText")

        self.lbl_warn_icon = QLabel()
        self.lbl_warn_text = QLabel("0")
        self.lbl_warn_text.setObjectName("StatusText")

        self.lbl_folder_icon = QLabel()
        self.lbl_folder_text = QLabel("0")
        self.lbl_folder_text.setObjectName("StatusText")

        self.file_count_widget = QWidget()
        fc_layout = QHBoxLayout(self.file_count_widget)
        fc_layout.setContentsMargins(6, 0, 0, 0)
        fc_layout.setSpacing(4)
        self.lbl_file_icon = QLabel()
        self.lbl_file_text = QLabel("0")
        self.lbl_file_text.setObjectName("StatusText")
        fc_layout.addWidget(self.lbl_file_icon)
        fc_layout.addWidget(self.lbl_file_text)
        
        self.file_count_widget.hide()

        status_layout.addWidget(self.lbl_err_icon)
        status_layout.addWidget(self.lbl_err_text)
        status_layout.addSpacing(6) 
        status_layout.addWidget(self.lbl_warn_icon)
        status_layout.addWidget(self.lbl_warn_text)
        status_layout.addSpacing(6)

        status_layout.addWidget(self.lbl_folder_icon)
        status_layout.addWidget(self.lbl_folder_text)
        
        status_layout.addWidget(self.file_count_widget)

        status_layout.addStretch()
        
        self.main_layout.addWidget(self.status_widget)

        # --- SET INITIAL VISUAL STATE ---
        self.tree.show() 
        self.proj_container.setMaximumHeight(16777215)
        self.timeline_list.hide() 
        self.timeline_container.setMaximumHeight(24)
        
        self.update_layout_states()
        self.update_status_icons()

        # Connections & Setup
        self.btn_new_file.clicked.connect(lambda: self.add_node(is_folder=False))
        self.btn_new_folder.clicked.connect(lambda: self.add_node(is_folder=True))
        self.btn_refresh.clicked.connect(self.load_config)
        self.btn_theme.clicked.connect(self.toggle_theme)

        self.model = QStandardItemModel()
        self.proxy = ExplorerProxyModel()
        self.proxy.setSourceModel(self.model)
        self.tree.setModel(self.proxy)
        
        self.tree.selectionModel().selectionChanged.connect(self.update_button_states)
        self.setup_shortcuts()

    # ==============================================================================
    # COUNTS AND STATUS LOGIC
    # ==============================================================================
    def get_total_folders(self, parent_item=None):
        if parent_item is None:
            parent_item = self.model.invisibleRootItem()
        count = 0
        for row in range(parent_item.rowCount()):
            child = parent_item.child(row)
            if child.data(ROLE_TYPE) == "folder":
                count += 1
                count += self.get_total_folders(child)
        return count

    def get_folder_file_count(self, folder_item):
        count = 0
        for row in range(folder_item.rowCount()):
            if folder_item.child(row).data(ROLE_TYPE) == "file":
                count += 1
        return count

    def update_counts(self):
        total_folders = self.get_total_folders()
        self.lbl_folder_text.setText(str(total_folders))
        
        indexes = self.tree.selectionModel().selectedRows()
        if indexes:
            source_idx = self.proxy.mapToSource(indexes[0])
            item = self.model.itemFromIndex(source_idx)
            if item and item.data(ROLE_TYPE) == "folder":
                self.file_count_widget.show()
                file_count = self.get_folder_file_count(item)
                self.lbl_file_text.setText(str(file_count))
            else:
                self.file_count_widget.hide()
        else:
            self.file_count_widget.hide()

    def update_status_counts(self):
        err_count = 0
        warn_count = 0
        
        def count_statuses(parent_item):
            nonlocal err_count, warn_count
            for row in range(parent_item.rowCount()):
                child = parent_item.child(row)
                status = child.data(ROLE_STATUS)
                if status == "Error":
                    err_count += 1
                elif status == "Warning":
                    warn_count += 1
                
                # Recursively check inside folders
                if child.data(ROLE_TYPE) == "folder":
                    count_statuses(child)
                
        count_statuses(self.model.invisibleRootItem())
        self.lbl_err_text.setText(str(err_count))
        self.lbl_warn_text.setText(str(warn_count))

    # ==============================================================================
    # DYNAMIC LAYOUT MANAGEMENT (Fixes Accordion Physics)
    # ==============================================================================
    def update_layout_states(self):
        proj_open = not self.tree.isHidden()
        time_open = not self.timeline_list.isHidden()

        if proj_open and time_open:
            self.bottom_spacer.hide()
            self.main_layout.setStretch(0, 1) 
            self.main_layout.setStretch(1, 0) 
            self.splitter.setStretchFactor(0, 1)
            self.splitter.setStretchFactor(1, 1)
        elif proj_open and not time_open:
            self.bottom_spacer.hide()
            self.main_layout.setStretch(0, 1)
            self.main_layout.setStretch(1, 0)
            self.splitter.setStretchFactor(0, 1)
            self.splitter.setStretchFactor(1, 0)
        elif not proj_open and time_open:
            self.bottom_spacer.hide()
            self.main_layout.setStretch(0, 1) 
            self.main_layout.setStretch(1, 0)
            self.splitter.setStretchFactor(0, 0)
            self.splitter.setStretchFactor(1, 1)
        else:
            # Both closed
            self.bottom_spacer.show()
            self.main_layout.setStretch(0, 0) 
            self.main_layout.setStretch(1, 1) 
            self.splitter.setStretchFactor(0, 0)
            self.splitter.setStretchFactor(1, 0)

    def toggle_projects(self):
        is_visible = self.tree.isHidden()
        self.tree.setVisible(is_visible)
        
        if is_visible:
            self.proj_container.setMaximumHeight(16777215)
        else:
            self.proj_container.setMaximumHeight(24)
            
        self.update_layout_states()
        self.update_status_icons()

    def toggle_timeline(self):
        is_visible = self.timeline_list.isHidden()
        self.timeline_list.setVisible(is_visible)
        
        if is_visible:
            self.timeline_container.setMaximumHeight(16777215)
        else:
            self.timeline_container.setMaximumHeight(24)
            
        self.update_layout_states()
        self.update_status_icons()

    # ==============================================================================
    # CORE LOGIC
    # ==============================================================================
    def log_timeline_event(self, action_name):
        timestamp = time.strftime("%I:%M %p")
        username = getpass.getuser()

        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 26))

        widget = TimelineItemWidget(
            action_name,
            timestamp,
            username
        )
        widget.update_theme(self.get_svg_icon)

        self.timeline_list.insertItem(0, item)
        self.timeline_list.setItemWidget(item, widget)

    def update_button_states(self, selected=None, deselected=None):
        indexes = self.tree.selectionModel().selectedRows()
        
        if self.get_total_folders() == 0:
            self.btn_new_file.setEnabled(False)
            self.btn_new_file.setToolTip("Create a folder first")
        elif not indexes:
            self.btn_new_file.setEnabled(False)
            self.btn_new_file.setToolTip("Select a folder to create a file")
        else:
            self.btn_new_file.setEnabled(True)
            self.btn_new_file.setToolTip("New File...")
            
        self.update_action_icons()
        self.update_counts()

    def update_status_icons(self):
        icon_size = QSize(14, 14)
        
        # When Status Bar is Blue (Light Mode), force icons to be White for pristine contrast
        if self.is_dark_mode:
            err_color = "#f48771"
            warn_color = "#cca700"
            default_color = "#cccccc"
            header_color = "#cccccc"
        else:
            err_color = "#ffffff"
            warn_color = "#ffffff"
            default_color = "#ffffff"
            header_color = "#555555"

        self.lbl_err_icon.setPixmap(self.get_svg_icon("error", err_color).pixmap(icon_size))
        self.lbl_warn_icon.setPixmap(self.get_svg_icon("warning", warn_color).pixmap(icon_size))
        
        self.lbl_folder_icon.setPixmap(self.get_svg_icon("folder_count", default_color).pixmap(icon_size))
        self.lbl_file_icon.setPixmap(self.get_svg_icon("file_count", default_color).pixmap(icon_size))
        
        self.proj_header.set_icon(self.get_svg_icon("chevron_down" if not self.tree.isHidden() else "chevron_right", header_color))
        self.timeline_header.set_icon(self.get_svg_icon("chevron_down" if not self.timeline_list.isHidden() else "chevron_right", header_color))

    def update_action_icons(self):
        disabled_color = "#555555" if self.is_dark_mode else "#a0a0a0"
        active_color = "#cccccc" if self.is_dark_mode else "#333333"
        
        for btn in [self.btn_new_file, self.btn_new_folder, self.btn_refresh, self.btn_theme]:
            icon_type = btn.property("icon_type")
            color = disabled_color if not btn.isEnabled() else active_color
            btn.setIcon(self.get_svg_icon(icon_type, override_color=color))

    def generate_file_icon(self, filename, is_folder):
        if is_folder:
            return self.get_svg_icon("new_folder", "#dcb67a") 
        elif filename.endswith(".json"):
            return self.get_svg_icon("file", "#41b883")  
        elif filename.endswith(".py"):
            return self.get_svg_icon("file", "#3776ab")  
        else:
            return self.get_svg_icon("file") 

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
        
        def update_icons_recursively(parent_item):
            for row in range(parent_item.rowCount()):
                child = parent_item.child(row)
                is_folder = (child.data(ROLE_TYPE) == "folder")
                child.setIcon(self.generate_file_icon(child.text(), is_folder))
                update_icons_recursively(child)
                
        update_icons_recursively(self.model.invisibleRootItem())
        
        for i in range(self.timeline_list.count()):
            item = self.timeline_list.item(i)
            widget = self.timeline_list.itemWidget(item)
            if widget:
                widget.update_theme(self.get_svg_icon)

    def apply_theme(self):
        self.setStyleSheet(DARK_THEME if self.is_dark_mode else LIGHT_THEME)
        self.update_action_icons()
        self.update_status_icons()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("F2"), self, self.edit_selected)
        QShortcut(QKeySequence("Delete"), self, self.delete_selected)

    def set_item_status(self, item, status):
        item.setData(status, ROLE_STATUS)
        self.log_timeline_event(f"Set '{item.text()}' to {status}")
        self.save_config()
        self.update_status_counts()

    def show_context_menu(self, position):
        indexes = self.tree.selectionModel().selectedRows()
        if not indexes:
            return
            
        source_idx = self.proxy.mapToSource(indexes[0])
        item = self.model.itemFromIndex(source_idx)
        is_folder = (item.data(ROLE_TYPE) == "folder")

        menu = QMenu()

        if not is_folder:
            run_act = menu.addAction("Run Tool")
            run_act.triggered.connect(lambda checked=False, i=item: self.log_timeline_event(f"Ran '{i.text()}'"))
            
        status_menu = menu.addMenu("Set Status")
        for status in ["Healthy", "Warning", "Error", "Running", "None"]:
            act = status_menu.addAction(status)
            act.triggered.connect(lambda checked=False, s=status, i=item: self.set_item_status(i, s))
            
        menu.addSeparator()
        
        rename_act = menu.addAction("Rename (F2)")
        rename_act.triggered.connect(self.edit_selected)
        
        delete_text = "Delete Folder" if is_folder else "Delete Tool"
        delete_act = menu.addAction(delete_text)
        delete_act.triggered.connect(self.delete_selected)

        menu.exec_(self.tree.viewport().mapToGlobal(position))

    def add_node(self, is_folder):
        parent_item = self.model.invisibleRootItem()
        
        # Structure Logic:
        # 1. Folders are ALWAYS created at the root level.
        # 2. Files MUST be created inside a folder.
        if not is_folder:
            indexes = self.tree.selectionModel().selectedRows()
            if indexes:
                selected_idx = self.proxy.mapToSource(indexes[0])
                item = self.model.itemFromIndex(selected_idx)
                if item.data(ROLE_TYPE) == "folder":
                    parent_item = item
                else:
                    parent_item = item.parent() or self.model.invisibleRootItem()
            
            # Catch/fallback: Prevent creating a file at the root completely
            if parent_item == self.model.invisibleRootItem():
                return

        new_item = QStandardItem("")
        item_type = "folder" if is_folder else "file"
        new_item.setData(item_type, ROLE_TYPE)
        new_item.setData("None", ROLE_STATUS) 
        new_item.setData(None, ROLE_OLD_NAME) 
        new_item.setIcon(self.generate_file_icon("", is_folder))
        
        parent_item.appendRow(new_item)
        
        if parent_item != self.model.invisibleRootItem():
            self.tree.expand(self.proxy.mapFromSource(parent_item.index()))
            
        new_idx = self.proxy.mapFromSource(new_item.index())
        self.tree.setCurrentIndex(new_idx)
        self.tree.edit(new_idx)
        
        self.update_button_states()
        self.update_counts()

    def on_item_edited(self, item):
        self.model.blockSignals(True)
        
        name = item.text().strip()
        item_type = item.data(ROLE_TYPE)
        is_folder = (item_type == "folder")
        
        if not name:
            name = "Unnamed Folder" if is_folder else "Unnamed File"
            item.setText(name)
            
        item.setIcon(self.generate_file_icon(name, is_folder))
        
        old_name = item.data(ROLE_OLD_NAME)
        if not old_name:
            self.log_timeline_event(f"Created '{name}'")
        elif old_name != name:
            self.log_timeline_event(f"Renamed to '{name}'")
            
        item.setData(name, ROLE_OLD_NAME)
        self.model.blockSignals(False)
        self.save_config()

    def edit_selected(self):
        indexes = self.tree.selectionModel().selectedRows()
        if indexes:
            self.tree.edit(indexes[0])

    def delete_selected(self):
        indexes = self.tree.selectionModel().selectedRows()
        if not indexes:
            return
            
        source_idx = self.proxy.mapToSource(indexes[0])
        item = self.model.itemFromIndex(source_idx)
        name = item.text()
        
        # Open Enterprise Grade Custom Dialog
        dialog = EnterpriseConfirmDialog(
            "Confirm Deletion", 
            f"Are you sure you want to delete '{name}' and its contents? This action cannot be undone.",
            self,
            self.is_dark_mode
        )
        
        if dialog.exec_() == QDialog.Accepted:
            self.log_timeline_event(f"Deleted '{name}'")
            
            parent = item.parent() or self.model.invisibleRootItem()
            parent.removeRow(source_idx.row())
            
            self.save_config()
            self.update_button_states()
            self.update_status_counts()
            self.update_counts()

    def save_config(self):
        try:
            self.model.itemChanged.disconnect(self.on_item_edited)
        except TypeError:
            pass

        def serialize_node(parent_item):
            nodes = []

            for row in range(parent_item.rowCount()):
                child = parent_item.child(row)

                nodes.append({
                    "name": child.text(),
                    "type": child.data(ROLE_TYPE),
                    "status": child.data(ROLE_STATUS) or "None",
                    "created": child.data(ROLE_CREATED) or time.time(),
                    "children": serialize_node(child)
                })

            return nodes

        # ---------------------------------------------------------
        # Save Timeline
        # ---------------------------------------------------------
        timeline_events = []

        for i in range(self.timeline_list.count()):
            item = self.timeline_list.item(i)
            widget = self.timeline_list.itemWidget(item)

            if widget:
                timeline_events.append({
                    "action": widget.lbl_action.text(),
                    "time": widget.lbl_subtitle.text()
                })

        # ---------------------------------------------------------
        # Complete configuration
        # ---------------------------------------------------------
        data = {
            "tools": serialize_node(self.model.invisibleRootItem()),
            "timeline": timeline_events
        }

        try:
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

        self.model.itemChanged.connect(self.on_item_edited)

    def load_config(self):
        try:
            self.model.itemChanged.disconnect(self.on_item_edited)
        except TypeError:
            pass

        # Clear existing tree and timeline
        self.model.clear()
        self.timeline_list.clear()

        def deserialize_node(data_list, parent_item):
            for node_data in data_list:
                name = node_data.get("name", "Unknown")
                item_type = node_data.get("type", "file")
                is_folder = (item_type == "folder")

                item = QStandardItem(name)

                item.setIcon(
                    self.generate_file_icon(name, is_folder)
                )

                item.setData(item_type, ROLE_TYPE)
                item.setData(
                    node_data.get("status", "None"),
                    ROLE_STATUS
                )
                item.setData(name, ROLE_OLD_NAME)
                item.setData(
                    node_data.get("created", time.time()),
                    ROLE_CREATED
                )

                parent_item.appendRow(item)

                if "children" in node_data:
                    deserialize_node(
                        node_data["children"],
                        item
                    )

        # =========================================================
        # LOAD CONFIG FILE
        # =========================================================
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)

                # -------------------------------------------------
                # Load Explorer Tree
                # -------------------------------------------------
                deserialize_node(
                    data.get("tools", []),
                    self.model.invisibleRootItem()
                )

                # -------------------------------------------------
                # Load Timeline
                # -------------------------------------------------
                for event in data.get("timeline", []):
                    action = event.get("action", "")
                    subtitle = event.get("time", "")

                    item = QListWidgetItem()
                    item.setSizeHint(QSize(0, 26))

                    # Stored format:
                    # "username • timestamp"
                    if " • " in subtitle:
                        username, timestamp = subtitle.split(" • ", 1)
                    else:
                        username = getpass.getuser()
                        timestamp = subtitle

                    widget = TimelineItemWidget(
                        action,
                        timestamp,
                        username
                    )

                    widget.update_theme(self.get_svg_icon)

                    self.timeline_list.insertItem(0, item)
                    self.timeline_list.setItemWidget(item, widget)

            except Exception as e:
                print(f"Error loading config: {e}")

        # =========================================================
        # RESTORE UI STATE
        # =========================================================
        self.model.itemChanged.connect(self.on_item_edited)

        self.tree.expandAll()

        self.update_button_states()
        self.update_status_counts()
        self.update_counts()

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VSCodeExplorer()
    window.show()
    sys.exit(app.exec_())