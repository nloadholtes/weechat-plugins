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


def gh_watch_cb(data, signal, signal_data):
    server = signal.split(",")[0]
    msg = weechat.info_get_hashtable("irc_message_parse", {"message": signal_data})
    buffer = weechat.buffer_search("python", "GithubWatcher")
    # print("In join_cb: %s " % msg)
    if buffer:
        output = "%s (%s) has joined this channel?" % (msg["nick"], msg["channel"])
        weechat.prnt(buffer, output)
        # weechat.prnt_date_tags(buffer, 0, "", output)  # Throws down a datestamp
        weechat.buffer_set(buffer, "hotlist", "3")  # Sets the color of the bufferlist channel to magenta
    return weechat.WEECHAT_RC_OK


if __name__ == "__main__":
    weechat.register("github_watcher", "GithubWatcher", "1.0", "MIT",
                     "Keeping an eye on github messages", "gw_watch_end", "")
    weechat.prnt("", "Github watcher (python) started")
    buffer = weechat.buffer_new("GithubWatcher", "buffer_input_cb", "", "buffer_close_cb", "")
    weechat.buffer_set(buffer, "title", "Watching Github messages")
    weechat.buffer_set(buffer, "localvar_set_no_log", "0")

    weechat.hook_signal("*,irc_in2_join", "join_cb", "")
