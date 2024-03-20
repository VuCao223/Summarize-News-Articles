import sys
from PyQt6 import QtWidgets
from gensim.models import KeyedVectors

from duanmoi1 import sent_tokenize, sentencesVector, soluongcau, sumarization
from news import Ui_MainWindow

class TextSummarizationApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text Summarization App')

        self.clean.clicked.connect(self.clean_contents)
        self.sum.clicked.connect(self.summarize_text)
        self.input.clicked.connect(self.load_text_file)

    def clean_contents(self):
        self.contents.clear()
        self.text_sum.clear()

    def load_text_file(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.txt)")
        if file_dialog.exec():
            try:
                file_path = file_dialog.selectedFiles()[0]
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.contents.setPlainText(content)
            except Exception as e:
                # Xử lý lỗi ở đây, ví dụ: hiển thị thông báo lỗi
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def summarize_text(self):
        content = self.contents.toPlainText()
        stopwords_content = get_stopwords(stopword_path)
        sentences = sent_tokenize(content)
        w2v = KeyedVectors.load_word2vec_format(w2v_path, binary=False)
        X = sentencesVector(sentences, stopwords_content, w2v)
        kmeans = soluongcau(X)
        summary = sumarization(kmeans, X, sentences)
        self.text_sum.setPlainText(summary)

def get_stopwords(stopword_path):
    with open(stopword_path, 'r', encoding='utf-8') as f:
        return f.read().split('\n')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w2v_path = "vi_txt/vi.vec"
    stopword_path = "E:/PycharmProjects/pythonProject/duanmoi/document/stopwords.csv"
    window = TextSummarizationApp()
    window.show()
    sys.exit(app.exec())
