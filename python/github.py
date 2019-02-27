import re
try:
    import weechat
except ImportError:
    print("This script must be run from inside weechat")
    exit -1


def gh_watch_end():
    """Looks like we were told to stop"""
    return weechat.WEECHAT_RC_OK


def buffer_input_cb(data, buffer, input_data):
    return weechat.WEECHAT_RC_OK


def buffer_close_cb(data, buffer):
    return weechat.WEECHAT_RC_OK


def gh_watch_cb(data, bufferp, date, tags, disp, high, prefix, msg):
    if "github\x1c :]" not in prefix:
        return weechat.WEECHAT_RC_OK
    if msg.startswith("[ http"):
        return weechat.WEECHAT_RC_OK
    buffer = weechat.buffer_search("python", "GithubWatcher")
    if buffer:
        # print("tags: %s " % tags)
        # print("disp: %s " % disp)
        # print("high: %s " % high)
        # print("prefix: '%r'" % prefix)
        if msg[0] == "[":
            chunked_msg = msg.split("")
            print("unhandled msg:%s" % msg)
        if msg.startswith("https://github"):
            chunked_msg = re.split("\(|\)", msg)
            if len(chunked_msg)<3:
                print("wrong message type: %s" % chunked_msg)
                return weechat.WEECHAT_RC_OK
            where = chunked_msg[1]
            what = chunked_msg[3]
            who = chunked_msg[4]
            weechat.prnt(buffer, "%s -- %s -- %s" % (where, what, who))
        else:
            weechat.prnt(buffer, msg)
        weechat.buffer_set(buffer, "hotlist", "3")  # Sets the color of the bufferlist channel to magenta
    return weechat.WEECHAT_RC_OK


if __name__ == "__main__":
    weechat.register("github_watcher", "GithubWatcher", "1.0", "MIT",
                     "Keeping an eye on github messages", "gh_watch_end", "")
    weechat.prnt("", "Github watcher (python) started")
    buffer = weechat.buffer_new("GithubWatcher", "buffer_input_cb", "", "buffer_close_cb", "")
    weechat.buffer_set(buffer, "title", "Watching Github messages")
    weechat.buffer_set(buffer, "localvar_set_no_log", "0")

    weechat.hook_print("", "", "", 0, "gh_watch_cb", "")
