import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, 
    QComboBox, QTableWidget, QTableWidgetItem, QStackedWidget, QFormLayout, QWidget, QMessageBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Aplikasi Hotel')
        self.setGeometry(100, 100, 400, 300)

        # Directory to store data
        self.data_dir = 'hotel_data'
        os.makedirs(self.data_dir, exist_ok=True)

        # File paths
        self.guest_file = os.path.join(self.data_dir, 'guests.json')
        self.booking_file = os.path.join(self.data_dir, 'bookings.json')

        # Load data from files
        self.guest_list = self.load_data(self.guest_file)
        self.room_bookings = self.load_data(self.booking_file)

        # Create StackedWidget to manage different views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Main Menu
        self.main_menu = QWidget()
        self.main_menu_layout = QVBoxLayout()
        self.main_menu.setLayout(self.main_menu_layout)
        
        self.main_menu_layout.addWidget(QLabel('<h1>Aplikasi Hotel</h1>'))

        self.register_button = QPushButton('Daftar Tamu')
        self.register_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.register_button.clicked.connect(self.show_register_guest)
        self.main_menu_layout.addWidget(self.register_button)

        self.booking_button = QPushButton('Pesan Kamar')
        self.booking_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.booking_button.clicked.connect(self.show_room_booking)
        self.main_menu_layout.addWidget(self.booking_button)

        self.status_button = QPushButton('Status Kamar')
        self.status_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.status_button.clicked.connect(self.show_room_status)
        self.main_menu_layout.addWidget(self.status_button)
        
        self.stacked_widget.addWidget(self.main_menu)

        # Guest Registration
        self.guest_registration = QWidget()
        self.guest_registration_layout = QFormLayout()
        self.guest_registration.setLayout(self.guest_registration_layout)
        
        self.guest_registration_layout.addRow(QLabel('<h2>Pendaftaran Tamu</h2>'))
        
        self.name_input = QLineEdit()
        self.guest_registration_layout.addRow('Nama:', self.name_input)
        
        self.id_input = QLineEdit()
        self.guest_registration_layout.addRow('ID:', self.id_input)
        
        self.register_guest_button = QPushButton('Daftar')
        self.register_guest_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.register_guest_button.clicked.connect(self.register_guest)
        self.guest_registration_layout.addRow(self.register_guest_button)
        
        self.back_button1 = QPushButton('Kembali ke Menu Utama')
        self.back_button1.setStyleSheet("font-size: 16px; padding: 10px;")
        self.back_button1.clicked.connect(self.show_main_menu)
        self.guest_registration_layout.addRow(self.back_button1)
        
        self.stacked_widget.addWidget(self.guest_registration)

        # Room Booking
        self.room_booking = QWidget()
        self.room_booking_layout = QFormLayout()
        self.room_booking.setLayout(self.room_booking_layout)
        
        self.room_booking_layout.addRow(QLabel('<h2>Pemesanan Kamar</h2>'))
        
        self.booking_name_input = QLineEdit()
        self.room_booking_layout.addRow('Nama:', self.booking_name_input)
        
        self.room_type_input = QComboBox()
        self.room_type_input.addItems(['Single', 'Double', 'Suite'])
        self.room_booking_layout.addRow('Tipe Kamar:', self.room_type_input)
        
        self.book_room_button = QPushButton('Pesan')
        self.book_room_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.book_room_button.clicked.connect(self.book_room)
        self.room_booking_layout.addRow(self.book_room_button)
        
        self.back_button2 = QPushButton('Kembali ke Menu Utama')
        self.back_button2.setStyleSheet("font-size: 16px; padding: 10px;")
        self.back_button2.clicked.connect(self.show_main_menu)
        self.room_booking_layout.addRow(self.back_button2)
        
        self.stacked_widget.addWidget(self.room_booking)

        # Room Status
        self.room_status = QWidget()
        self.room_status_layout = QVBoxLayout()
        self.room_status.setLayout(self.room_status_layout)
        
        self.room_status_layout.addWidget(QLabel('<h2>Status Kamar</h2>'))
        
        self.status_table = QTableWidget()
        self.status_table.setRowCount(10)  # Assume 10 rooms for simplicity
        self.status_table.setColumnCount(3)  # Added one more column for Check-Out button
        self.status_table.setHorizontalHeaderLabels(['Kamar', 'Status', ''])
        for i in range(10):
            self.status_table.setItem(i, 0, QTableWidgetItem(f'Kamar {i+1}'))
            self.status_table.setItem(i, 1, QTableWidgetItem('Tersedia'))
            check_out_button = QPushButton('Check-Out')
            check_out_button.clicked.connect(lambda _, row=i: self.check_out(row))
            self.status_table.setCellWidget(i, 2, check_out_button)
        self.room_status_layout.addWidget(self.status_table)
        
        self.back_button3 = QPushButton('Kembali ke Menu Utama')
        self.back_button3.setStyleSheet("font-size: 16px; padding: 10px;")
        self.back_button3.clicked.connect(self.show_main_menu)
        self.room_status_layout.addWidget(self.back_button3)
        
        self.stacked_widget.addWidget(self.room_status)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def show_register_guest(self):
        self.stacked_widget.setCurrentWidget(self.guest_registration)

    def show_room_booking(self):
        self.stacked_widget.setCurrentWidget(self.room_booking)

    def show_room_status(self):
        # Update room status table based on bookings
        for i in range(10):
            room_status = 'Tersedia'
            for booking in self.room_bookings:
                if booking['room'] == f'Kamar {i+1}':
                    room_status = 'Terpesan'
                    break
            self.status_table.setItem(i, 1, QTableWidgetItem(room_status))
        
        self.stacked_widget.setCurrentWidget(self.room_status)

    def register_guest(self):
        name = self.name_input.text()
        guest_id = self.id_input.text()

        if name and guest_id:
            self.guest_list.append({'name': name, 'id': guest_id})
            self.save_data(self.guest_file, self.guest_list)
            QMessageBox.information(self, 'Sukses', 'Tamu berhasil didaftarkan')
            self.name_input.clear()
            self.id_input.clear()
        else:
            QMessageBox.warning(self, 'Error', 'Nama dan ID harus diisi')

    def book_room(self):
        name = self.booking_name_input.text()
        room_type = self.room_type_input.currentText()

        if name and room_type:
            # Check if the guest is registered
            if not any(guest['name'] == name for guest in self.guest_list):
                QMessageBox.warning(self, 'Error', 'Nama tidak terdaftar sebagai tamu')
                return
            
            room_number = None
            for i in range(10):
                if self.status_table.item(i, 1).text() == 'Tersedia':
                    room_number = f'Kamar {i+1}'
                    break

            if room_number:
                self.room_bookings.append({'name': name, 'room': room_number, 'type': room_type})
                self.save_data(self.booking_file, self.room_bookings)
                QMessageBox.information(self, 'Sukses', f'Kamar berhasil dipesan: {room_number}')
                self.booking_name_input.clear()
                self.room_type_input.setCurrentIndex(0)
            else:
                QMessageBox.warning(self, 'Error', 'Tidak ada kamar tersedia')
        else:
            QMessageBox.warning(self, 'Error', 'Nama dan tipe kamar harus diisi')

    def check_out(self, room_index):
        room_number = f'Kamar {room_index + 1}'
        # Find the booking and remove it
        for booking in self.room_bookings:
            if booking['room'] == room_number:
                self.room_bookings.remove(booking)
                self.save_data(self.booking_file, self.room_bookings)
                QMessageBox.information(self, 'Sukses', f'Tamu di {room_number} sudah check-out')
                break
        self.show_room_status()  # Refresh the room status table

    def save_data(self, filepath, data):
        with open(filepath, 'w') as file:
            json.dump(data, file)

    def load_data(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return json.load(file)
        return []

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()