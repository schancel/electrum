from electroncash.keyserver.tools import *
from electroncash.i18n import _

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from .util import *


def telegram_executor(handle: str):
    QDesktopServices.openUrl(QUrl("https://t.me/" + handle))


class KeyserverForm(QWidget):
    def is_full(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def _get_data(self):
        raise NotImplementedError

    def _construct_metadata(self, addr: str, data, signer, ttl: int):
        raise NotImplementedError

    def _get_ttl(self):
        raise NotImplementedError

    def set_signer(self, signer):
        self.signer = signer

    def construct_metadata(self, addr):
        data = self._get_data()
        metadata = self._construct_metadata(
            addr, data, self.signer, ttl=self._get_ttl())
        return metadata


class PlainTextForm(KeyserverForm):
    def __init__(self, on_text_changed, *args, **kwargs):
        super(PlainTextForm, self).__init__(*args, **kwargs)
        plain_text_grid = QGridLayout()
        msg = _('Plain text to be uploaded.')
        description_label = HelpLabel(_('&Text'), msg)
        plain_text_grid.addWidget(description_label, 3, 0)
        self.upload_plain_text_e = QTextEdit()
        self.upload_plain_text_e.textChanged.connect(on_text_changed)
        description_label.setBuddy(self.upload_plain_text_e)
        plain_text_grid.addWidget(self.upload_plain_text_e, 3, 1, 1, -1)
        self.setLayout(plain_text_grid)

    def is_full(self):
        return bool(self.upload_plain_text_e.toPlainText())

    def clear(self):
        self.upload_plain_text_e.clear()

    def _get_ttl(self):
        return 60*60

    def _get_data(self):
        return self.upload_plain_text_e.toPlainText()

    def _construct_metadata(self, addr, data, signer, ttl):
        return plain_text_metadata(addr, data, signer, ttl)


class TelegramForm(KeyserverForm):
    def __init__(self, on_text_changed, *args, **kwargs):
        super(TelegramForm, self).__init__(*args, **kwargs)
        plain_text_grid = QGridLayout()
        msg = _('Telegram handle to be uploaded.')
        description_label = HelpLabel(_('&Handle'), msg)
        plain_text_grid.addWidget(description_label, 3, 0)
        self.upload_telegram_e = QLineEdit()
        self.upload_telegram_e.textChanged.connect(on_text_changed)
        description_label.setBuddy(self.upload_telegram_e)
        plain_text_grid.addWidget(self.upload_telegram_e, 3, 1, 1, -1)
        self.setLayout(plain_text_grid)

    def is_full(self):
        return bool(self.upload_telegram_e.text())

    def clear(self):
        self.upload_telegram_e.clear()

    def _get_ttl(self):
        return 60*60

    def _get_data(self):
        return self.upload_telegram_e.text()

    def _construct_metadata(self, addr, data, signer, ttl):
        return plain_text_metadata(addr, data, signer, ttl, type_override="telegram")


class PeerListForm(KeyserverForm):
    def __init__(self, on_text_changed, *args, **kwargs):
        super(PeerListForm, self).__init__(*args, **kwargs)
        plain_text_grid = QGridLayout()
        msg = _('Keyserver list to be uploaded. Line delimited.')
        description_label = HelpLabel(_('&Servers'), msg)
        plain_text_grid.addWidget(description_label, 3, 0)
        self.upload_ks_urls_e = QTextEdit()
        self.upload_ks_urls_e.textChanged.connect(on_text_changed)
        description_label.setBuddy(self.upload_ks_urls_e)
        plain_text_grid.addWidget(self.upload_ks_urls_e, 3, 1, 1, -1)
        self.setLayout(plain_text_grid)

    def is_full(self):
        return bool(self.upload_ks_urls_e.toPlainText())

    def clear(self):
        self.upload_ks_urls_e.clear()

    def _get_ttl(self):
        return 60*60

    def _get_data(self):
        urls = self.upload_ks_urls_e.toPlainText().split("\n")
        return urls

    def _construct_metadata(self, addr, urls, signer, ttl):
        return ks_urls_metadata(addr, urls, signer, ttl)

# TODO
class StealthAddressForm(KeyserverForm):
    def __init__(self, on_text_changed, *args, **kwargs):
        super(StealthAddressForm, self).__init__(*args, **kwargs)

    def is_full(self):
        return bool(self.upload_telegram_e.text())

    def clear(self):
        pass

    def _get_data(self):
        return None

class VCardForm(KeyserverForm):
    def __init__(self, on_text_changed, *args, **kwargs):
        super(VCardForm, self).__init__(*args, **kwargs)
        vcard_grid = QGridLayout()

        msg = _('Name of contact.')
        description_label = HelpLabel(_('&Name'), msg)
        vcard_grid.addWidget(description_label, 0, 0)
        self.upload_vName_e = QLineEdit()
        self.upload_vName_e.textChanged.connect(on_text_changed)
        description_label.setBuddy(self.upload_vName_e)
        vcard_grid.addWidget(self.upload_vName_e, 0, 1, 1, -1)

        msg = _('Mobile number of contact.')
        description_label = HelpLabel(_('&Mobile'), msg)
        vcard_grid.addWidget(description_label, 1, 0)
        self.upload_vMobile_e = QLineEdit()
        self.upload_vMobile_e.textChanged.connect(on_text_changed)
        description_label.setBuddy(self.upload_vMobile_e)
        vcard_grid.addWidget(self.upload_vMobile_e, 1, 1, 1, -1)

        msg = _('Email of contact.')
        description_label = HelpLabel(_('&Email'), msg)
        vcard_grid.addWidget(description_label, 2, 0)
        self.upload_vEmail_e = QLineEdit()
        self.upload_vEmail_e.textChanged.connect(on_text_changed)
        description_label.setBuddy(self.upload_vEmail_e)
        vcard_grid.addWidget(self.upload_vEmail_e, 2, 1, 1, -1)

        self.setLayout(vcard_grid)

    def is_full(self):
        # Name is required
        return bool(self.upload_vName_e.text())

    def clear(self):
        self.upload_vName_e.clear()
        self.upload_vMobile_e.clear()
        self.upload_vEmail_e.clear()

    def _get_ttl(self):
        return 60*60

    def _get_data(self):
        card = {
            "name": self.upload_vName_e.text(),
            "mobile": self.upload_vMobile_e.text(),
            "email": self.upload_vEmail_e.text()
        }
        return card

    def _construct_metadata(self, addr, card, signer, ttl):
        return vcard_metadata(addr, card, signer, ttl)
