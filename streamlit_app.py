import tornado.web
import streamlit as st

# ==========================================
# [Monkey Patching] Tornado Server 헤더 삭제
# ==========================================
# 1. 원래 함수 백업
_original_set_default_headers = tornado.web.RequestHandler.set_default_headers

# 2. 덮어쓸 함수 정의
def patched_set_default_headers(self):
    # 원래 기능 수행 (CORS 설정 등)
    _original_set_default_headers(self)
    
    # [핵심] Server 헤더를 'Hidden'으로 변경하거나 아예 삭제
    # (삭제해도 앞단 프록시가 다시 채울 수 있어서, 확인을 위해 값 변경으로 테스트 추천)
    self.set_header("Server", "My-Secure-Server") 
    # self.clear_header("Server") # 아예 지우고 싶을 때

# 3. 함수 교체
tornado.web.RequestHandler.set_default_headers = patched_set_default_headers
# ==========================================

st.title("Server Header Patch Test")
st.write("Tornado의 Server 헤더가 변경되었는지 개발자 도구(F12)로 확인해보세요.")