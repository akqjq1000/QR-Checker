import re
from urllib.parse import urlparse, unquote

class URLToFeatureVector:

    def __init__(self, raw_url: str):
        self.url = raw_url.strip()
        self.parsed = urlparse(self.url)

        domain_part = self.parsed.netloc.split(":")[0]
        self.domain_parts = domain_part.split(".")

    def extract_features(self) -> dict:
        len_url = len(self.url)

        # 서브도메인 및 루트 도메인, Suffix(TLD 등) 처리
        # ex) ://naver.com -> parts: ['sub', 'naver', 'com']
        if len(self.domain_parts) >= 3 and not self._is_ip_address():
            sub_domain = ".".join(self.domain_parts[:-2])
            root_domain = self.domain_parts[-2]
            suffix = self.domain_parts[-1]
            count_sub_domain = len(self.domain_parts) - 2
        elif len(self.domain_parts) == 2 and not self._is_ip_address():
            sub_domain = ""
            root_domain = self.domain_parts[0]
            suffix = self.domain_parts[-1]
            count_sub_domain = 0
        else:
            # IP 주소이거나 비정상적인 도메인인 경우
            sub_domain = ""
            root_domain = ".".join(self.domain_parts)
            suffix = ""
            count_sub_domain = 0

        len_sub_domain = len(sub_domain)
        len_root_domain = len(root_domain)
        len_suffix = len(suffix)

        # URL 내 인코딩 데이터 (%XX 등)의 길이
        # 원본 길이와 디코딩된 길이의 차이를 통해 %XX의 총 길이를 계산
        decoded_url = unquote(self.url)
        # % 기호의 개수 * 3 으로 계산할 수도 있으나 원본과 비교가 안전
        len_encoding = len(re.findall(r"%[0-9a-fA-F]{2}", self.url)) * 3

        # URL 내 쿼리 질의문(? 이후)의 길이
        len_query = len(self.parsed.query)
        
        # 파일 경로 깊이 ('/' 개수 - 프로토콜 뒤의 // 제외)
        count_file_path = self.parsed.path.count("/")

        # 특수문자 개수 (알파벳, 숫자, 점, 슬래시를 제외한 피싱 의심 문자)
        count_special_char = len(re.findall(r"[^a-zA-Z0-9./]", self.url))

        # '.' (닷)의 개수
        count_url_dots = self.url.count(".")

        # 도메인이 문자열이 아닌 IP 주소 형태인지 여부
        is_ip = self._is_ip_address()

        # private TLD 여부 (.local, .internal 등 공식 기관이 안 쓰는 로컬 도메인)
        private_tlds = ["local", "internal", "lan", "home", "test"]
        is_private = suffix.lower() in private_tlds

        # 낚시성 필터 단어 포함 여부
        filter_words = [
            "login",
            "verify",
            "bank",
            "secure",
            "update",
            "signin",
            "account",
        ]
        is_filter = any(word in self.url.lower() for word in filter_words)

        # 사용된 포트 번호 (없으면 -1)
        num_port = self.parsed.port if self.parsed.port is not None else -1

        return {
            "len_url": len_url,
            "len_sub_domain": len_sub_domain,
            "len_root_domain": len_root_domain,
            "len_suffix": len_suffix,
            "len_encoding": len_encoding,
            "len_query": len_query,
            "count_sub_domain": count_sub_domain,
            "count_file_path": count_file_path,
            "count_special_char": count_special_char,
            "count_url_dots": count_url_dots,
            "is_ip": is_ip,
            "is_private": is_private,
            "is_filter": is_filter,
            "num_port": num_port,
        }

    def _is_ip_address(self) -> bool:
        domain = self.parsed.netloc.split(":")[0]
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        return bool(re.match(ip_pattern, domain))

if __name__ == "__main__":
    # 테스트
    test_url = "http://secure-bank.internal"

    extractor = URLToFeatureVector(test_url)
    features = extractor.extract_features()

    import pprint

    pprint.pprint(features)

