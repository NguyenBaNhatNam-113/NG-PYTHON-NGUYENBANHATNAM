import sys
import json
import os
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget

DB_FILE = "user.json"  # File lưu dữ liệu user
CART_FILE = "cart.json"  # File lưu dữ liệu giỏ hàng

class SignInWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("signin.ui", self)
        self.signinputton.clicked.connect(self.login)
        self.donthaveacc.mousePressEvent = self.go_to_signup

    def load_users(self):
        if not os.path.exists(DB_FILE):
            return []
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def login(self):
        email = self.email.text().strip()
        password = self.passw.text().strip()

        if not email or not password:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Cảnh báo")
            msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
            msg_box.setText('<span style="color: lightblue; font-size: 12px;">Vui lòng nhập đầy đủ email và mật khẩu.</span>')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
            msg_box.exec()
            return

        users = self.load_users()
        for user in users:
            if user["email"] == email and user["password"] == password:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Thành công")
                msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
                msg_box.setText(f'<span style="color: lightblue; font-size: 12px;">Chào mừng bạn quay trở lại, {email}!</span>')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
                msg_box.exec()
                self.go_to_main()
                return

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Lỗi")
        msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
        msg_box.setText('<span style="color: lightblue; font-size: 12px;">Email hoặc mật khẩu không đúng.</span>')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
        msg_box.exec()

    def go_to_signup(self, event):
        self.close()
        self.signup_window = SignUpWindow()
        self.signup_window.show()

    def go_to_main(self):
        self.mainwindow = MainWindow()
        self.mainwindow.show()
        self.close()

class SignUpWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("signup.ui", self)
        self.signupbutton.clicked.connect(self.signup)
        self.haveacc.mousePressEvent = self.go_to_signin

    def load_users(self):
        if not os.path.exists(DB_FILE):
            return []
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_users(self, users):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

    def signup(self):
        email = self.uemail.text().strip()
        password = self.upassw.text().strip()
        confirm = self.conpassw.text().strip()
        agree = self.agree.isChecked()

        if not email or not password or not confirm:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Cảnh báo")
            msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
            msg_box.setText('<span style="color: lightblue; font-size: 12px;">Vui lòng điền đầy đủ thông tin.</span>')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
            msg_box.exec()
            return

        if password != confirm:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Cảnh báo")
            msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
            msg_box.setText('<span style="color: lightblue; font-size: 12px;">Mật khẩu và xác nhận mật khẩu không khớp.</span>')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
            msg_box.exec()
            return

        if not agree: 
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Cảnh báo")
            msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
            msg_box.setText('<span style="color: lightblue; font-size: 12px;">Bạn phải đồng ý với chính sách bảo mật.</span>')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
            msg_box.exec()
            return

        users = self.load_users()
        for user in users:
            if user["email"] == email:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Cảnh báo")
                msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
                msg_box.setText('<span style="color: lightblue; font-size: 12px;">Email đã được đăng ký.</span>')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
                msg_box.exec()
                return

        users.append({"email": email, "password": password})
        self.save_users(users)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Thành công")
        msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
        msg_box.setText('<span style="color: lightblue; font-size: 12px;">Đăng ký thành công! Vui lòng đăng nhập.</span>')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
        msg_box.exec()
        self.go_to_signin(None)

    def go_to_signin(self, event):
        self.close()
        self.signin_window = SignInWindow()
        self.signin_window.show()

class ProductDetail(QtWidgets.QWidget):
    add_to_cart = QtCore.pyqtSignal(dict)

    def __init__(self, product_data):
        super().__init__()
        self.product_data = product_data
        uic.loadUi("product.ui", self)

        self.ten.setText(product_data.get("ten", "Không xác định"))
        self.mota.setText(product_data.get("mota", "Không có mô tả"))
        self.gia.setText(f"{product_data.get('gia', 0):,} VNĐ")
        
        image_path = product_data.get("hinhanh", "")
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(180, 180, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            self.hinhanh.setPixmap(pixmap)
            self.hinhanh.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            self.hinhanh.setText("Không có hình ảnh")

        self.add.clicked.connect(self.emit_add_to_cart_signal)

    def emit_add_to_cart_signal(self):
        print("Phát tín hiệu add_to_cart:", self.product_data)
        self.add_to_cart.emit(self.product_data)

class Product_W(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(dict)

    def __init__(self, product_data):
        super().__init__()
        self.product_data = product_data
        uic.loadUi("product_main.ui", self)

        self.ten.setText(product_data.get("ten", "Không xác định"))
        self.gia.setText(f"{product_data.get('gia', 0):,} VNĐ")

        image_path = product_data.get("hinhanh", "")
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            self.hinhanh.setPixmap(pixmap)
            self.hinhanh.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            self.hinhanh.setText("Không có hình ảnh")

    def mousePressEvent(self, event):
        print("Phát tín hiệu clicked:", self.product_data)
        self.clicked.emit(self.product_data)

class CartItem(QtWidgets.QWidget):
    state_changed = QtCore.pyqtSignal()

    def __init__(self, item_data):
        super().__init__()
        self.item_data = item_data
        uic.loadUi("cart_item.ui", self)

        self.ten.setText(item_data["product"].get("ten", "Không xác định"))
        self.gia.setText(f"{item_data['product'].get('gia', 0):,} VNĐ")
        self.soluong.setText(str(item_data.get("quantity", 1)))

        image_path = item_data["product"].get("hinhanh", "")
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            self.anh.setPixmap(pixmap)
            self.anh.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            self.anh.setText("Không có hình ảnh")

        self.anh.setFixedSize(50, 50)
        self.ten.setMinimumWidth(200)
        self.gia.setMinimumWidth(100)
        self.soluong.setMinimumWidth(50)
        self.ten.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.gia.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.soluong.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.checkBox.setChecked(True)
        self.checkBox.stateChanged.connect(self.state_changed.emit)

    def is_selected(self):
        return self.checkBox.isChecked()

class CartWindow(QtWidgets.QWidget):
    cart_updated = QtCore.pyqtSignal(list)

    def __init__(self, initial_items=None):
        super().__init__()
        uic.loadUi("cart.ui", self)
        self.cart_items = initial_items if initial_items is not None else self.load_cart()

        if self.scrollAreaWidgetContents.layout() is None:
            layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
            layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            layout.setSpacing(10)
            layout.setContentsMargins(10, 10, 10, 10)
            self.scrollAreaWidgetContents.setLayout(layout)

        self.cart_item_widgets = []
        self.update_cart_display()
        self.pay_btn.clicked.connect(self.process_payment)

    def add_to_cart(self, product, quantity=1):
        for item in self.cart_items:
            if item["product"]["id"] == product["id"]:
                item["quantity"] += quantity
                self.update_cart_display()
                self.save_cart()
                self.cart_updated.emit(self.cart_items)
                return
        self.cart_items.append({"product": product, "quantity": quantity})
        self.update_cart_display()
        self.save_cart()
        self.cart_updated.emit(self.cart_items)

    def update_cart_display(self):
        layout = self.scrollAreaWidgetContents.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.cart_item_widgets.clear()

        if not self.cart_items:
            empty_label = QtWidgets.QLabel("Giỏ hàng trống")
            empty_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty_label)
            self.total.setText("Tổng: 0 VNĐ")
        else:
            for item in self.cart_items:
                cart_item_widget = CartItem(item)
                cart_item_widget.state_changed.connect(self.update_total)
                self.cart_item_widgets.append(cart_item_widget)
                layout.addWidget(cart_item_widget)
            self.update_total()

    def update_total(self):
        total = 0
        for widget in self.cart_item_widgets:
            if widget.is_selected():
                item = widget.item_data
                total += item["product"]["gia"] * item["quantity"]
        self.total.setText(f"Tổng: {total:,} VNĐ")

    def process_payment(self):
        selected_items = []
        for widget in self.cart_item_widgets:
            if widget.is_selected():
                selected_items.append(widget.item_data)

        if not selected_items:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Cảnh báo")
            msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
            msg_box.setText('<span style="color: lightblue; font-size: 12px;">Vui lòng chọn ít nhất một sản phẩm để thanh toán.</span>')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
            msg_box.exec()
            return

        total = sum(item["product"]["gia"] * item["quantity"] for item in selected_items)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Thanh toán")
        msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
        msg_box.setText(f'<span style="color: lightblue; font-size: 12px;">Thanh toán thành công! Tổng: {total:,} VNĐ</span>')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setStyleSheet("QLabel { color: lightblue; font-size: 12px; } QPushButton { font-size: 12px; }")
        msg_box.exec()

        self.cart_items = [item for item in self.cart_items if item not in selected_items]
        self.update_cart_display()
        self.save_cart()
        self.cart_updated.emit(self.cart_items)

    def save_cart(self):
        with open(CART_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cart_items, f, indent=2, ensure_ascii=False)

    def load_cart(self):
        if not os.path.exists(CART_FILE):
            return []
        try:
            with open(CART_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi khi đọc cart.json: {e}")
            return []

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main2.ui", self)
        self.detail_window = None
        self.cart_window = None
        self.cart_items = self.load_cart()
        self.load_products()
        
        self.beyblade.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.page_3)
        self.krgavv.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.page)
        self.galaxyos.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.page_11)
        self.zikudr.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.page_2)
        
        self.cart.mousePressEvent = self.show_cart

    def load_products(self):
        category_mapping = {
            "Beyblade": self.scrollAreaWidgetContents_3,
            "Kamen Rider Gavv": self.scrollAreaWidgetContents_2,
            "Galaxy Orbit Set": self.scrollAreaWidgetContents,
            "Ziku Driver": self.scrollAreaWidgetContents_4
        }

        for scroll_content in category_mapping.values():
            for widget in scroll_content.findChildren(QtWidgets.QWidget):
                widget.deleteLater()

        for scroll_content in category_mapping.values():
            layout = QtWidgets.QHBoxLayout(scroll_content)
            layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
            layout.setSpacing(10)
            layout.setContentsMargins(10, 10, 10, 10)
            scroll_content.setLayout(layout)

        try:
            with open("products.json", "r", encoding="utf-8") as f:
                products = json.load(f)
        except Exception as e:
            print(f"Lỗi khi đọc products.json: {e}")
            return

        for scroll_content in category_mapping.values():
            for product in products:
                category = product.get("category", "")
                if category in category_mapping and category_mapping[category] == scroll_content:
                    widget = Product_W(product)
                    widget.clicked.connect(self.show_product_detail)
                    scroll_content.layout().addWidget(widget)
            scroll_content.layout().addStretch()

        for scroll_content in category_mapping.values():
            scroll_area = scroll_content.parentWidget().parentWidget()
            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def show_product_detail(self, product_data):
        if self.detail_window:
            self.detail_window.close()
        self.detail_window = ProductDetail(product_data)
        self.detail_window.add_to_cart.connect(self.add_to_cart)
        self.detail_window.show()

    def add_to_cart(self, product_data):
        for item in self.cart_items:
            if item["product"]["id"] == product_data["id"]:
                item["quantity"] += 1
                print(f"Cập nhật số lượng: {product_data['ten']} x {item['quantity']}")
                self.save_cart()
                return
        self.cart_items.append({"product": product_data, "quantity": 1})
        print(f"Đã thêm vào giỏ: {product_data['ten']} x 1")
        self.save_cart()

    def show_cart(self, event):
        if self.cart_window:
            self.cart_window.close()
        self.cart_window = CartWindow(initial_items=self.cart_items)
        self.cart_window.cart_updated.connect(self.update_cart_items)
        self.cart_window.show()

    def update_cart_items(self, updated_items):
        self.cart_items = updated_items
        self.save_cart()

    def save_cart(self):
        with open(CART_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cart_items, f, indent=2, ensure_ascii=False)

    def load_cart(self):
        if not os.path.exists(CART_FILE):
            return []
        try:
            with open(CART_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi khi đọc cart.json: {e}")
            return []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignInWindow()
    window.show()
    sys.exit(app.exec())