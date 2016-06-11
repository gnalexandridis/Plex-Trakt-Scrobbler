from plugin.core.environment import translate as _
from plugin.preferences.options.core.base import SimpleOption
from plugin.preferences.options.o_sync.constants import MODE_KEYS_BY_LABEL, MODE_LABELS_BY_KEY, MODE_IDS_BY_KEY
from plugin.sync.core.enums import SyncMode

import logging

log = logging.getLogger(__name__)


class SyncWatchedOption(SimpleOption):
    key = 'sync.watched.mode'
    type = 'enum'

    choices = MODE_LABELS_BY_KEY
    default = SyncMode.Full

    group = (_('Sync'), _('Watched'))
    label = _('Mode')
    description = _(
        "Syncing mode for movie and episode watched states (applies to both automatic and manual syncs).\n"
        "\n"
        " - **Full** - Synchronize watched states with your Trakt.tv profile\n"
        " - **Pull** - Only pull watched states from your Trakt.tv profile\n"
        " - **Push** - Only push watched states to your Trakt.tv profile\n"
        " - **Fast Pull** - Only pull changes to watched states from your Trakt.tv profile\n"
        " - **Disabled** - Completely disable syncing of watched states"
    )
    order = 200

    preference = 'sync_watched'

    def on_database_changed(self, value, account=None):
        if value not in MODE_IDS_BY_KEY:
            log.warn('Unknown value: %r', value)
            return

        # Map `value` to plex preference
        value = MODE_IDS_BY_KEY[value]

        # Update preference
        return self._update_preference(value, account)

    def on_plex_changed(self, value, account=None):
        if value not in MODE_KEYS_BY_LABEL:
            log.warn('Unknown value: %r', value)
            return

        # Map plex `value`
        value = MODE_KEYS_BY_LABEL[value]

        # Update database
        self.update(value, account, emit=False)
        return value
