#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import asyncio
import logging
import functools

from uamqp import constants
from uamqp import authentication
from uamqp import errors
from uamqp import c_uamqp

_logger = logging.getLogger(__name__)


class CBSAsyncAuthMixin(authentication.CBSAuthMixin):

    async def create_authenticator_async(self, session):
        loop = asyncio.get_event_loop()
        self._cbs_auth  = await loop.run_in_executor(None, functools.partial(self.create_authenticator, session))
        return self._cbs_auth

    async def close_authenticator_async(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, functools.partial(self.close_authenticator))

    async def handle_token_async(self):
        loop = asyncio.get_event_loop()
        timeout = False
        in_progress = False
        auth_status = await loop.run_in_executor(None, functools.partial(self._cbs_auth.get_status))
        auth_status = constants.CBSAuthStatus(auth_status)
        if auth_status == constants.CBSAuthStatus.Failure:
            raise errors.TokenAuthFailure(*self._cbs_auth.get_failure_info())
        elif auth_status == constants.CBSAuthStatus.Expired:
            raise errors.TokenExpired("CBS Authentication Expired.")
        elif auth_status == constants.CBSAuthStatus.Timeout:
            timeout = True
        elif auth_status == constants.CBSAuthStatus.InProgress:
            in_progress = True
        elif auth_status == constants.CBSAuthStatus.RefreshRequired:
            await loop.run_in_executor(None, functools.partial(self._cbs_auth.refresh, None))
        elif auth_status == constants.CBSAuthStatus.Idle:
            await loop.run_in_executor(None, functools.partial(self._cbs_auth.authenticate))
            in_progress = True
        elif auth_status == constants.CBSAuthStatus.Ok:
            if self._refresh_token:
                try:
                    await loop.run_in_executor(None, functools.partial(self._cbs_auth.refresh, self._refresh_token))
                finally:
                    self._refresh_token = None
        else:
            raise ValueError("Invalid auth state.")
        return timeout, in_progress


class SASTokenAsync(authentication.SASTokenAuth, CBSAsyncAuthMixin):
    pass