try:
    import weechat
except ImportError:
    print("This script must be run from inside weechat")
    exit -1


def highlight_end():
    """Looks like we were told to stop"""
    return weechat.WEECHAT_RC_OK


def buffer_input_cb(data, buffer, input_data):
    return weechat.WEECHAT_RC_OK


def buffer_close_cb(data, buffer):
    return weechat.WEECHAT_RC_OK


def join_cb(data, signal, signal_data):
    # signal is for example: "freenode,irc_in2_join"
    # signal_data is IRC message, for example: ":nick!user@host JOIN :#channel"
    server = signal.split(",")[0]
    msg = weechat.info_get_hashtable("irc_message_parse", {"message": signal_data})
    buffer = weechat.buffer_search("python", "Highlight")
    # print("In join_cb: %s " % msg)
    if buffer:
        output = "%s (%s) has joined this channel?" % (msg["nick"], msg["channel"])
        weechat.prnt(buffer, output)
        # weechat.prnt_date_tags(buffer, 0, "", output)  # Throws down a datestamp
        weechat.buffer_set(buffer, "hotlist", "3")  # Sets the color of the bufferlist channel to magenta
    return weechat.WEECHAT_RC_OK


def modifier_cb(data, modifier, modifier_data, string):
    # add server name to all messages received
    # (OK that's not very useful, but that's just an example!)
    # print("data: %s" % data)  # Blank?
    # print("modifier: %s" % modifier)  # irc_in_PRIBMSG
    # print("modifier_data: %s" % modifier_data)  # znc
    return "%s" % string


if __name__ == "__main__":
    weechat.register("highlight_python", "Highlight", "1.0", "MIT",
                     "User defineable things to highlight", "highlight_end", "")
    weechat.prnt("", "Highlight (python) started")
    buffer = weechat.buffer_new("Highlight", "buffer_input_cb", "", "buffer_close_cb", "")
    weechat.buffer_set(buffer, "title", "Highlights and mentions")
    weechat.buffer_set(buffer, "localvar_set_no_log", "1")

    # Temp, just to test
    # weechat.hook_signal("*,irc_in2_join", "join_cb", "")
    weechat.hook_modifier("irc_in_privmsg", "modifier_cb", "")
