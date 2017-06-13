###
# Copyright (c) 2017, Bogdan Ilisei
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Wowalert')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

import requests
from bs4 import BeautifulSoup as bs

class Wowalert(callbacks.Plugin):
    """Retrieves World of Warcraft region alerts."""
    threaded = True

    def wowalert(self, irc, msg, args, opts):
        """[--eu] [--us]
        Retrieves WoW region alerts.
        """

        show_us = True
        show_eu = True
        eu_force = False
        us_force = False
       
        if opts:
            show_eu = False
            show_us = False
            for (option, arg) in opts:
                if option == 'eu' and arg:
                    eu_force = True
                    show_eu = True
                
                if option == 'us' and arg:
                    us_force = True
                    show_us = True

        us_url = 'http://launcher.worldofwarcraft.com/alert'
        eu_url = 'http://status.wow-europe.com/en/alert'

        eu_result = ''
        if show_eu:
            try:
                eu_r = requests.get(eu_url)
            except:
                irc.reply(format('%s: error retrieving EU data', ircutils.bold('WoW Alert')))

            if eu_r.content:
                eu = bs(eu_r.content)
                try:
                    eu_result = eu.p.next_sibling.contents[0]
                except:
                    eu_result = 'error'
            else:
                if eu_force:
                    eu_result = 'Empty'
                    
            if eu_result:
                irc.reply(format('%s: %s', ircutils.bold('EU'), eu_result))

        us_result = ''
        if show_us:
            try:
                us_r = requests.get(us_url)
            except:
                irc.reply(format('%s: error retrieving US data', ircutils.bold('WoW Alert')))

            if us_r.content:
                us = bs(us_r.content)
                try:
                    us_result = us.p.next_sibling.contents[0]
                except:
                    us_result = 'error'
            else:
                if us_force: 
                    us_result = 'Empty'

            if us_result:
                irc.reply(format('%s: %s', ircutils.bold('US'), us_result))
        
        if not eu_force and not us_force and not us_result and not eu_result:
            irc.reply(format('%s: no alerts', ircutils.bold('WoW Alert')))

    wowalert = wrap(wowalert, [getopts({'eu': '', 'us': ''})])

Class = Wowalert

# vim:set shiftwidth=4 softtabstop=4 expandtab:
