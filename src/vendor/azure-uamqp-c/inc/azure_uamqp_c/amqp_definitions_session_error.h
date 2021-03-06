

// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

#ifndef AMQP_DEFINITIONS_SESSION_ERROR_H
#define AMQP_DEFINITIONS_SESSION_ERROR_H


#ifdef __cplusplus
#include <cstdint>
extern "C" {
#else
#include <stdint.h>
#include <stdbool.h>
#endif

#include "azure_uamqp_c/amqpvalue.h"
#include "azure_c_shared_utility/umock_c_prod.h"


    typedef const char* session_error;

    MOCKABLE_FUNCTION(, AMQP_VALUE, amqpvalue_create_session_error, session_error, value);


    #define amqpvalue_get_session_error amqpvalue_get_symbol

    #define session_error_window_violation "amqp:session:window-violation"
    #define session_error_errant_link "amqp:session:errant-link"
    #define session_error_handle_in_use "amqp:session:handle-in-use"
    #define session_error_unattached_handle "amqp:session:unattached-handle"


#ifdef __cplusplus
}
#endif

#endif /* AMQP_DEFINITIONS_SESSION_ERROR_H */
