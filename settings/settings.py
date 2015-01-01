import json
import logging
import os

logger = logging.getLogger("settings")


def _init_dirs(path):
    """Helper function to make the directories in `path` if they don't exist

    Path should only consist of directories, to avoid making a directory with
    a filename extension, but we will put in place checks against this.
    """
    if not os.path.exists(path):  # path doesn't exist, safe to proceed
        # make sure the path doesn't look file-like
        end_of_path = os.path.split(path)[-1]
        if ("." in end_of_path) and (not end_of_path.startswith(".")):
            dirs, filename = os.path.split(path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
        else:
            os.makedirs(path)



class _Setting(object):
    def __init__(self, value, on_changed=None):
        self._value = value
        self._on_changed = on_changed

    def get(self):
        return self._value

    def set(self, value):
        self._value = value
        if self._on_changed:
            self._on_changed(value)

    def assign_on_changed_callback(self, callback):
        self._on_changed = callback


class JSONSettings(object):
    """Settings saved on disk as JSON, given a certain path"""

    def __init__(self, path):
        self._path = path
        self._settings = {}

    def _save(self):
        """Persist json representation of `self._settings` to disk

        This is done by calling `get` on each `_Setting` object.
        """
        json_settings = {}
        for k, v in self._settings.items():
            json_settings[k] = v.get()

        with open(self._path, "wb") as settings:
            settings.write(json.dumps(json_settings))

    def load(self):
        """Load existing settings, as json, from disk

        We read the keys and values of the settings in as raw json, but our,
        internal memory representation is a dictionary with k/v pairs where
        the values are `_Setting` objects.
        """

        # make sure the directory path exists
        _init_dirs(self._path)

        if os.path.exists(self._path):
            with open(self._path, "rb") as settings:
                try:
                    json_settings = json.loads(settings.read())
                    for k, v in json_settings.items():
                        self._settings[k] = _Setting(v)
                        setting = self._settings[k]
                    logger.info("Settings successfully loaded %s" % setting.get())
                    return
                except Exception, e:
                    logger.warn("Corrupt settings file, %s, blowing away" % e)

        # the settings file doesn't exist or is corrupt, let's make a new one
        with open(self._path, "wb"):
            logger.info("New settings file created %s" % self._path)

    def add_setting(self, name, default, on_changed=None):
        """Add a setting with a default value, if it doesn't exist already

        If the setting does exist, we still need to assign them the custom
        setter/getters because these are lost when persisting to disk
        """
        setting = self._settings.get(name)
        if setting:
            logger.info("Ignoring default for setting %s" % name)
            setting.assign_on_changed_callback(on_changed)
        else:
            self._settings[name] = _Setting(default, on_changed)
            logger.info("New setting added %s with default %s", name, default)

        self._save()

    def set(self, name, value):
        """Set the value of a setting"""
        setting = self._settings.get(name)
        if setting:
            setting.set(value)
            self._save()

    def get(self, name):
        """Get the value of a setting"""
        setting = self._settings.get(name)
        if setting:
            return setting.get()

    def to_dict(self):
        dict_settings = {}
        for k, v in self._settings.items():
            dict_settings[k] = v.get()
        return dict_settings
