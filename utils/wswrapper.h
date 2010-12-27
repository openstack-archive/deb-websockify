/*
 * wswrap/wswrapper: Add WebSockets support to any service.
 * Copyright 2010 Joel Martin
 * Licensed under LGPL version 3 (see docs/LICENSE.LGPL-3)
 *
 * wswrapper.so is meant to be LD preloaded. Use wswrap to run a program using
 * wswrapper.so.
 */

//#define DO_DEBUG 1
//#define DO_TRACE 1

#ifdef DO_DEBUG
#define DEBUG(...) \
    if (DO_DEBUG) { \
        fprintf(stderr, "wswrapper: "); \
        fprintf(stderr, __VA_ARGS__); \
    }
#else
#define DEBUG(...)
#endif

#ifdef DO_TRACE
#define TRACE(...) \
    if (DO_TRACE) { \
        fprintf(stderr, "wswrapper: "); \
        fprintf(stderr, __VA_ARGS__); \
    }
#else
#define TRACE(...)
#endif

#define MSG(...) \
    fprintf(stderr, "wswrapper: "); \
    fprintf(stderr, __VA_ARGS__);

#define RET_ERROR(eno, ...) \
    fprintf(stderr, "wswrapper error: "); \
    fprintf(stderr, __VA_ARGS__); \
    errno = eno; \
    return -1;


const char _WS_response[] = "\
HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
%sWebSocket-Origin: %s\r\n\
%sWebSocket-Location: %s://%s%s\r\n\
%sWebSocket-Protocol: sample\r\n\
\r\n%s";

#define WS_BUFSIZE 65536
#define WS_MAX_FDS 1024

/* Buffers and state for each wrapped WebSocket connection */
typedef struct {
    char rbuf[WS_BUFSIZE];
    char sbuf[WS_BUFSIZE];
    int  rcarry_cnt;
    char rcarry[3];
    int  newframe;
} _WS_connection;


