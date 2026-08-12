import sqlite3
from schema import *

class QrDB:
    def __init__(self):
        self.conn = sqlite3.connect('./qr.db')
        self._init_db()

    def _init_db(self) -> bool:
        sql = '''
        CREATE TABLE IF NOT EXISTS scan_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            raw_url TEXT NOT NULL,

            len_url INTEGER, len_sub_domain INTEGER, len_root_domain INTEGER,
            len_suffix INTEGER, len_encoding INTEGER, len_query INTEGER,
            count_sub_domain INTEGER, count_file_path INTEGER, count_special_char INTEGER,
            count_url_dots INTEGER, is_ip BOOLEAN, is_private BOOLEAN,
            is_filter BOOLEAN, num_port INTEGER, ratio_alpha_numeric NUMBER, value_entropy_url NUMBER,

            img_path TEXT NOT NULL,
            is_malicious INT,
            confidence_score INT,
            reason TEXT
            -- measures TEXT
        )
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            self.conn.commit()
            print('데이터베이스 초기화 완료')
            return True
        except Exception as e:
            print("데이터 초기화 오류 발생:", e)
        return False

    def _get_all(self):
        pass

    def _get_item(self):
        pass

    def _post_item(self, raw_url: str, img_path: str, fv: FeatureVector, dr: DetectionResult, ar: AnalysisResult):
        sql ='''
        INSERT INTO scan_history(raw_url, img_path, len_url, len_sub_domain, len_root_domain, len_suffix,
                    len_encoding, len_query, count_sub_domain, count_file_path,
                    count_special_char, count_url_dots, is_ip, is_private, is_filter, num_port, 
                    ratio_alpha_numeric, value_entropy_url, is_malicious, confidence_score, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        params = [raw_url, img_path]

        params.extend(fv.to_array())
        params.extend(list(dr.to_dict().values()))
        ar_list = list(ar.to_dict().values())
        params.append(ar_list[0])

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print("데이터베이스 삽입 오류:", e)

    def delete_item(self, id):
        sql = '''
        DELETE FROM scan_history WHERE id=?
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, [id])
            self.conn.commit()
        except Exception as e:
            print("데이터베이스 삭제 오류:", e)

    # 객체 소멸 
    def __del__(self):
        self.conn.close()

# 테스트 코드
if __name__ == "__main__":
    qrdb = QrDB()

    raw_url = "http://g00gle-login.com:8080/verify"

    features = FeatureVector(
        len_url=35, len_sub_domain=6, len_root_domain=15, len_suffix=3,
        len_encoding=0, len_query=6,
        count_sub_domain=1, count_file_path=1, count_special_char=5, count_url_dots=3,
        is_ip=False, is_private=False, is_filter=True, num_port=8080,
        ratio_alpha_numeric=0.82, value_entropy_url=3.94,
    )
    detection = DetectionResult(is_malicious=True, confidence_score=0.92)
    analysis = AnalysisResult(
        reason="구글 공식 도메인 오탈자를 이용한 스푸핑 도메인 및 비표준 포트 사용",
        countermeasures=[
            "해당 링크에 접속하지 마세요.",
            "이미 접속하여 정보를 입력했다면 즉시 관련 계정 패스워드를 변경하세요.",
        ],
    )

    qrdb._post_item(raw_url, '/image/qr-1.jpg', features, detection, analysis)