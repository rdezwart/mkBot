from configparser import ConfigParser


def check_config(config: ConfigParser):

    print("Checking config file...")

    if len(config.read("config.ini")) > 0:
        print("\tExists: True")

        if check_sections(config):
            print("\tSections: True")

            if check_options(config):
                print("\tOptions: True")
                return True
            else:
                return False
        else:
            return False
    else:
        print("\tExists: False")
        print("\nError: No 'config.ini' found in root directory, see README for an example.")
        return False


def check_sections(config: ConfigParser):
    if not config.has_section("bot"):
        print("\tSections: False")
        print("\nError: 'bot' section is missing.")
        return False
    elif not config.has_section("esix"):
        print("\tSections: False")
        print("\nError: 'esix' section is missing.")
        return False

    return True


def check_options(config: ConfigParser):
    if not config.has_option("bot", "nick"):
        print("\tOptions: False")
        print("\nError: 'bot.nick' option is missing.")
        return False
    elif not config.has_option("bot", "pass"):
        print("\tOptions: False")
        print("\nError: 'bot.pass' option is missing.")
        return False

    elif not config.has_option("esix", "agent"):
        print("\tOptions: False")
        print("\nError: 'esix.agent' option is missing.")
        return False
    elif not config.has_option("esix", "name"):
        print("\tOptions: False")
        print("\nError: 'esix.name' option is missing.")
        return False
    elif not config.has_option("esix", "key"):
        print("\tOptions: False")
        print("\nError: 'esix.key' option is missing.")
        return False

    return True
