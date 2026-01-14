#!/usr/bin/env python3
"""
BiteBabe Admin Editor - Ultimate Version
- Landing Page Editor (Restored)
- Table-based Product & Topping Editor
- Image Upload (Copy to assets)
- Theme Customizer
- Git Integration
"""

import sys
import json
import os
import shutil
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox,
    QFormLayout, QGroupBox, QMessageBox, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QColorDialog, QDialog, QDialogButtonBox,
    QScrollArea, QFrame, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

# --- Helper Functions ---
def load_json(path):
    if not path.exists():
        return {} if path.name != "products.json" and path.name != "toppings.json" and path.name != "features" else []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}

def save_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {path}: {e}")
        return False

# --- Dialogs ---
class ProductDialog(QDialog):
    def __init__(self, product=None, all_toppings=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Product" if product else "New Product")
        self.setModal(True)
        self.layout = QFormLayout(self)
        self.product_data = product or {}
        
        # Determine Project Root for Image Copying
        # Assuming admin_editor.py is in /Start/
        self.project_root = Path(__file__).parent.resolve()
        self.assets_dir = self.project_root / "assets" / "products"
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        self.id_input = QLineEdit(self.product_data.get('id', str(int(subprocess.check_output(['date', '+%s']).decode().strip()))))
        self.id_input.setReadOnly(True)
        self.name_input = QLineEdit(self.product_data.get('name', ''))
        self.category_input = QLineEdit(self.product_data.get('category', ''))
        self.price_input = QLineEdit(str(self.product_data.get('price', 0)))
        self.stock_input = QLineEdit(str(self.product_data.get('stock', 0)))
        self.max_order_input = QLineEdit(str(self.product_data.get('max_order', 10)))
        self.desc_input = QTextEdit(self.product_data.get('description', ''))
        self.image_input = QLineEdit(self.product_data.get('image', ''))
        
        # Image browse
        img_layout = QHBoxLayout()
        img_layout.addWidget(self.image_input)
        browse_btn = QPushButton("📂 Upload/Select Image")
        browse_btn.clicked.connect(self.upload_image)
        img_layout.addWidget(browse_btn)

        self.layout.addRow("ID:", self.id_input)
        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("Category:", self.category_input)
        self.layout.addRow("Price (Rp):", self.price_input)
        self.layout.addRow("Stock:", self.stock_input)
        self.layout.addRow("Max Order:", self.max_order_input)
        self.layout.addRow("Description:", self.desc_input)
        self.layout.addRow("Description:", self.desc_input)
        self.layout.addRow("Image:", img_layout)

        # Toppings Selection
        self.toppings_widget = QListWidget()
        self.toppings_widget.setMaximumHeight(150)
        current_toppings = self.product_data.get('toppings', [])
        
        for t in (all_toppings or []):
            item = QListWidgetItem(f"{t.get('name', 'Unknown')} (+{t.get('price', 0)})")
            item.setData(Qt.UserRole, t.get('id'))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if t.get('id') in current_toppings:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.toppings_widget.addItem(item)
            
        self.layout.addRow("Toppings:", self.toppings_widget)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def upload_image(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if f:
            try:
                # Copy file to assets/products/
                filename = os.path.basename(f)
                dest_path = self.assets_dir / filename
                shutil.copy2(f, dest_path)
                
                # Set relative path for JSON
                rel_path = f"assets/products/{filename}"
                self.image_input.setText(rel_path)
                QMessageBox.information(self, "Success", f"Image uploaded to {rel_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to upload image: {e}")
                self.image_input.setText(f) # Fallback to absolute

    def get_data(self):
        try: price = int(self.price_input.text())
        except: price = 0
        try: stock = int(self.stock_input.text())
        except: stock = 0
        try: max_order = int(self.max_order_input.text())
        except: max_order = 10
        
        # Get selected toppings
        selected_toppings = []
        for i in range(self.toppings_widget.count()):
            item = self.toppings_widget.item(i)
            if item.checkState() == Qt.Checked:
                selected_toppings.append(item.data(Qt.UserRole))

        return {
            "id": self.id_input.text(),
            "name": self.name_input.text(),
            "category": self.category_input.text(),
            "price": price,
            "stock": stock,
            "max_order": max_order,
            "description": self.desc_input.toPlainText(),
            "image": self.image_input.text(),
            "toppings": selected_toppings
        }

class ToppingDialog(QDialog):
    def __init__(self, topping=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Topping" if topping else "New Topping")
        self.topping_data = topping or {}
        self.layout = QFormLayout(self)
        
        self.id_input = QLineEdit(self.topping_data.get('id', f"top_{int(subprocess.check_output(['date', '+%s']).decode().strip())}"))
        self.name_input = QLineEdit(self.topping_data.get('name', ''))
        self.price_input = QLineEdit(str(self.topping_data.get('price', 0)))
        
        self.layout.addRow("ID:", self.id_input)
        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("Price:", self.price_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def get_data(self):
        try: price = int(self.price_input.text())
        except: price = 0
        return {
            "id": self.id_input.text(),
            "name": self.name_input.text(),
            "price": price
        }

# --- Tabs ---

class LandingPageTab(QWidget):
    def __init__(self, data_path, parent=None):
        super().__init__(parent)
        self.data_path = data_path
        self.layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        form_layout = QVBoxLayout(widget)
        
        # Hero Section
        hero = QGroupBox("Target: Hero Section")
        hero_lo = QFormLayout()
        self.hero_title = QLineEdit()
        self.hero_subtitle = QTextEdit()
        self.hero_subtitle.setMaximumHeight(60)
        self.hero_btn = QLineEdit()
        hero_lo.addRow("Title:", self.hero_title)
        hero_lo.addRow("Subtitle:", self.hero_subtitle)
        hero_lo.addRow("Button Text:", self.hero_btn)
        hero.setLayout(hero_lo)
        form_layout.addWidget(hero)

        # About Section
        about = QGroupBox("Target: About Section")
        about_lo = QFormLayout()
        self.about_enable = QCheckBox("Show About Section")
        self.about_title = QLineEdit()
        self.about_desc = QTextEdit()
        self.about_desc.setMaximumHeight(80)
        about_lo.addRow(self.about_enable)
        about_lo.addRow("Title:", self.about_title)
        about_lo.addRow("Description:", self.about_desc)
        about.setLayout(about_lo)
        form_layout.addWidget(about)

        # Features Section
        features_grp = QGroupBox("Target: Features (Max 3)")
        feats_lo = QVBoxLayout()
        self.feature_inputs = []
        for i in range(3):
            f_frame = QFrame()
            f_frame.setFrameShape(QFrame.StyledPanel)
            f_lo = QHBoxLayout(f_frame)
            icon = QLineEdit(); icon.setPlaceholderText("Emoji/Icon")
            title = QLineEdit(); title.setPlaceholderText("Title")
            desc = QLineEdit(); desc.setPlaceholderText("Description")
            f_lo.addWidget(QLabel(f"#{i+1}")); f_lo.addWidget(icon); f_lo.addWidget(title); f_lo.addWidget(desc)
            self.feature_inputs.append({'icon': icon, 'title': title, 'description': desc})
            feats_lo.addWidget(f_frame)
        features_grp.setLayout(feats_lo)
        form_layout.addWidget(features_grp)

        # SEO
        seo = QGroupBox("Target: SEO Metadata")
        seo_lo = QFormLayout()
        self.seo_title = QLineEdit()
        self.seo_desc = QTextEdit(); self.seo_desc.setMaximumHeight(60)
        seo_lo.addRow("Page Title:", self.seo_title)
        seo_lo.addRow("Meta Desc:", self.seo_desc)
        seo.setLayout(seo_lo)
        form_layout.addWidget(seo)

        # Footer
        foot = QGroupBox("Target: Footer")
        foot_lo = QFormLayout()
        self.foot_copy = QLineEdit()
        foot_lo.addRow("Copyright:", self.foot_copy)
        foot.setLayout(foot_lo)
        form_layout.addWidget(foot)

        form_layout.addStretch()
        scroll.setWidget(widget)
        self.layout.addWidget(scroll)

        save_btn = QPushButton("💾 Save Landing Page")
        save_btn.clicked.connect(self.save)
        self.layout.addWidget(save_btn)

        self.load()

    def load(self):
        data = load_json(self.data_path)
        
        # Hero
        h = data.get('hero', {})
        self.hero_title.setText(h.get('title',''))
        self.hero_subtitle.setPlainText(h.get('subtitle',''))
        self.hero_btn.setText(h.get('buttonText',''))
        
        # About
        a = data.get('about', {})
        self.about_enable.setChecked(a.get('enabled', False))
        self.about_title.setText(a.get('title',''))
        self.about_desc.setPlainText(a.get('description',''))

        # Features
        feats = data.get('features', [])
        for i, inputs in enumerate(self.feature_inputs):
            if i < len(feats):
                inputs['icon'].setText(feats[i].get('icon',''))
                inputs['title'].setText(feats[i].get('title',''))
                inputs['description'].setText(feats[i].get('description',''))

        # SEO
        s = data.get('seo', {})
        self.seo_title.setText(s.get('title',''))
        self.seo_desc.setPlainText(s.get('description',''))

        # Footer
        self.foot_copy.setText(data.get('footer', {}).get('copyright',''))

    def save(self):
        data = {
            "hero": {
                "title": self.hero_title.text(),
                "subtitle": self.hero_subtitle.toPlainText(),
                "buttonText": self.hero_btn.text(),
                "backgroundImage": ""
            },
            "about": {
                "enabled": self.about_enable.isChecked(),
                "title": self.about_title.text(),
                "description": self.about_desc.toPlainText(),
                "image": ""
            },
            "features": [],
            "seo": {
                "title": self.seo_title.text(),
                "description": self.seo_desc.toPlainText(),
                "keywords": ""
            },
            "footer": {"copyright": self.foot_copy.text()}
        }
        
        for inputs in self.feature_inputs:
            if inputs['title'].text():
                data['features'].append({
                    "icon": inputs['icon'].text(),
                    "title": inputs['title'].text(),
                    "description": inputs['description'].text()
                })
        
        if save_json(self.data_path, data):
            QMessageBox.information(self, "Success", "Landing Page Updated!")


class ProductsTab(QWidget):
    def __init__(self, data_path, parent=None):
        super().__init__(parent)
        self.data_path = data_path
        self.layout = QVBoxLayout(self)
        
        toolbar = QHBoxLayout()
        add_btn = QPushButton("➕ Add Product")
        add_btn.clicked.connect(self.add_product)
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_data)
        toolbar.addWidget(add_btn)
        toolbar.addWidget(refresh_btn)
        toolbar.addStretch()
        self.layout.addLayout(toolbar)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "Stock"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.doubleClicked.connect(self.edit_selected)
        self.layout.addWidget(self.table)
        
        actions_layout = QHBoxLayout()
        edit_btn = QPushButton("✏️ Edit Selected")
        edit_btn.clicked.connect(self.edit_selected)
        del_btn = QPushButton("🗑️ Delete Selected")
        del_btn.setStyleSheet("background-color: #ffcccc;")
        del_btn.clicked.connect(self.delete_selected)
        save_btn = QPushButton("💾 Save Changes")
        save_btn.setStyleSheet("font-weight: bold; background-color: #e6f7ff;")
        save_btn.clicked.connect(self.save_data)
        
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(del_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(save_btn)
        self.layout.addLayout(actions_layout)
        
        self.products = []
        self.load_data()
        
    def load_data(self):
        self.products = load_json(self.data_path)
        self.table.setRowCount(len(self.products))
        for i, p in enumerate(self.products):
            self.table.setItem(i, 0, QTableWidgetItem(str(p.get('id', ''))))
            self.table.setItem(i, 1, QTableWidgetItem(p.get('name', '')))
            self.table.setItem(i, 2, QTableWidgetItem(p.get('category', '')))
            self.table.setItem(i, 3, QTableWidgetItem(str(p.get('price', 0))))
            self.table.setItem(i, 4, QTableWidgetItem(str(p.get('stock', 0))))
            
    def add_product(self):
        all_toppings = load_json(self.data_path.parent / "toppings.json")
        dialog = ProductDialog(all_toppings=all_toppings, parent=self)
        if dialog.exec_():
            new_data = dialog.get_data()
            self.products.append(new_data)
            self.load_data_to_table_only()
            
    def edit_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        idx = rows[0].row()
        product = self.products[idx]
        
        all_toppings = load_json(self.data_path.parent / "toppings.json")
        dialog = ProductDialog(product, all_toppings, self)
        if dialog.exec_():
            self.products[idx] = dialog.get_data()
            self.load_data_to_table_only()
            
    def delete_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        if QMessageBox.question(self, "Confirm", "Delete selected product?") == QMessageBox.Yes:
            idx = rows[0].row()
            del self.products[idx]
            self.load_data_to_table_only()

    def load_data_to_table_only(self):
        self.table.setRowCount(len(self.products))
        for i, p in enumerate(self.products):
            self.table.setItem(i, 0, QTableWidgetItem(str(p.get('id', ''))))
            self.table.setItem(i, 1, QTableWidgetItem(p.get('name', '')))
            self.table.setItem(i, 2, QTableWidgetItem(p.get('category', '')))
            self.table.setItem(i, 3, QTableWidgetItem(str(p.get('price', 0))))
            self.table.setItem(i, 4, QTableWidgetItem(str(p.get('stock', 0))))

    def save_data(self):
        if save_json(self.data_path, self.products):
            QMessageBox.information(self, "Saved", "Products saved successfully!")

class ToppingsTab(QWidget):
    def __init__(self, data_path, parent=None):
        super().__init__(parent)
        self.data_path = data_path
        self.layout = QVBoxLayout(self)
        
        toolbar = QHBoxLayout()
        add_btn = QPushButton("➕ Add Topping")
        add_btn.clicked.connect(self.add_topping)
        toolbar.addWidget(add_btn)
        toolbar.addStretch()
        self.layout.addLayout(toolbar)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.doubleClicked.connect(self.edit_selected)
        self.layout.addWidget(self.table)
        
        actions = QHBoxLayout()
        save_btn = QPushButton("💾 Save Toppings")
        save_btn.clicked.connect(self.save_data)
        actions.addStretch()
        actions.addWidget(save_btn)
        self.layout.addLayout(actions)
        
        self.toppings = []
        self.load_data()

    def load_data(self):
        self.toppings = load_json(self.data_path)
        self.update_table()

    def update_table(self):
        self.table.setRowCount(len(self.toppings))
        for i, t in enumerate(self.toppings):
            self.table.setItem(i, 0, QTableWidgetItem(str(t.get('id', ''))))
            self.table.setItem(i, 1, QTableWidgetItem(t.get('name', '')))
            self.table.setItem(i, 2, QTableWidgetItem(str(t.get('price', 0))))

    def add_topping(self):
        dialog = ToppingDialog(parent=self)
        if dialog.exec_():
            self.toppings.append(dialog.get_data())
            self.update_table()

    def edit_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        idx = rows[0].row()
        dialog = ToppingDialog(self.toppings[idx], self)
        if dialog.exec_():
            self.toppings[idx] = dialog.get_data()
            self.update_table()

    def save_data(self):
        if save_json(self.data_path, self.toppings):
            QMessageBox.information(self, "Saved", "Toppings saved!")

class ThemeTab(QWidget):
    def __init__(self, data_path, parent=None):
        super().__init__(parent)
        self.data_path = data_path
        self.layout = QVBoxLayout(self)
        
        self.store_data = {}
        self.inputs = {}
        
        form_group = QGroupBox("Store Settings")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.slogan_input = QLineEdit()
        self.whatsapp_input = QLineEdit()
        
        form_layout.addRow("Store Name:", self.name_input)
        form_layout.addRow("Slogan:", self.slogan_input)
        form_layout.addRow("WhatsApp:", self.whatsapp_input)
        form_group.setLayout(form_layout)
        self.layout.addWidget(form_group)
        
        colors_group = QGroupBox("Theme Colors")
        colors_layout = QFormLayout()
        
        self.color_keys = ['primary', 'background', 'light', 'text', 'accent']
        self.color_widgets = {}
        
        for key in self.color_keys:
            h_layout = QHBoxLayout()
            line_edit = QLineEdit()
            btn = QPushButton("🎨")
            btn.setFixedWidth(40)
            btn.clicked.connect(lambda checked, k=key, le=line_edit: self.pick_color(k, le))
            h_layout.addWidget(line_edit)
            h_layout.addWidget(btn)
            self.color_widgets[key] = line_edit
            colors_layout.addRow(key.capitalize() + ":", h_layout)
            
        colors_group.setLayout(colors_layout)
        self.layout.addWidget(colors_group)
        
        save_btn = QPushButton("💾 Save Configuration")
        save_btn.clicked.connect(self.save)
        self.layout.addWidget(save_btn)
        
        self.layout.addStretch()
        self.load()

    def pick_color(self, key, line_edit):
        current_hex = line_edit.text()
        color = QColorDialog.getColor(QColor(current_hex) if current_hex else Qt.white, self)
        if color.isValid():
            line_edit.setText(color.name())
            line_edit.setStyleSheet(f"background-color: {color.name()}; color: {'white' if color.lightness() < 128 else 'black'}")

    def load(self):
        self.store_data = load_json(self.data_path)
        self.name_input.setText(self.store_data.get('name', ''))
        self.slogan_input.setText(self.store_data.get('slogan', ''))
        self.whatsapp_input.setText(self.store_data.get('whatsapp', ''))
        theme = self.store_data.get('theme', {})
        for key in self.color_keys:
            val = theme.get(key, '')
            self.color_widgets[key].setText(val)
            if val:
                try: self.color_widgets[key].setStyleSheet(f"background-color: {val}; color: {'white' if QColor(val).lightness() < 128 else 'black'}")
                except: pass

    def save(self):
        self.store_data['name'] = self.name_input.text()
        self.store_data['slogan'] = self.slogan_input.text()
        self.store_data['whatsapp'] = self.whatsapp_input.text()
        if 'theme' not in self.store_data: self.store_data['theme'] = {}
        for key in self.color_keys:
            self.store_data['theme'][key] = self.color_widgets[key].text()
        if save_json(self.data_path, self.store_data):
            QMessageBox.information(self, "Saved", "Store settings saved!")

class GitTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.status_label = QLabel("Git Status: Checking...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        self.layout.addWidget(self.status_label)
        controls = QGroupBox("Deploy Actions")
        c_layout = QFormLayout()
        self.remote_input = QLineEdit()
        self.remote_input.setPlaceholderText("https://github.com/username/repo.git")
        c_layout.addRow("Git Remote URL:", self.remote_input)
        btn_layout = QHBoxLayout()
        self.init_btn = QPushButton("Initialize Repo")
        self.init_btn.clicked.connect(self.git_init)
        self.push_btn = QPushButton("🚀 Save & Push to GitHub")
        self.push_btn.setStyleSheet("background-color: #d4edda; font-weight: bold; padding: 10px;")
        self.push_btn.clicked.connect(self.git_push_all)
        btn_layout.addWidget(self.init_btn)
        btn_layout.addWidget(self.push_btn)
        c_layout.addRow(btn_layout)
        controls.setLayout(c_layout)
        self.layout.addWidget(controls)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #2b2b2b; color: #f0f0f0; font-family: Monospace;")
        self.layout.addWidget(self.log_output)
        self.check_status()

    def log(self, text):
        self.log_output.append(text)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def run_cmd(self, cmd):
        self.log(f"$ {' '.join(cmd)}")
        try:
            # Set GIT_TERMINAL_PROMPT=0 to prevent git from hanging on credential prompts
            env = os.environ.copy()
            env["GIT_TERMINAL_PROMPT"] = "0"
            
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
            if res.stdout: self.log(res.stdout)
            if res.stderr: self.log(f"[INFO] {res.stderr}")
            return True, res.stdout
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else e.stdout
            self.log(f"Error: {error_msg}")
            return False, error_msg
        except Exception as e:
            self.log(str(e))
            return False, str(e)

    def check_status(self):
        if os.path.exists(".git"):
            self.status_label.setText("Git Status: Active Repo (Initialized)")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.init_btn.setEnabled(False)
            ok, out = self.run_cmd(["git", "remote", "get-url", "origin"])
            if ok: self.remote_input.setText(out.strip())
        else:
            self.status_label.setText("Git Status: Not Initialized")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.init_btn.setEnabled(True)

    def git_init(self):
        self.run_cmd(["git", "init"])
        self.run_cmd(["git", "add", "."])
        self.run_cmd(["git", "commit", "-m", "Initial commit"])
        self.run_cmd(["git", "branch", "-M", "main"])
        self.check_status()

    def git_push_all(self):
        remote = self.remote_input.text().strip()
        if not remote:
            QMessageBox.warning(self, "Missing Remote", "Please enter a valid GitHub remote URL.")
            return

        # Check for remote origin
        ok, current_remote = self.run_cmd(["git", "remote", "get-url", "origin"])
        if not ok:
             self.run_cmd(["git", "remote", "add", "origin", remote])
        elif current_remote.strip() != remote:
             self.run_cmd(["git", "remote", "set-url", "origin", remote])

        self.log("\n--- Starting Automatic Backup & Push ---")
        
        # Ensure user config exists (optional but good for new environments)
        self.run_cmd(["git", "config", "user.name", "aldilcv2"])
        self.run_cmd(["git", "config", "user.email", "aldilcv2@gmail.com"])
        
        self.run_cmd(["git", "add", "."])
        
        # Check if there's anything to commit
        ok, status = self.run_cmd(["git", "status", "--porcelain"])
        if ok and not status.strip():
            self.log("Nothing to commit, working tree clean.")
        else:
            self.run_cmd(["git", "commit", "-m", "Auto-update via Admin Panel"])

        ok, out = self.run_cmd(["git", "push", "-u", "origin", "main"])
        
        if ok:
            QMessageBox.information(self, "Success", "✅ Code successfully pushed to GitHub!")
        else:
            hint = ""
            if "terminal prompts disabled" in out.lower() or "authentication failed" in out.lower():
                hint = "\n\n💡 Hint: GitHub requires a Personal Access Token (PAT) for HTTPS.\n" \
                       "Or run 'git config --global credential.helper store' in terminal to save login."
            
            QMessageBox.critical(self, "Error", f"❌ Failed to push. Check the log for details.{hint}")

# --- Main Application ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BiteBabe Manager Pro")
        self.setGeometry(100, 100, 1000, 700)
        self.data_dir = Path(__file__).parent / "data"
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.landing_tab = LandingPageTab(self.data_dir / "landing_page.json")
        self.tabs.addTab(self.landing_tab, "📝 Landing Page")
        
        self.products_tab = ProductsTab(self.data_dir / "products.json")
        self.tabs.addTab(self.products_tab, "🍪 Products")
        
        self.toppings_tab = ToppingsTab(self.data_dir / "toppings.json")
        self.tabs.addTab(self.toppings_tab, "🍫 Toppings")
        
        self.theme_tab = ThemeTab(self.data_dir / "store.json")
        self.tabs.addTab(self.theme_tab, "🎨 Theme & Store")
        
        self.git_tab = GitTab()
        self.tabs.addTab(self.git_tab, "🚀 Deploy / Git")
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QTabWidget::pane { border: 1px solid #ddd; background: white; border-radius: 4px; }
            QTabBar::tab { padding: 10px 20px; background: #e0e0e0; margin-right: 2px; border-radius: 4px 4px 0 0; }
            QTabBar::tab:selected { background: white; font-weight: bold; border-bottom: 2px solid #FF5C9E; }
            QPushButton { padding: 6px 12px; border-radius: 4px; border: 1px solid #ccc; background: white; }
            QPushButton:hover { background: #f0f0f0; }
            QLineEdit, QTextEdit, QTableWidget { padding: 5px; border: 1px solid #ccc; border-radius: 4px; }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 245, 245))
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    app.setPalette(palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
