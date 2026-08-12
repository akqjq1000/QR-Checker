import sqlite3

class QrDB:
    def __init__(self):
        self.conn = sqlite3.connect('qr.db')

    def _init_db(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS qr_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            img_src TEXT NOT NULL,
            is_malicious INT,
            confidence_score INT,
            extracted_features TEXT,
            ai_analysis TEXT
        );
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("데이터 초기화 오류 발생:", e)

    def _get_all(self):
        pass

    def _get_item(self):
        pass

    def _post_item(self):
        pass

    def _update_item(self):
        pass

    def delete_item(self):
        pass

    def __del__(self):
        self.conn.close()