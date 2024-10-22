from typing import Union
from Requets import PostRequest, Login
from Reporter import Reporter
from UserRedis import UserInfoRedis


class Launcher:

    def __init__(self, accounts: UserInfoRedis, loginer: Login, requester: PostRequest,
                 reporter: Reporter, ) -> None: ...

    def selectReport(self, user: str, passw: str, flag: Union[int, bool]) -> None: ...

    def dayReport(self, user: str, passw: str) -> None: ...

    def userPoll(self, user: str, passw: str, start_date: str) -> None: ...

    def schedule(self): ...


class Actuator(Launcher):
    def __init__(self, accounts: UserInfoRedis, loginer: Login, requester: PostRequest, reporter: Reporter) -> None: ...

    def Sun_Moon(self, flag: Union[int, bool]) -> None: ...

    def NewUser(self) -> None: ...

    def NewUserTotal(self): ...

    def schedule(self) -> None: ...


class TroubleRemoval(Launcher):
    def __init__(self, accounts: UserInfoRedis, loginer: Login, requester: PostRequest, reporter: Reporter) -> None: ...

    def Total(self) -> None: ...


class VocationActuator(Actuator):
    '''The vocation version for day-report.'''