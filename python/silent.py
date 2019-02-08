try:
    import weechat
except ImportError:
    print("This script must be run from inside weechat")
    exit -1


def silent_end():
    """Looks like we were told to stop"""
    return weechat.WEECHAT_RC_OK


if __name__ == "__main__":
    weechat.register("silent_python", "Silent", "1.0", "MIT",
                     "Make a user silent", "silent_end", "")
    weechat.prnt("", "Silent Python started?")
