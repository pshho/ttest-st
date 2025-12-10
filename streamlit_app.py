import streamlit as st
import tornado.web
import gc

def patch_server_header():
    # 1. 실행 중인 Tornado App 찾기 (한 줄 처리)
    app = next((obj for obj in gc.get_objects() if isinstance(obj, tornado.web.Application)), None)
    if not app: return

    # 2. 덮어쓸 함수 정의
    def new_headers(self):
        if hasattr(self, '_orig'): self._orig()
        # self.clear_header("Server") # 삭제 시 주석 해제
        self.set_header("Server", "My-Secure-Server") 

    # 3. 모든 라우터의 핸들러 수집 (와일드카드 & 기본 라우터 통합)
    routers = [getattr(app, r) for r in ['wildcard_router', 'default_router'] if hasattr(app, r)]
    handlers = {rule.target for r in routers for rule in r.rules}

    # 4. 패치 적용 (중복 방지 포함)
    for h in handlers:
        if not getattr(h, '_patched', False):
            h._orig, h.set_default_headers, h._patched = h.set_default_headers, new_headers, True

# 실행
patch_server_header()

# --- 테스트 UI ---
st.title("Header Patch Applied")
st.write("F12 > Network 탭에서 Server 헤더가 변경되었는지 확인하세요.")