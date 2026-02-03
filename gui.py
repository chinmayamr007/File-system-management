import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QMessageBox, QInputDialog, 
                             QLabel, QProgressBar, QTextEdit, QFrame, QGridLayout)
from vfs_engine import VirtualFileSystem 

class FileSystemManager(QWidget):
    def __init__(self):
        super().__init__()
        self.vfs = VirtualFileSystem() 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('🛡️ Cyber-Sentinel VFS Manager')
        self.setGeometry(100, 100, 950, 650)
        
        self.setStyleSheet("""
            QWidget { background-color: #1a1b26; color: #a9b1d6; font-family: 'Consolas', monospace; }
            QListWidget { background-color: #24283b; border: 2px solid #414868; border-radius: 8px; }
            QPushButton { background-color: #414868; border-radius: 5px; padding: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #7aa2f7; color: #1a1b26; }
            QProgressBar { border: 1px solid #414868; text-align: center; background: #24283b; }
            QProgressBar::chunk { background-color: #9ece6a; }
            QTextEdit { background-color: #16161e; color: #73daca; font-size: 11px; }
        """)

        main_layout = QHBoxLayout()

        # Left Panel: File Browser [cite: 31]
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("📂 INODE TABLE"))
        self.file_list = QListWidget()
        left_panel.addWidget(self.file_list)

        # Buttons [cite: 32]
        self.btn_create = QPushButton("✨ CREATE")
        self.btn_read = QPushButton("🔍 READ")
        self.btn_write = QPushButton("📝 WRITE")
        self.btn_delete = QPushButton("🗑️ DELETE")
        self.btn_props = QPushButton("ℹ️ PROPERTIES")

        for btn in [self.btn_create, self.btn_read, self.btn_write, self.btn_delete, self.btn_props]:
            left_panel.addWidget(btn)
        
        main_layout.addLayout(left_panel, 2)

        # Right Panel: Storage Map & Logs [cite: 34]
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("🧱 BLOCK ALLOCATION MAP"))
        
        self.block_grid = QFrame()
        self.grid_layout = QGridLayout(self.block_grid)
        self.grid_layout.setSpacing(2)
        self.blocks = []
        for i in range(256):
            label = QLabel()
            label.setFixedSize(12, 12)
            label.setStyleSheet("background-color: #414868; border-radius: 2px;")
            self.grid_layout.addWidget(label, i // 16, i % 16)
            self.blocks.append(label)
        
        right_panel.addWidget(self.block_grid)
        self.usage_bar = QProgressBar()
        self.usage_bar.setMaximum(256)
        right_panel.addWidget(self.usage_bar)
        
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        right_panel.addWidget(QLabel("📜 SYSTEM LOGS"))
        right_panel.addWidget(self.logs)

        main_layout.addLayout(right_panel, 3)
        self.setLayout(main_layout)

        # Connect Events
        self.btn_create.clicked.connect(self.create_file)
        self.btn_read.clicked.connect(self.read_file)
        self.btn_write.clicked.connect(self.write_file)
        self.btn_delete.clicked.connect(self.delete_file)
        self.btn_props.clicked.connect(self.show_properties)

        self.refresh_ui()

    def log(self, msg):
        self.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def refresh_ui(self):
        """Synchronizes GUI with the VFS state[cite: 35]."""
        self.file_list.clear()
        self.file_list.addItems(self.vfs.inodes.keys())
        stats = self.vfs.get_stats()
        self.usage_bar.setValue(stats['used_blocks'])
        
        for label in self.blocks: 
            label.setStyleSheet("background-color: #414868; border-radius: 2px;")
            
        for name, data in self.vfs.inodes.items():
            for b_idx in data.get('blocks', []):
                if b_idx < 256:
                    self.blocks[b_idx].setStyleSheet("background-color: #bb9af7; border: 1px solid #7aa2f7;")

    def create_file(self):
        name, ok = QInputDialog.getText(self, 'Input', 'Filename:')
        if ok and name:
            self.log(self.vfs.create(name))
            self.refresh_ui()

    def write_file(self):
        item = self.file_list.currentItem()
        if item:
            text, ok = QInputDialog.getMultiLineText(self, 'Input', 'Data:')
            if ok:
                self.log(self.vfs.write(item.text(), text))
                self.refresh_ui()

    def read_file(self):
        item = self.file_list.currentItem()
        if item:
            content = self.vfs.read(item.text())
            QMessageBox.information(self, "Data", content)
            self.log(f"Read operation: {item.text()}")

    def show_properties(self):
        """Displays Inode Metadata[cite: 33, 58]."""
        item = self.file_list.currentItem()
        if item:
            m = self.vfs.inodes.get(item.text())
            info = "\n".join([f"{k.upper()}: {v}" for k, v in m.items()])
            QMessageBox.information(self, "Properties", info)

    def delete_file(self):
        item = self.file_list.currentItem()
        if item:
            self.log(self.vfs.delete(item.text()))
            self.refresh_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileSystemManager()
    ex.show()
    sys.exit(app.exec_())
