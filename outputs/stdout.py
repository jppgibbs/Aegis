# coding: utf-8

from __future__ import division
import sys, calendar, itertools, hashlib, urllib2
from collections import OrderedDict

import zxcvbn

END = ""
WHITE = ""
UNDERLINE = ""
GREEN = ""
YELLOW = ""
ORANGE = ""
RED = ""
DIM = ""
HIBP_CHECK_API = "https://api.pwnedpasswords.com/range/{}"


def add_args(parser):
    group = parser.add_argument_group("stdout module options")
    group.add_argument('--limit', default=20, type=int, help="Limit each section to")
    group.add_argument('--no-hibp', action="store_true", default=False,
                       help="Checks to see if password appears in Have I Been Pwned (password is never transmitted to the server)")
    args, unknown_args = parser.parse_known_args()

    return args


def run(db, args):
    total, local_users, domain_users, computers = db.counts

    print("Aegis report for {}\n".format(args.domain))
    print("Local / Domain users:\t{}/{}".format(local_users, domain_users))

    if not args.only_enabled:
        print("Enabled / disabled users:\t{}/{}".format(*db.user_counts))

    if not args.only_users:
        print("Computer accounts:\t{}\t{:.2f}%".format(computers, (computers / total) * 100))

    cracked, blank, historic = db.password_stats
    print("Passwords cracked:\t{}/{}\t{:.2f}%".format(cracked, total, (cracked / total) * 100))
    print("Historic passwords:\t{}\t{:.2f}%".format(historic, (historic / total) * 100))

    only_alpha, with_special, only_digits = db.password_composition_stats
    print(UNDERLINE + "\nPassword composition" + END)
    print("Only alphanumeric:\t{}\t{:.2f}%".format(only_alpha, (only_alpha / total) * 100))
    print("Only digits:\t{}\t{:.2f}%".format(only_digits, (only_digits / total) * 100))
    print("With 'special char':\t{}\t{:.2f}%".format(with_special, (with_special / total) * 100))

    headers = ["Password", "Length", "Count", "Score", "Pwned", "Users"]
    fmt_lambda = lambda password, count, score, users: [password, len(password), count, score,
                                                        __get_usage(password) if not args.no_hibp else '',
                                                        __process_users(users)]
    default_align = ["<", "<", "<", "<", "<", ""]
    #default_align = [">", "<", "<", "<", "<", ""]

    top_passwords = db.get_passwords(sortby=lambda (password, count, score, users): (count, score, len(password)),
                                     reverse=True, limit=args.limit)
    __print_table(title="Top {} Passwords (by use, score)".format(args.limit), headers=headers, align=default_align,
                  values=top_passwords, format=fmt_lambda)

    bad_pass = db.get_passwords(sortby=lambda (password, count, score, users): (
    zxcvbn.password_strength(password)["score"], len(password), len(users)), reverse=False, limit=args.limit)
    __print_table(title="Top {} Worst Passwords (by score, length)".format(args.limit), headers=headers,
                  align=default_align, values=bad_pass, format=fmt_lambda)

    passwords = db.get_passwords_where(lambda password: password != "")
    __graph_passwords_containing("Passwords containing months", passwords,
                                 OrderedDict([(calendar.month_name[m], 0) for m in range(1, 13)]))
    __graph_passwords_containing("Passwords containing days", passwords,
                                 OrderedDict([(calendar.day_name[d], 0) for d in range(0, 7)]))

    print(UNDERLINE + "\nPassword length distribution" + END)
    grpd_passwords = ((p, len(list(count))) for p, count in
                      itertools.groupby(sorted(passwords, key=lambda r: len(r["password"])),
                                        lambda r: len(r["password"])))
    keys, vals = map(list, zip(*grpd_passwords))
    vals_percents = [" ({:.2f}%)".format((v / total) * 100) for v in vals]
    __print_graph(keys, vals, vals_percents)


def __print_table(title, headers, align, values, format):
    fmt = "".join(["{:" + align[headers.index(x)] + str(int(len(x) * 1.75)) + "}\t".expandtabs() for x in headers])
    print(UNDERLINE + "\n{}".format(title) + END)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * len(header) for header in headers]))

    for item in values:
        print(fmt.format(*format(*item)))


def __coloured_score(score, text=None):
    colormap = {0: RED, 1: ORANGE, 2: YELLOW, 3: GREEN, 4: WHITE}
    return "{}{:<8}{}".format(colormap[score], text or score, END)


def __get_usage(password):
    try:
        sha1_password = hashlib.sha1(password).hexdigest().upper()
        request = urllib2.Request(HIBP_CHECK_API.format(sha1_password[:5]), headers={"User-Agent": "Aegise-dit"})
        response = urllib2.urlopen(request).read()
        lines = dict(map(lambda line: line.split(":"), response.split("\r\n")))
        passwords = {password: int(count) for password, count in lines.iteritems()}

        return "{:,}".format(passwords.get(sha1_password[5:]) or 0)
    except:
        return "-"


def __process_users(users):
    return ", ".join(__process_user(user) for user in users)


def __process_user(user):
    uname = user["username"]

    if "historic" in user:
        return "{}{}{}".format(DIM, uname, END)
    elif "enabled" in user and not user["enabled"]:
        return "{}{}{}".format(RED, uname, END)
    else:
        return "{}{}{}".format(GREEN, uname, END)


def __process_passwords(passwords):
    out = []

    for p, users in passwords:
        out.append(__coloured_score(zxcvbn.password_strength(p)["score"], p))

    return ", ".join(out)


def __graph_passwords_containing(title, passwords, list):
    for row in passwords:
        for key in list:
            if key.lower() in row["password"].lower():
                list[key] += 1

    if any(val for val in list.values()):
        print((UNDERLINE + "\n{0}" + END).format(title))
        __print_graph(list.keys(), list.values())


def __print_graph(labels, data, data_labels=None):
    width = 50
    val_min = min(data)
    val_max = max(data)
    normalised = data if val_max < width else [(_v - val_min) * (width / float(val_max - val_min)) for _v in data]

    for i in range(len(labels)):
        value = data[i]
        data_label = data_labels[i] if data_labels is not None else ""
        blocks = int(normalised[i])

        sys.stdout.write("{:>15}: ".format(labels[i]))
        if blocks < 1 and (value > val_min or value > 0):
            sys.stdout.write("▏")
        else:
            for _ in range(blocks):
                sys.stdout.write("▇")

        print("   {}{}".format(value, data_label))