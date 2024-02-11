import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
from parser_pdf import text_from_pdf, get_transactions


class TransactionCategorization(QMainWindow):
    def __init__(self, transactions):
        super().__init__()

        self.current_transaction_index = 0
        self.transactions = transactions
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Transaction Categorization')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.date_label = QLabel(self)
        self.transaction_type_label = QLabel(self)
        self.amount_label = QLabel(self)
        self.name_label = QLabel(self)
        self.transaction_count_label = QLabel(self)

        self.category_label = QLabel('Select Category:', self)
        self.category_combobox = QComboBox(self)
        self.categories = ["Aluguel", "Internet", "Celular", "Casa", "Streamings", "\n"
                        "Mercado", "Saúde", "Alimentação", "Fun Time", "Transporte",
                        "Compras Carla", "Compras Rodrigo", "McGill", "Taxes",
                        "Outros", "Viagens", "\n",
                        "Ganho - Rodrigo (Stipend)", "Ganho - Rodrigo (TA)", "Ganho - Carla (Midnight)",
                        "Ganho - Carla (Nubank)", "Ganho - Carla (Itaú)", "Ganho - Rodrigo (Nubank/Invest.)",
                        "Ganho - Outros", "\n", "Cartão de Crédito", "Interac"]
        
        self.category_combobox.addItems(self.categories)
        self.category_combobox.currentIndexChanged.connect(self.save_category)

        self.prev_button = QPushButton('<--', self)
        self.next_button = QPushButton('-->', self)
        self.show_summary_button = QPushButton('Show summary', self)
        self.export_button = QPushButton('Export data', self)


        self.prev_button.clicked.connect(self.prev_transaction)
        self.next_button.clicked.connect(self.next_transaction)
        self.show_summary_button.clicked.connect(self.show_summary)
        self.export_button.clicked.connect(self.export_data)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        layout = QVBoxLayout()
        layout.addWidget(self.date_label)
        layout.addWidget(self.transaction_type_label)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_combobox)
        layout.addWidget(self.transaction_count_label)
        layout.addLayout(button_layout)  # Add button layout
        layout.addWidget(self.show_summary_button)
        layout.addWidget(self.export_button)

        self.central_widget.setLayout(layout)

        # Display the first transaction
        self.display_transaction(0)

    def prev_transaction(self):
        self.display_transaction(self.current_transaction_index - 1)

    def next_transaction(self):
        self.display_transaction(self.current_transaction_index + 1)

    def display_transaction(self, index):
        if 0 <= index < len(self.transactions):
            self.current_transaction_index = index
            transaction = self.transactions[self.current_transaction_index]
            self.date_label.setText(f"Date: {transaction['Date']}")
            self.transaction_type_label.setText(f"Type: {transaction['Transaction Type']}")
            self.amount_label.setText(f"Amount: ${transaction['Amount']}")
            self.name_label.setText(f"Name: {transaction['Name']}")
            category = transaction.get('Category', '')  # Get the saved category
            index = self.category_combobox.findText(category)
            self.category_combobox.setCurrentIndex(index)  # Set the selected category

            self.transaction_count_label.setText(f'Transaction {self.current_transaction_index + 1}/{len(self.transactions)}')

        else:
            self.current_transaction_index = -1
            self.date_label.setText("All transactions processed")
            self.transaction_type_label.setText(f"Type: ")
            self.amount_label.setText(f"Amount: $")
            self.name_label.setText(f"Name: ")

            self.transaction_count_label.setText(f'Done!')

            print(self.transactions)
            
            

    def save_category(self):
        selected_category = self.category_combobox.currentText()
        if 0 <= self.current_transaction_index < len(self.transactions):
            self.transactions[self.current_transaction_index]['Category'] = selected_category

    def export_data(self):
        reply = QMessageBox.question(
            self,
            'Exporting data',
            # 'Do you want to export this months data to the database?',
            'Functionality to be added later. Close application?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            pass
    
    def show_summary(self):
        summary_window = SummaryWindow(self.transactions, self.categories)
        summary_window.exec()


class SummaryWindow(QMessageBox):
    def __init__(self, transactions, categories):
        super().__init__()
        self.setWindowTitle("Summary")
        self.transactions = transactions
        self.categories = categories
        self.calculate_summary()
        self.setText(self.summary_text)


    def calculate_summary(self):
        summary = {category: 0 for category in self.categories}
        for transaction in self.transactions:
            category = transaction.get('Category')
            if category in summary:
                summary[category] += float(transaction['Amount'])
            else:
                summary[category] = float(transaction['Amount'])
        self.summary_text = "\n".join([f"{category}: ${amount}" for category, amount in summary.items()])
        self.summary_print_text = "\n".join([f"{amount}" for _, amount in summary.items()])
        print("Printing summary:\n", self.summary_print_text.replace('.', ','))





def main():

    file_pdf = 'statement_short.pdf'

    lines = text_from_pdf(file_pdf, x_tolerance=2, init_y_top=440, reg_y_top=210)
    transactions = get_transactions(lines)


    app = QApplication(sys.argv)
    window = TransactionCategorization(transactions)
    window.show()
    sys.exit(app.exec())



if __name__ == '__main__':
    main()
