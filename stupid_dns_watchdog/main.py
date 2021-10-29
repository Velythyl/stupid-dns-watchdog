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

CONFIG_ROOT = run("echo $HOME")+"/.stupid_dns_watchdog"

def get_config_repo(repo_name):
    configpath = CONFIG_ROOT

    import os
    assert os.path.isdir(configpath)

    if not os.path.isdir(configpath+f"/{repo_name}"):
        print("You need to call `sdw init <github url>` first.")
        exit()

    return configpath+f"/{repo_name}"

def get_latest_cached_ip(repo_name, machine_name):
    repo_path = get_config_repo(repo_name)

    run(f"touch {repo_path}/{machine_name}")
    ret = run(f"cat {repo_path}/{machine_name}")
    return ret.split("\n")[-1].split(",")[-1]

def get_current_ip():
    return run("curl ifconfig.me")

def get_date():
    x = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return x

def write_ip(ip, repo_name, machine_name):
    run(f"cd {get_config_repo(repo_name)} && git pull --force", redirect_stderr=True)

    run(f"echo \"{get_date()},{ip}\" >> {get_config_repo(repo_name)}/{machine_name}")

    try:
        run(f"cd {get_config_repo(repo_name)} && git add * && git commit -a -m \"SDW {get_date()}\" && git push", redirect_stderr=True)
    except:
        run(f"echo \"{get_date()}\" > {CONFIG_ROOT}/MANUAL_RUN.txt")


def check(repo_name, machine_name):
    repo_name = run(f"basename {repo_name} .git")

    current_ip = get_current_ip()
    if current_ip == get_latest_cached_ip(repo_name, machine_name):
        print("No changes detected. SDW will exit now.")
        exit(0)

    # we need to warn our master on her github
    write_ip(current_ip, repo_name, machine_name)

def mkconf():
    try:
        os.makedirs(CONFIG_ROOT)
    except FileExistsError:
        pass

def main():
    mkconf()

    import sys
    if sys.argv[1] == "init":
        repo_name = run(f"basename {sys.argv[2]} .git")
        run(f"git clone {sys.argv[2]} {CONFIG_ROOT}/{repo_name}", redirect_stderr=True)

        from crontab import CronTab
        cron = CronTab(user=True)
        job = cron.new(command=f"sdw check {repo_name} {sys.argv[3]}", comment=f"SDW on {get_date()} for {repo_name}")
        job.hour.every(2)
        cron.write()

        print("Successfully inited SDW. If you had already done so on this machine, don't forget to delete the old CRON file.")

        print("\n\nRunning initial check now.\n\n")
        check(repo_name, sys.argv[3])

    elif sys.argv[1] == "check":
        check(sys.argv[2], sys.argv[3])
    else:
        raise NotImplemented()


if __name__ == "__main__":
    main()