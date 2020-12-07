import sqlite3


class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_tables()
        self.insert_default()

    def create_connection(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        """
        Creates tables if they do not exist
        """
        self.create_connection()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Presets(
            _id INTEGER NOT NULL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            main_window INTEGER NOT NULL,
            text_editor INTEGER NOT NULL,
            syntax_highlight INTEGER NOT NULL,
            is_current INTEGER UNIQUE
        )
        
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS MainWindow(
            _id INTEGER NOT NULL PRIMARY KEY,
            background_color TEXT,
            font TEXT,
            font_color TEXT,
            font_size TEXT,
            menu_selected_item_bgd_color TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS TextEditor(
            _id INTEGER NOT NULL PRIMARY KEY,
            background_color TEXT,
            font TEXT,
            font_color TEXT,
            font_size TEXT,
            line_highlighter_color TEXT
        )
        """)

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS SyntaxHighlight(
            _id INTEGER NOT NULL PRIMARY KEY,
            keywords TEXT,
            operators TEXT,
            braces TEXT,
            defclass TEXT,
            string TEXT,
            multiline_string TEXT,
            comments TEXT,
            self TEXT,
            numbers TEXT
        )
        ''')
        self.close_connection()

    def insert_default(self):
        """
        Inserts default values in tables
        """
        self.create_connection()
        self.cursor.execute('SELECT name FROM Presets WHERE name = (?)', ('Default', ))
        if not self.cursor.fetchall():
            self.cursor.execute('''
            INSERT INTO Presets(name, main_window, text_editor, syntax_highlight, is_current) VALUES ('Default', 1, 1, 1, 1)
            ''')

            self.cursor.execute('''
            INSERT INTO MainWindow(background_color, font, font_color, font_size, menu_selected_item_bgd_color) VALUES (?, ?, ?, ?, ?)
            ''', ('#505050', "Segoe UI", '#d5e6d3', '15px', '#434343'))

            self.cursor.execute('''
            INSERT INTO TextEditor(background_color, font, font_color, font_size, line_highlighter_color) VALUES (?, ?, ?, ?, ?)
            ''', ('#202020', "Segoe UI Semibold", '#d5e6d3', '20px', '#505050'))

            self.cursor.execute('''
            INSERT INTO SyntaxHighlight(keywords, operators, braces, defclass, string, multiline_string, comments, self, numbers) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('#ffa500', '#a9a9a9', '#a9a9a9', '#87ceeb', '#90ee90', '#008000', '#006400', '#ff00ff', '#87ceeb'))

            self.connection.commit()
            self.close_connection()

    def get_current_preset_name(self):
        """
        Returns current presets name
        :return: str
        """
        self.create_connection()
        self.cursor.execute('''SELECT name FROM Presets WHERE is_current IS NOT NULL ''')
        preset = self.cursor.fetchone()[0]
        self.close_connection()
        return preset

    def get_current_preset(self):
        """
        Returns current presets values
        :return: tuple(tuple, tuple, tuple)
        """
        self.create_connection()
        self.cursor.execute('''SELECT * FROM Presets WHERE is_current IS NOT NULL ''')
        preset = self.cursor.fetchall()[0]
        self.cursor.execute('''SELECT * FROM MainWindow WHERE _id = ?''', (preset[2], ))
        mw = self.cursor.fetchone()
        self.cursor.execute('''SELECT * FROM TextEditor WHERE _id = ?''', (preset[3], ))
        te = self.cursor.fetchone()
        self.cursor.execute('''SELECT * FROM SyntaxHighlight WHERE _id = ?''', (preset[4], ))
        sh = self.cursor.fetchone()
        self.close_connection()
        return mw, te, sh

    def get_all_presets(self):
        """
        Returns names of all presets
        :return: list
        """
        self.create_connection()
        self.cursor.execute('''SELECT name FROM Presets''')
        presets = [i[0] for i in self.cursor.fetchall()]
        self.close_connection()
        return presets

    def set_current_preset(self, name):
        """
        Sets given preset as current
        :param name: str
        """
        self.create_connection()
        self.cursor.execute('''SELECT name FROM Presets WHERE is_current = 1''')
        old_preset = self.cursor.fetchone()
        if old_preset:
            self.cursor.execute('''UPDATE Presets SET is_current = NULL WHERE name = ?''', old_preset)
        self.cursor.execute('''UPDATE Presets SET is_current = 1 WHERE name = ?''', (name, ))
        self.connection.commit()
        self.close_connection()

    def delete_preset(self, name):
        self.create_connection()
        self.cursor.execute('''SELECT main_window, text_editor, syntax_highlight FROM Presets WHERE name = ?''', (name, ))
        mw, te, sh = self.cursor.fetchall()[0]
        self.cursor.execute('''DELETE FROM Presets WHERE name = ?''', (name, ))
        self.cursor.execute('''DELETE FROM MainWindow WHERE _id = ?''', (mw, ))
        self.cursor.execute('''DELETE FROM TextEditor WHERE _id = ?''', (te, ))
        self.cursor.execute('''DELETE FROM SyntaxHighlight WHERE _id = ?''', (sh, ))
        self.connection.commit()
        self.close_connection()

    def insert_into_main_window(self, data):
        """
        Inserts data in MainWindow table and returns index of data
        :param data: dict
        :return: int
        """
        self.cursor.execute('''
                    INSERT INTO MainWindow(background_color, font, font_color, font_size, menu_selected_item_bgd_color) VALUES (?, ?, ?, ?, ?)
                    ''', (data['bgcolor'], data['font'], data['font color'], data['font size'], data['selected item color']))
        self.cursor.execute('''
            SELECT MAX(_id) FROM MainWindow
        ''')
        index = self.cursor.fetchone()[0]
        self.connection.commit()
        return index

    def insert_into_text_editor(self, data):
        """
            Inserts data in TextEditor table and returns index of data
            :param data: dict
            :return: int
        """
        self.cursor.execute('''
                    INSERT INTO TextEditor(background_color, font, font_color, font_size, line_highlighter_color) VALUES (?, ?, ?, ?, ?)
                    ''', (data['bgcolor'], data['font'], data['font color'], data['font size'], data['line_highlighter_color']))
        self.cursor.execute('''
                    SELECT MAX(_id) FROM TextEditor
                ''')
        index = self.cursor.fetchone()[0]
        self.connection.commit()
        return index

    def insert_into_syntax_highlight(self, data):
        """
            Inserts data in SyntaxHighlight table and returns index of data
            :param data: dict
            :return: int
        """
        self.cursor.execute('''
                    INSERT INTO SyntaxHighlight(keywords, operators, braces, defclass, string, multiline_string, comments, self, numbers) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (data['keywords'], data['operators'], data['braces'], data['defclass'], data['string'], data['multiline_string'], data['comments'], data['self_color'], data['numbers']))
        self.cursor.execute('''
                    SELECT MAX(_id) FROM SyntaxHighlight
                ''')
        index = self.cursor.fetchone()[0]
        self.connection.commit()
        return index

    def create_new_preset(self, name, main_window_data, text_edit_data, syntax_highlight_data):
        """
        Creates new preset
        :param name: str
        :param main_window_data: dict
        :param text_edit_data: dict
        :param syntax_highlight_data: dict
        """
        self.create_connection()
        mw = self.insert_into_main_window(main_window_data)
        te = self.insert_into_text_editor(text_edit_data)
        sh = self.insert_into_syntax_highlight(syntax_highlight_data)
        self.cursor.execute('''
                    INSERT INTO Presets(name, main_window, text_editor, syntax_highlight) VALUES (?, ?, ?, ?)
                    ''', (name, mw, te, sh))
        self.connection.commit()
        self.close_connection()

    def update_main_window(self, name, data):
        """
        Updates presets MainWindow data and returns index of data
        :param name: str
        :param data: dict
        :return: int
        """
        self.cursor.execute('''
                    UPDATE MainWindow
                    SET (background_color, font, font_color, font_size, menu_selected_item_bgd_color) = (?, ?, ?, ?, ?)
                    WHERE _id = (SELECT main_window FROM Presets WHERE name = ?)
                    ''', (data['bgcolor'], data['font'], data['font color'], data['font size'], data['selected item color'], name))
        self.cursor.execute('''
            SELECT MAX(_id) FROM MainWindow
        ''')
        index = self.cursor.fetchone()[0]
        self.connection.commit()
        return index

    def update_text_editor(self, name, data):
        """
        Updates presets TextEditor data and returns index of data
        :param name: str
        :param data: dict
        :return: int
        """
        self.cursor.execute('''
                    UPDATE TextEditor
                    SET (background_color, font, font_color, font_size, line_highlighter_color) = (?, ?, ?, ?, ?)
                    WHERE _id = (SELECT text_editor FROM Presets WHERE name = ?)
                    ''', (data['bgcolor'], data['font'], data['font color'], data['font size'], data['line_highlighter_color'], name))
        self.cursor.execute('''
                    SELECT MAX(_id) FROM TextEditor
                ''')
        index = self.cursor.fetchone()[0]
        self.connection.commit()
        return index

    def update_syntax_highlight(self, name, data):
        """
        Updates presets SyntaxHighlight data and returns index of data
        :param name: str
        :param data: dict
        :return: int
        """
        self.cursor.execute('''
                    UPDATE SyntaxHighlight
                    SET (keywords, operators, braces, defclass, string, multiline_string, comments, self, numbers) = (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    WHERE _id = (SELECT syntax_highlight FROM Presets WHERE name = ?)
                    ''', (data['keywords'], data['operators'], data['braces'], data['defclass'], data['string'], data['multiline_string'], data['comments'], data['self_color'], data['numbers'], name))
        self.cursor.execute('''
                    SELECT MAX(_id) FROM SyntaxHighlight
                ''')
        index = self.cursor.fetchone()[0]
        self.connection.commit()
        return index

    def update_preset(self, name, main_window_data, text_edit_data, syntax_highlight_data):
        """
        Updates preset
        :param name: str
        :param main_window_data: dict
        :param text_edit_data: dict
        :param syntax_highlight_data: dict
        """
        self.create_connection()
        self.update_main_window(name, main_window_data)
        self.update_text_editor(name, text_edit_data)
        self.update_syntax_highlight(name, syntax_highlight_data)
        self.close_connection()

