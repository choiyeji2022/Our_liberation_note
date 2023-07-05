from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsGroupMemberOrMaster(BasePermission):
    SAFE_METHODS = ('GET', )
    message = "접근 권한이 없습니다."
    
    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 읽기 전용 권한은 그룹에 속한 멤버만 허용
        if request.method in self.SAFE_METHODS:
            return request.user.is_authenticated and request.user in obj.members.all()

        # 요청 메서드가 쓰기 전용인 경우 마스터만 권한 허용
        return request.user.is_authenticated and obj.master == request.user
