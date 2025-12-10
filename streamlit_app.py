import tornado.web
import streamlit as st
import tornado.web
import gc

def apply_tornado_patch():
    # 1. 메모리에서 현재 실행 중인 Tornado Application 객체를 찾습니다.
    # (Streamlit은 내부적으로 Tornado 객체를 숨겨두므로 gc로 찾습니다)
    tornado_apps = [
        obj for obj in gc.get_objects() 
        if isinstance(obj, tornado.web.Application)
    ]
    
    if not tornado_apps:
        return

    # 2. 찾은 앱의 모든 라우팅 규칙(Rules)을 순회합니다.
    app = tornado_apps[0]
    
    # 3. Router에 등록된 모든 핸들러 클래스(Target)를 가져옵니다.
    # (일반 URL, 웹소켓, _stcore 내부 경로 포함)
    target_handlers = []
    
    if hasattr(app, 'wildcard_router'):
        for rule in app.wildcard_router.rules:
            target_handlers.append(rule.target)
    
    if hasattr(app, 'default_router'):
        for rule in app.default_router.rules:
            target_handlers.append(rule.target)

    # 4. 각 핸들러 클래스에 대해 Monkey Patch를 적용합니다.
    for handler_class in set(target_handlers): # 중복 제거
        # 이미 패치된 경우 스킵
        if getattr(handler_class, '_is_patched_by_us', False):
            continue
            
        # 기존 메서드 백업
        if hasattr(handler_class, 'set_default_headers'):
            handler_class._original_set_default_headers = handler_class.set_default_headers
        
        # 메서드 교체
        handler_class.set_default_headers = secure_headers_patch
        handler_class._is_patched_by_us = True

# 패치 실행
apply_tornado_patch()
# ==========================================

st.title("Advanced Header Patch Test")
st.write("이제 /_stcore/stream 등 내부 경로를 포함한 모든 응답에서 Server 헤더가 사라집니다.")
=======
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
>>>>>>> 7c90ba8774f162f2216c045d4e82f4bd246bbf0a