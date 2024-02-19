from fastapi import HTTPException, status


class ChatRoomException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(ChatRoomException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class PasswordMismatchException(ChatRoomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пароли не совпадают"


class ChatIsNotExistsException(ChatRoomException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Чата с таким id не существует"


class ChatAccessDeniedException(ChatRoomException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Доступ к чату запрещен"


class ChatDeletionPermissionsException(ChatRoomException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "У вас нет прав на удаление данного чата"


class ChatPasswordMismatchException(ChatRoomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неправильный пароль"


HTTPException(status_code=403, detail="У вас нет права на удаление данного чата")
