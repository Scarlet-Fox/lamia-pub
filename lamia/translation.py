"""The translation global for lamia are setup here."""
import gettext
import os

locale = os.path.dirname(__file__) + ('/locales')
gettext.bindtextdomain('lamia', locale)
gettext.textdomain('lamia')
en = gettext.translation('lamia', locale, ['en'])
gettext = gettext.gettext
