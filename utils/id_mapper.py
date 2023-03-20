id_map = {
        'bedurgi999': '박보선',
        'sa46lll': '서명현',
        'woowonkim': '김우원',
        'seungah-hong': '홍승아',
        'tigre911': '김진우',
        'frosts2-study': '김설희',
        'danielchoi1115': '최승열',
        'sskong777': '홍석현',
        'noino0819': '최시언',
        'seungjookim': '김승주',
        'deingvelop': '송민진',
        'black-kit': '양석진',
        'cherryjubilee': '박혜원',
        'devjoowon': "박주원"
    }

def get_name_from_id(user_id:str):
    return id_map.get(user_id.lower())