from Launcher import Launcher,UserInfoRedis,Login,PostRequest,Reporter
from Reporter import AsyncReporter


def main():
    accounts = UserInfoRedis()
    loginer = Login(...,...)
    req_obj = PostRequest()
    # reporter = Reporter()
    reporter = AsyncReporter()
    launch = Launcher(accounts=accounts,loginer=loginer,requester=req_obj,reporter=reporter)
    launch.schedule()
    # launch.Sun_Moon(1)
    

if __name__ == "__main__":
    main()