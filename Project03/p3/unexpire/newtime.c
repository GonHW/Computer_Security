#define _GNU_SOURCE
#define DEFAULT_DATE "01-01-2022 00:00:00"
#define DATE_ENV_VAR "FAKE_TIME"
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <time.h>

// Name: Hench Wu
// netID: hhw14
// RUID: 212006857
// your code for time() goes here

static time_t (*get_real_time_func())(time_t *) {
    static time_t (*real_time_func)(time_t *) = NULL;
    if (!real_time_func) {
        real_time_func = (time_t (*)(time_t *))dlsym(RTLD_NEXT, "time");
        if (!real_time_func) {
            fprintf(stderr, "Error locating the real 'time' function: %s\n", dlerror());
            exit(EXIT_FAILURE);
        }
    }
    return real_time_func;
}

time_t time(time_t *t) {
    static int fake_time_initialized = 0;
    static time_t fake_time;
    if (!fake_time_initialized) {
        const char* fake_time_str = getenv(DATE_ENV_VAR) ? getenv(DATE_ENV_VAR) : DEFAULT_DATE;
        struct tm time_info;
        if (strptime(fake_time_str, "%m-%d-%Y %H:%M:%S", &time_info) == NULL) {
            fprintf(stderr, "Failed to parse time string: %s\n", fake_time_str);
            exit(EXIT_FAILURE);
        }
        fake_time = mktime(&time_info);
        if (fake_time == (time_t)-1) {
            fprintf(stderr, "mktime conversion failed for time: %s\n", fake_time_str);
            exit(EXIT_FAILURE);
        }
        fake_time_initialized = 1;
    }

    if (fake_time_initialized == 1) {
        fake_time_initialized = 2; // Change state to use real time function in subsequent calls
        if (t) *t = fake_time;
        return fake_time;
    } else {
        time_t (*real_time)(time_t *) = get_real_time_func();
        return real_time(t);
    }
}


// #define _GNU_SOURCE
// #include <time.h>
// #include <dlfcn.h>
// #include <stdlib.h>

// time_t time(time_t *t) {
//     static time_t (*real_time)(time_t *) = NULL;
//     static int first_call = 1;
//     if (!real_time) {
//         real_time = dlsym(RTLD_NEXT, "time");
//     }
    
//     if (first_call) {
//         first_call = 0;
//         struct tm tm = {0};
//         strptime("01-01-2022", "%m-%d-%Y", &tm); // Set date to Jan 1, 2022
//         time_t fake_time = mktime(&tm);
//         if (t) *t = fake_time;
//         return fake_time;
//     } else {
//         return real_time(t);
//     }
// }