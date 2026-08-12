from modules.schema import FeatureVector

def extract(url: str) -> FeatureVector:
    """URL에서 피처를 추출하는 MOCK 함수"""
    return FeatureVector(
        len_url=len(url),
        len_sub_domain=12,
        len_root_domain=17,
        len_suffix=3,
        len_encoding=0,
        len_query=0,
        count_sub_domain=1,
        count_file_path=1,
        count_special_char=2,
        count_url_dots=url.count("."),
        is_ip=False,
        is_private=False,
        is_filter=True,
        num_port=-1,
        ratio_alpha_numeric=0.94,
        value_entropy_url=3.72
    )