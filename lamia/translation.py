"""The translation global for lamia are setup here."""
# pylint: disable=invalid-name
import gettext
import os

locale = os.path.dirname(__file__) + ('/locales')
gettext.bindtextdomain('lamia', locale)
gettext.textdomain('lamia')
EN = gettext.translation('lamia', locale, ['en'])
gettext = gettext.gettext
_ = gettext