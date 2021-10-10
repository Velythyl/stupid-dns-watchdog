import os
import subprocess
from datetime import datetime

def run(input, exception_on_failure=True, redirect_stderr=False):
    try:
        import subprocess
        print("\t"+input)
        program_output = subprocess.check_output(f"{input}", shell=True, universal_newlines=True,
                                                 stderr=subprocess.STDOUT if redirect_stderr else None)
    except Exception as e:
        program_output = e.output
        if exception_on_failure:
            print("\t\t"+program_output)
            raise e

    print("\t\t"+program_output)

    return program_output.strip()

def get_host_id():
    return run("cat /etc/machine-id")+".machine"

CONFIG_ROOT = run("echo $HOME")+"/.stupid_dns_watchdog"

def get_config_repo():
    configpath = CONFIG_ROOT

    import os
    assert os.path.isdir(configpath)

    if not os.path.isdir(configpath+"/repo"):
        print("You need to call `sdw init <github url>` first.")
        exit()

    return configpath+"/repo"

def get_latest_cached_ip():
    repo_path = get_config_repo()

    run(f"touch {repo_path}/{get_host_id()}")
    ret = run(f"cat {repo_path}/{get_host_id()}")
    return ret.split("\n")[-1].split(",")[-1]

def get_current_ip():
    return run("curl ifconfig.me")

def get_date():
    x = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return x

def write_ip(ip):
    run(f"cd {get_config_repo()} && git pull --force", redirect_stderr=True)

    run(f"echo \"{get_date()},{ip}\" >> {get_config_repo()}/{get_host_id()}")

    try:
        run(f"cd {get_config_repo()} && git add * && git commit -a -m \"SDW {get_date()}\" && git push", redirect_stderr=True)
    except:
        run(f"echo \"{get_date()}\" > {CONFIG_ROOT}/MANUAL_RUN.txt")


def check():
    current_ip = get_current_ip()
    if current_ip == get_latest_cached_ip():
        print("No changes detected. SDW will exit now.")
        exit(0)

    # we need to warn our master on her github
    write_ip(current_ip)

def mkconf():
    try:
        os.makedirs(CONFIG_ROOT)
    except FileExistsError:
        pass

def main():
    mkconf()

    import sys
    if sys.argv[1] == "init":
        run(f"git clone {sys.argv[2]} {CONFIG_ROOT}/repo")

        from crontab import CronTab
        cron = CronTab(user=True)
        job = cron.new(command="sdw check", comment=f"SDW on {get_date()}")
        job.hour.every(2)
        cron.write()

        print("Successfully inited SDW. If you had already done so on this machine, don't forget to delete the old CRON file.")

        print("\n\nRunning initial check now.\n\n")
        check()

    elif sys.argv[1] == "check":
        check()
    else:
        raise NotImplemented()


if __name__ == "__main__":
    main()