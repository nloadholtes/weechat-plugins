try:
    import weechat
except ImportError:
    print("This script must be run from inside weechat")
    exit -1


def collapse_end():
    """Looks like we were told to stop"""
    return weechat.WEECHAT_RC_OK


def collapse_cb(data, modifier, modifier_data, string):
    # msg = weechat.info_get_hashtable("irc_message_parse", {"message": signal_data})
    
    chunked_msg = string.split()  # TODO: get the right field
    where = chunked_msg[1]
    what = chunked_msg[5]
    who = chunked_msg[-1]
    return "%s -- %s -- %s" % (where, what, who)
    

if __name__ == "__main__":
    weechat.register("collapse_python", "Collapse", "1.0", "MIT",
                     "Collapse long messages (think github notifications) into more readable messages.", "collapse_end", "")
    weechat.hook_modifier("irc_in_privmsg", "modifier_cb", "")
    weechat.prnt("", "Collapse (python) started")
