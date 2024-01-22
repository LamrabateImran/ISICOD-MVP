# Import necessary PyQt5 modules and other dependencies
from PyQt5.QtWidgets import (QLabel, QMessageBox)


def show_popup(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.exec_()


def clear_layout_labels(part_layout):
    for i in reversed(range(part_layout.count())):
        widgetToRemove = part_layout.itemAt(i).widget()
        if widgetToRemove is not None:
            widgetToRemove.setParent(None)


def view_more(checkbox_group):
    # Check the state of the last checkbox
    checked_id = checkbox_group.checkedId()
    if checked_id != -1:
        return checked_id
    else:
        show_popup('Unchecked option', 'Please select one option')


def get_labels_in_layout(part_layout):
    labels = []
    for i in range(part_layout.count()):
        item = part_layout.itemAt(i)
        if item.widget() and isinstance(item.widget(), QLabel):
            labels.append(item.widget())
    return labels


def create_label(self, layout, value, stylesheet):
    label = QLabel(value, self)
    label.setStyleSheet(stylesheet)
    layout.addWidget(label)

