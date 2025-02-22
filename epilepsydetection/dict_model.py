from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex

class DictionaryModel(QAbstractListModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or {}
        self._checked_items = set()

    def data(self, index, role):
        if not index.isValid():
            return None

        key = list(self._data.keys())[index.row()]

        if role == Qt.DisplayRole:
            return key
        elif role == Qt.CheckStateRole:
            return Qt.Checked if key in self._checked_items else Qt.Unchecked

        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        key = list(self._data.keys())[index.row()]

        if role == Qt.CheckStateRole:
            if value == 2:
                self._checked_items.add(key)
            else:
                self._checked_items.discard(key)
            self.dataChanged.emit(index, index, [role])
            return True

        return False


    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable


    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    

    def get_value(self, key):
        return self._data.get(key)

    def set_value(self, key, value):
        self._data[key] = value
        self._checked_items.add(key)
        self.layoutChanged.emit()

    def get_checked_items(self):
        return {key: self._data[key] for key in self._checked_items}


    def resetInternalData(self):
        self._data = {}
        self.layoutChanged.emit()