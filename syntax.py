from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class TemplateHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#00ffff"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        self.highlighting_rules = []

        # Python / C style keywords
        keywords = [
            "def", "class", "import", "return", "if", "else", "while", "for", "in",
            "try", "except", "void", "int", "char", "include", "printf", "main"
        ]
        for word in keywords:
            pattern = QRegularExpression(rf"\b{word}\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#ffa500"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"]*"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^']*'"), string_format))

        # Comments (Python + C style)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#888888"))
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"//.*"), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"/\*.*\*/"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iter = pattern.globalMatch(text)
            while match_iter.hasNext():
                match = match_iter.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
