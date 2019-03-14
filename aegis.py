import sys, glob, os, argparse, itertools, time
from threading import Thread, Event

import ntds_parser as ntds, outputs
from database import HashDatabase, DomainDoesntExist

# BANNER = """\033[91m
#
#  $$$$$$\                      $$\
# $$  __$$\                     \__|
# $$ /  $$ | $$$$$$\   $$$$$$\  $$\  $$$$$$$\
# $$$$$$$$ |$$  __$$\ $$  __$$\ $$ |$$  _____|
# $$  __$$ |$$$$$$$$ |$$ /  $$ |$$ |\$$$$$$\
# $$ |  $$ |$$   ____|$$ |  $$ |$$ | \____$$\
# $$ |  $$ |\$$$$$$$\ \$$$$$$$ |$$ |$$$$$$$  |
# \__|  \__| \_______| \____$$ |\__|\_______/
#                     $$\   $$ |
#                     \$$$$$$  |
#                      \______/
# \033[0m\033[91m\n"""


if __name__ == "__main__":
   # print(BANNER)
    available_outputs = ", ".join(outputs.discover_outputs().keys())

    parser = argparse.ArgumentParser(add_help=False, description="Aegis makes it easier to perform password "
                                                                "audits against Windows-based corporate environments.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--database-name", default="db.json", action="store")
    parser.add_argument("--help", action="store_true", required=False)

    group = parser.add_argument_group("1. Cracking", "ke-dit can take your raw ntds.dit and SYSTEM hive "
                                                              "and turn them in to a user:hash file for cracking "
                                                              "within your favourite password cracker")
    group.add_argument("--system", action="store")
    group.add_argument("--ntds", action="store")
    group.add_argument("--username", action="store")
    group.add_argument("--password", action="store")
    group.add_argument("--target", action="store")
    group.add_argument("--out", action="store")
    group.add_argument("--no-history", action="store_false", dest="historic", default=True)

    group = parser.add_argument_group("2. Reporting", "use these options to process a hash:password file from "
                                                        "your favourite password cracker")
    group.add_argument("--pot", action="store")
    group.add_argument("--domain", action="store")
    group.add_argument("--only-enabled", action="store_true", dest="only_enabled", default=False)
    group.add_argument("--only-users", action="store_true", dest="only_users", default=False)
    group.add_argument("--output", action="store", default="stdout")

    args, unknown_args = parser.parse_known_args()
    args = outputs.get_output_by_name(args.output).add_args(parser)

    local = (args.system and args.ntds)
    remote = (args.username and args.password and args.target)

    if local or remote:
        domain, records = ntds.process_local(args.system, args.ntds, args.historic) if local else ntds.process_remote(args.username, args.password, args.target, args.historic)
        ntlm_file = args.out or "{0}.hashes.ntlm".format(domain)

        with HashDatabase(args.database_name, domain, raise_if_table_doesnt_exist=False) as db:
            with open(ntlm_file, "w+") as out:
                for record in records:
                    out.write("%s:%s%s" % (record["username"], record["ntlmhash"], os.linesep))
                    db.insert(record)

        print("Found {} hashes for '{}', available at {}. Run them through your favourite password cracker and re-run Aegis with --pot - see README for tips!".format(len(records), domain, ntlm_file))
    elif args.pot and args.domain:
        def __update(stopper):
            spinner = itertools.cycle(['-', '/', '|', '\\'])

            while not stopper.is_set():
                #sys.stdout.write("[" + spinner.next() + "] Processing...\r")
                sys.stdout.flush()
                time.sleep(0.2)

        def __opendb(domain):
            with HashDatabase(args.database_name, domain, raise_if_table_doesnt_exist=True, only_enabled=args.only_enabled, only_users=args.only_users) as db:
                try:
                    with open(args.pot, "r") as pot:
                        for line in pot:
                            line = line.rstrip("\r\n").replace("$NT$", "")  # $NT$ for John
                            hash, password = map(str.strip, line.split(":"))

                            if password:
                                db.update_hash_password(hash, password)

                    outputs.get_output_by_name(args.output).run(db, args)
                except IOError:
                    print("Failed to read '{}'. Make sure the file exists and is readable.".format(args.pot))
                    print("Did you mean: {}?".format(", ".join(glob.glob("*.pot"))))

        stopper = Event()
        spinner = Thread(target=__update, args=(stopper,))
        spinner.start()

        try:
            __opendb(args.domain)
        except DomainDoesntExist as e:
            print(e.message)
            print("Did you mean: {}?".format(", ".join(e.tables[1:])))
        finally:
            stopper.set()
            spinner.join()
    else:
        parser.print_help()
