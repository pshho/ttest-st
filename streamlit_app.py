import streamlit as st
import tornado.web
import gc

# ==========================================
# [Advanced Patching] 실행 중인 모든 핸들러 강제 패치
# ==========================================

# 1. 덮어쓸 함수(Patch Function)를 먼저 정의합니다.
def secure_headers_patch(self):
    # 기존에 백업해둔 원본 함수가 있다면 실행 (CORS 등 기능 유지)
    if hasattr(self, '_original_set_default_headers'):
        self._original_set_default_headers()
    
    # [핵심] Server 헤더 삭제 또는 변경
    # self.clear_header("Server") # 아예 지우기
    self.set_header("Server", "My-Secure-Server") # 테스트용: 값 변경 확인

def apply_tornado_patch():
    # 2. 메모리에서 현재 실행 중인 Tornado Application 객체를 찾습니다.
    tornado_apps = [
        obj for obj in gc.get_objects() 
        if isinstance(obj, tornado.web.Application)
    ]
    
    if not tornado_apps:
        return

    # 3. 찾은 앱의 모든 라우팅 규칙(Rules)을 순회합니다.
    app = tornado_apps[0]
    
    # 4. Router에 등록된 모든 핸들러 클래스(Target)를 수집합니다.
    target_handlers = []
    
    if hasattr(app, 'wildcard_router'):
        for rule in app.wildcard_router.rules:
            target_handlers.append(rule.target)
    
    if hasattr(app, 'default_router'):
        for rule in app.default_router.rules:
            target_handlers.append(rule.target)

    # 5. 수집된 각 핸들러 클래스에 대해 Monkey Patch를 적용합니다.
    for handler_class in set(target_handlers): # 중복 제거
        # 이미 패치된 경우 스킵 (중복 실행 방지)
        if getattr(handler_class, '_is_patched_by_us', False):
            continue
            
        # 기존 메서드 백업 (있을 경우에만)
        if hasattr(handler_class, 'set_default_headers'):
            handler_class._original_set_default_headers = handler_class.set_default_headers
        
        # 메서드 교체 (위에서 정의한 secure_headers_patch 함수로)
        handler_class.set_default_headers = secure_headers_patch
        handler_class._is_patched_by_us = True

# 6. 패치 실행 (함수 정의가 다 끝난 뒤에 실행해야 함)
apply_tornado_patch()
# ==========================================

st.title("Advanced Header Patch Test")
st.write("개발자 도구(F12) -> Network 탭에서 'Server' 헤더가 'My-Secure-Server'로 바뀌었는지 확인하세요.")
st.write("이제 /_stcore/stream 경로도 포함하여 적용됩니다.")