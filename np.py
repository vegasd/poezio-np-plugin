#!/usr/bin/python3

from subprocess import Popen, PIPE
from datetime import date

# {{{ Only for poezio plugin
try:
    from plugin import BasePlugin
    import common
    import tabs
except:
    pass
else:
    class Plugin(BasePlugin):
        """Plugin for poezio"""
        def init(self):
            self.add_tab_command(
                tabs.MucTab,
                'np',
                self.command_np,
                "Отправляет в конфу сообщение о прослушиваемой композиции"
            )

        def command_np(self, args):
            args = " ".join(common.shell_split(args))  # костыль
            mes = get_np_message(get_np_info())
            if not args:
                r = "{}.".format(mes)
            else:
                a = args.strip()
                if a[0] not in ('.,!:;?…'):
                    a = " " + a
                r = "{}{}".format(mes, a)
            self.core.send_message(r)
# }}} Only for poezio plugin


def isfeminine(word):
    if word in ("антологии", "песню",
                "композицию", "инструментальную композицию"):
        return True
    else:
        return False


def get_np_info():
    # TODO: use dbus here except of runnig a shell command
    cmd = 'deadbeef --nowplaying-tf "{}"'
    OPTIONS = ("artist", "title", "year", "genre", "albumartist",
               "album", "composer", "comment", "releasetype",
               "playback_time_remaining_seconds", "length_seconds")
    DELIMITER = " -=- "
    fmt = DELIMITER.join("%{}%".format(x) for x in OPTIONS)
    out, err = Popen(cmd.format(fmt), shell=True,
                     stdout=PIPE, stderr=PIPE).communicate()
    x = out.decode("utf-8").split(DELIMITER)
    t = {}
    for field in OPTIONS:
        t[field] = x.pop(0)
    t["reltype"] = t["releasetype"]
    return t


def istracknoname(t):
    title = t["title"].lower().strip()
    if title in ("intro", "outro", "instrumental", "untitled") or not title:
        return True
    else:
        return False


def istracksamename(t):
    if t['title'].lower() == t['artist'].lower():
        return True
    else:
        return False


def get_what(t):
    genre = t["genre"].lower().strip()
    title = t["title"].lower().strip()
    x = title.split() or ['']
    firstword, lastword = x[0].strip("()[]"), x[-1].strip("()[]")

    if 'clas' in genre:
        st = "композицию"
    elif any(x in genre for x in ('ambient', 'noise', 'drone', "instrumental")):
        st = "трек"
    elif lastword == 'instrumental' or "instrumental" in t["comment"].lower():
        st = "инструментальную композицию"
    elif "intro" in (lastword, firstword):
        st = "интро"
    elif "outro" in (lastword, firstword):
        st = "аутро"
    else:
        st = "песню"

    if istracknoname(t):
        if st not in ("интро", "аутро"):
            nn = "безымянную " if isfeminine(st) else "безымянный "
        else:
            nn = ""
        return nn + st
    elif istracksamename(t):
        nn = "одноименную " if isfeminine(st) else "одноименный "
        return nn + st
    else:
        return " ".join((st, "«{}»".format(t["title"])))


def isalbumnoname(t):
    if t['album'].lower() in ('demo', "split"):
        return True
    else:
        return False


def isalbumsamename(t):
    if t['title'].lower() == t['album'].lower():
        return True
    else:
        return False


def guess_reltype(t):
    if t['albumartist'].lower() == "va" \
            or 'various' in t['albumartist'].lower() \
            or t['albumartist'].count(" & ") > 4:
        return "Compilation"
    if " & " in t["albumartist"] and t['artist'] == t['albumartist']:
        return "Collaboration"
    if 0 < t['albumartist'].count(" & ") < 5:
        return "Split"
    return "Album"


def get_from(t):
    RTYPES = {"demo": "демо",
              "anthology": "антологии",
              "ep": "EP",
              "album": "альбома",
              "compilation": "сборника",
              "split": "сплита",
              "collaboration": "совместного альбома",
              "single": "сингла"}

    if t["reltype"]:
        reltype = t["reltype"].lower()
    else:
        reltype = guess_reltype(t).lower()

    if reltype in RTYPES:
        relstring = RTYPES[reltype]
    elif t["reltype"]:
        relstring = t["reltype"]

    noname = isalbumnoname(t)
    samename = isalbumsamename(t)

    result = []

    # Предлог
    if reltype in ("split", "compilation") and not noname and not samename:
        result.append("со")
    else:
        result.append("с")

    # Прилагательные
    if samename:
        result.append("одноименной" if isfeminine(relstring)
                      else "одноименного")
    if noname:
        result.append("безымянной" if isfeminine(relstring)
                      else "безымянного")

    # Существительное
    result.append(relstring)

    # Дополнение (для сплитов)
    if reltype == "split":
        artists = t['albumartist'].split(' & ')
        artist_is_on_split = t['artist'] in artists
        if artist_is_on_split:
            artists.remove(t['artist'])
        s = " и ".join(artists)
        if s:
            result.append("с " + s)

    # Название
    if not noname and not samename:
        if reltype == "split":
            result.append("под названием")
        result.append("«{}»".format(t["album"]))

    return " ".join(result)


def get_np_message(t):
    if t is None:
        return "/me ничего не слушает"
    if 'clas' in t['genre'].lower():
        res = ("{action} {composer}, " +
               "композицию «{title}» в исполнении {artist} {year} года")

    t["action"] = "слушает"
    t["what"] = get_what(t)
    t["from"] = get_from(t)

    # TODO:
    # if float(t["playback_time_remaining_seconds"]) < 30 \
    #         and float(t["length_seconds"]) > 120:
    #     t["action"] = "дослушивает"

    cur_year = date.today().year
    try:
        albyear = int(t["year"])
    except:
        pass
    else:
        if albyear == cur_year - 1:
            t["year"] = "прошлого"
        elif albyear == cur_year - 2:
            t["year"] = "позапрошлого"

    res = "{action} {artist}, {what} {from} {year} года"
    return "/me " + res.format(**t)


if __name__ == "__main__":
    print(get_np_message(get_np_info()))
