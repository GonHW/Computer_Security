#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <dlfcn.h>
#include <string.h>

// Name: Hench Wu
// netID: hhw14
// RUID: 212006857
// your code for readdir goes here


struct dirent *readdir(DIR *dirp) { 
    static struct dirent *(*original_readdir)(DIR *dirp) = NULL; 
    struct dirent *entry; 
    if(!original_readdir){
        original_readdir = (struct dirent *(*)(DIR *))dlsym(RTLD_NEXT, "readdir");
        if (!original_readdir) {
            fprintf(stderr, "Failed to find original readdir function.\n");
            exit(EXIT_FAILURE);
        }
    }

    while ((entry = original_readdir(dirp)) && strstr(getenv("HIDDEN") ?: "", entry->d_name)); 
    return entry; 
}