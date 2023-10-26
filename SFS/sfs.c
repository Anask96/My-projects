#define FUSE_USE_VERSION 26

#include <errno.h>
#include <fuse.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <assert.h>

#include "sfs.h"
#include "diskio.h"


static const char default_img[] = "test.img";

/* Options passed from commandline arguments */
struct options {
    const char *img;
    int background;
    int verbose;
    int show_help;
    int show_fuse_help;
} options;


#define log(fmt, ...) \
    do { \
        if (options.verbose) \
            printf(" # " fmt, ##__VA_ARGS__); \
    } while (0)


/* libfuse2 leaks, so let's shush LeakSanitizer if we are using Asan. */
const char* __asan_default_options() { return "detect_leaks=0"; }


/*
 * This is a helper function that is optional, but highly recomended you
 * implement and use. Given a path, it looks it up on disk. It will return 0 on
 * success, and a non-zero value on error (e.g., the file did not exist).
 * The resulting directory entry is placed in the memory pointed to by
 * ret_entry. Additionally it can return the offset of that direntry on disk in
 * ret_entry_off, which you can use to update the entry and write it back to
 * disk (e.g., rmdir, unlink, truncate, write).
 *
 * You can start with implementing this function to work just for paths in the
 * root entry, and later modify it to also work for paths with subdirectories.
 * This way, all of your other functions can use this helper and will
 * automatically support subdirectories. To make this function support
 * subdirectories, we recommend you refactor this function to be recursive, and
 * take the current directory as argument as well. For example:
 *
 *  static int get_entry_rec(const char *path, const struct sfs_entry *parent,
 *                           size_t parent_nentries, blockidx_t parent_blockidx,
 *                           struct sfs_entry *ret_entry,
 *                           unsigned *ret_entry_off)
 *
 * Here parent is the directory it is currently searching (at first the rootdir,
 * later the subdir). The parent_nentries tells the function how many entries
 * there are in the directory (SFS_ROOTDIR_NENTRIES or SFS_DIR_NENTRIES).
 * Finally, the parent_blockidx contains the blockidx of the given directory on
 * the disk, which will help in calculating ret_entry_off.
 */


static int get_entry(const char *path, struct sfs_entry *ret_entry,
                     unsigned *ret_entry_off, unsigned current_dir_off,
                     size_t current_dir_size, int get_path, int recursion) //if recursion is 0 get_entry will check if the entry is inside a given dir
{
    unsigned entries;

    if(current_dir_size / 64 == 64) entries = SFS_ROOTDIR_NENTRIES;
    else entries = SFS_DIR_NENTRIES;
    int res = -2;

    const char* token;
    if(get_path == 1) token = strtok((char *)path,"/");
    else token = path;

    struct sfs_entry rootdir [entries]; 
    disk_read(rootdir, current_dir_size, current_dir_off);  

    for(unsigned i=0; i < entries; i++) {       
        if(strcmp(rootdir[i].filename, token) == 0) {
            const char* token2 = token;          
            if(recursion == 1) token2 = strtok(NULL,"/");              
            if(token2 != NULL && token2 != token) {
                res = get_entry(token2, ret_entry, ret_entry_off, rootdir[i].first_block*SFS_BLOCK_SIZE+SFS_DATA_OFF, SFS_DIR_SIZE, 0, 1); 
            }
            else {
                for(unsigned j = 0; j < SFS_FILENAME_MAX; j++)
                    ret_entry->filename[j] = rootdir[i].filename[j];

                ret_entry->first_block = rootdir[i].first_block;
                ret_entry->size = rootdir[i].size;
                *ret_entry_off = current_dir_off + i;
                res = 0;
            }
        }
    }   
    
    /* Get the next component of the path. Make sure to not modify path if it is
     * the value passed by libfuse (i.e., make a copy). Note that strtok
     * modifies the string you pass it. */

    /* Allocate memory for the rootdir (and later, subdir) and read it from disk */

    /* Loop over all entries in the directory, looking for one with the name
     * equal to the current part of the path. If it is the last part of the
     * path, return it. If there are more parts remaining, recurse to handle
     * that subdirectory. */

    return res;
}


/*
 * Retrieve information about a file or directory.
 * You should populate fields of `stbuf` with appropriate information if the
 * file exists and is accessible, or return an error otherwise.
 *
 * For directories, you should at least set st_mode (with S_IFDIR) and st_nlink.
 * For files, you should at least set st_mode (with S_IFREG), st_nlink and
 * st_size.
 *
 * Return 0 on success, < 0 on error.
 */
static int sfs_getattr(const char *path,
                       struct stat *st)
{
    int res = 0;

    log("getattr %s\n", path);

    memset(st, 0, sizeof(struct stat));
    /* Set owner to user/group who mounted the image */
    st->st_uid = getuid();
    st->st_gid = getgid();
    /* Last accessed/modified just now */
    st->st_atime = time(NULL);
    st->st_mtime = time(NULL);

    if (strcmp(path, "/") == 0) {
        st->st_mode = S_IFDIR | 0755;
        st->st_nlink = 2;
    } else {
        struct sfs_entry ret_entry;
        unsigned ret_entry_off;
        res = get_entry(path, &ret_entry, &ret_entry_off, SFS_ROOTDIR_OFF, SFS_ROOTDIR_SIZE, 1, 1);
        if(res == 0) {
            if(ret_entry.size & SFS_DIRECTORY) {
                st->st_mode = S_IFDIR | 0755;
                st->st_nlink = 2; 
            } else {
                st->st_mode = S_IFREG | 0755;
                st->st_nlink = 1; 
                st->st_size = ret_entry.size & SFS_SIZEMASK;
            }
        }
    }

    return res;
}


/*
 * Return directory contents for `path`. This function should simply fill the
 * filenames - any additional information (e.g., whether something is a file or
 * directory) is later retrieved through getattr calls.
 * Use the function `filler` to add an entry to the directory. Use it like:
 *  filler(buf, <dirname>, NULL, 0);
 * Return 0 on success, < 0 on error.
 */
static int sfs_readdir(const char *path,
                       void *buf,
                       fuse_fill_dir_t filler,
                       off_t offset,
                       struct fuse_file_info *fi)
{
    (void)offset, (void)fi;
    log("readdir %s\n", path);

    (void)filler; /* Placeholder - use me */
    (void)buf; /* Placeholder - use me */

    unsigned entries = SFS_DIR_NENTRIES;
    unsigned size = SFS_DIR_SIZE;;
    unsigned dirOffset;

    if(strcmp(path, "/") == 0){
        entries = SFS_ROOTDIR_NENTRIES;
        size = SFS_ROOTDIR_SIZE;
        dirOffset = SFS_ROOTDIR_OFF;

    } else {
        struct sfs_entry ret_entry;
        unsigned ret_entry_off;
        get_entry(path, &ret_entry, &ret_entry_off, SFS_ROOTDIR_OFF, SFS_ROOTDIR_SIZE, 1, 1);
        dirOffset = ret_entry.first_block*SFS_BLOCK_SIZE+SFS_DATA_OFF;
    }


    struct sfs_entry rootdir [entries];
    disk_read(rootdir, size, dirOffset);

    for(unsigned i=0; i < entries; i++) {
        if(strlen(rootdir[i].filename) > 0) {
            filler(buf, rootdir[i].filename, NULL, 0);
        }
    }
    return 0;
}


/*
 * Read contents of `path` into `buf` for  up to `size` bytes.
 * Note that `size` may be bigger than the file actually is.
 * Reading should start at offset `offset`; the OS will generally read your file
 * in chunks of 4K byte.
 * Returns the number of bytes read (writting into `buf`), or < 0 on error.
 */
static int sfs_read(const char *path,
                    char *buf,
                    size_t size,
                    off_t offset,
                    struct fuse_file_info *fi)
{
    (void)fi;
    log("read %s size=%zu offset=%ld\n", path, size, offset);

    (void)buf; /* Placeholder - use me */

    unsigned fileOffset;

    if(strcmp(path, "/") == 0){
        return -ENOSYS;

    } else {
        struct sfs_entry ret_entry;
        unsigned ret_entry_off;
        get_entry(path, &ret_entry, &ret_entry_off, SFS_ROOTDIR_OFF, SFS_ROOTDIR_SIZE, 1, 1); 
        fileOffset = ret_entry.first_block;
    }

    int res = 0;
    int number_of_bytes = 0;  
    number_of_bytes = size;
    blockidx_t index[2];
    int bytes;
    index[0] = fileOffset;

    while(1) {
        if(res + 512 > offset) {

            index[1] = offset - res;
            bytes = res + 512 - offset;
            number_of_bytes -= bytes;
            
            if(index[0] == SFS_BLOCKIDX_END) return 0;
            disk_read(buf, bytes, index[0]*SFS_BLOCK_SIZE + SFS_DATA_OFF + index[1]);
            disk_read(index, sizeof(blockidx_t), index[0]*sizeof(blockidx_t) + SFS_BLOCKTBL_OFF); 
            res = bytes;
            break;
        }
        disk_read(index, sizeof(blockidx_t), index[0]*sizeof(blockidx_t) + SFS_BLOCKTBL_OFF); 
        res += 512;
        if(index[0] == SFS_BLOCKIDX_END) break;
    }
    
    while(1) {
        
        if(index[0] == SFS_BLOCKIDX_END) break;
        if(number_of_bytes >= 512) bytes = SFS_BLOCK_SIZE;
        else if(number_of_bytes > 0)bytes = number_of_bytes;
        else break;
        number_of_bytes -= bytes;  

        disk_read(buf + res, bytes, index[0]*SFS_BLOCK_SIZE + SFS_DATA_OFF);
        res += bytes;
        disk_read(index, sizeof(blockidx_t), index[0]*sizeof(blockidx_t) + SFS_BLOCKTBL_OFF); 
    }

    return res;
}                                    //command to use tail mnt/README and 

/*
 * Create directory at `path`.
 * The `mode` argument describes the permissions, which you may ignore for this
 * assignment.
 * Returns 0 on success, < 0 on error.
 */
const char* get_dir_name(const char* path) {
    struct sfs_entry ret_entry;
    unsigned ret_entry_off;

    unsigned parent_size = SFS_ROOTDIR_SIZE;
    unsigned parent_off = SFS_ROOTDIR_OFF;
    int res;
    
    char *name, *rest_path;
    rest_path = (char *)path;

    name = strtok_r(rest_path, "/", &rest_path);

  
    while(name != NULL) {
        res = get_entry(name, &ret_entry, &ret_entry_off, parent_off, parent_size, 0, 0);
        if(res != -2) {
            name = strtok_r(NULL,"/", &rest_path);
            parent_off = ret_entry_off;
            parent_size = SFS_DIR_SIZE;
        }
    }

    printf("name of eew%s\n")
    // res = -2,  name is new file name, offset soon to be parent dir 

    return name;
}
static int sfs_mkdir(const char *path,
                     mode_t mode)
{
    log("mkdir %s mode=%o\n", path, mode);

    const char* name = get_dir_name(path);

    return 0;
}


/*
 * Remove directory at `path`.
 * Directories may only be removed if they are empty, otherwise this function
 * should return -ENOTEMPTY.
 * Returns 0 on success, < 0 on error.
 */
static int sfs_rmdir(const char *path)
{
    log("rmdir %s\n", path);

    return -ENOSYS;
}


/*
 * Remove file at `path`.
 * Can not be used to remove directories.
 * Returns 0 on success, < 0 on error.
 */
static int sfs_unlink(const char *path)
{
    log("unlink %s\n", path);

    return -ENOSYS;
}


/*
 * Create an empty file at `path`.
 * The `mode` argument describes the permissions, which you may ignore for this
 * assignment.
 * Returns 0 on success, < 0 on error.
 */
static int sfs_create(const char *path,
                      mode_t mode,
                      struct fuse_file_info *fi)
{
    (void)fi;
    log("create %s mode=%o\n", path, mode);

    return -ENOSYS;
}


/*
 * Shrink or grow the file at `path` to `size` bytes.
 * Excess bytes are thrown away, whereas any bytes added in the process should
 * be nil (\0).
 * Returns 0 on success, < 0 on error.
 */
static int sfs_truncate(const char *path, off_t size)
{
    log("truncate %s size=%ld\n", path, size);

    return -ENOSYS;
}


/*
 * Write contents of `buf` (of `size` bytes) to the file at `path`.
 * The file is grown if nessecary, and any bytes already present are overwritten
 * (whereas any other data is left intact). The `offset` argument specifies how
 * many bytes should be skipped in the file, after which `size` bytes from
 * buffer are written.
 * This means that the new file size will be max(old_size, offset + size).
 * Returns the number of bytes written, or < 0 on error.
 */
static int sfs_write(const char *path,
                     const char *buf,
                     size_t size,
                     off_t offset,
                     struct fuse_file_info *fi)
{
    (void)fi;
    log("write %s data='%.*s' size=%zu offset=%ld\n", path, (int)size, buf,
        size, offset);

    return -ENOSYS;
}


/*
 * Move/rename the file at `path` to `newpath`.
 * Returns 0 on succes, < 0 on error.
 */
static int sfs_rename(const char *path,
                      const char *newpath)
{
    /* Implementing this function is optional, and not worth any points. */
    log("rename %s %s\n", path, newpath);

    return -ENOSYS;
}


static const struct fuse_operations sfs_oper = {
    .getattr    = sfs_getattr,
    .readdir    = sfs_readdir,
    .read       = sfs_read,
    .mkdir      = sfs_mkdir,
    .rmdir      = sfs_rmdir,
    .unlink     = sfs_unlink,
    .create     = sfs_create,
    .truncate   = sfs_truncate,
    .write      = sfs_write,
    .rename     = sfs_rename,
};

#define OPTION(t, p)                            \
    { t, offsetof(struct options, p), 1 }
#define LOPTION(s, l, p)                        \
    OPTION(s, p),                               \
    OPTION(l, p)
static const struct fuse_opt option_spec[] = {
    LOPTION("-i %s",    "--img=%s",     img),
    LOPTION("-b",       "--background", background),
    LOPTION("-v",       "--verbose",    verbose),
    LOPTION("-h",       "--help",       show_help),
    OPTION(             "--fuse-help",  show_fuse_help),
    FUSE_OPT_END
};

static void show_help(const char *progname)
{
    printf("usage: %s mountpoint [options]\n\n", progname);
    printf("By default this FUSE runs in the foreground, and will unmount on\n"
           "exit. If something goes wrong and FUSE does not exit cleanly, use\n"
           "the following command to unmount your mountpoint:\n"
           "  $ fusermount -u <mountpoint>\n\n");
    printf("common options (use --fuse-help for all options):\n"
           "    -i, --img=FILE      filename of SFS image to mount\n"
           "                        (default: \"%s\")\n"
           "    -b, --background    run fuse in background\n"
           "    -v, --verbose       print debug information\n"
           "    -h, --help          show this summarized help\n"
           "        --fuse-help     show full FUSE help\n"
           "\n", default_img);
}

int main(int argc, char **argv)
{
    struct fuse_args args = FUSE_ARGS_INIT(argc, argv);

    options.img = strdup(default_img);

    fuse_opt_parse(&args, &options, option_spec, NULL);

    if (options.show_help) {
        show_help(argv[0]);
        return 0;
    }

    if (options.show_fuse_help) {
        assert(fuse_opt_add_arg(&args, "--help") == 0);
        args.argv[0][0] = '\0';
    }

    if (!options.background)
        assert(fuse_opt_add_arg(&args, "-f") == 0);

    disk_open_image(options.img);

    return fuse_main(args.argc, args.argv, &sfs_oper, NULL);
}

struct sfs_entry get_new_entry_and_parent(char* path, unsigned* location_off, unsigned *entries, unsigned *size, unsigned new_entry_type) {

    struct sfs_entry ret_entry;
    unsigned ret_entry_off;

    unsigned parent_size = SFS_ROOTDIR_SIZE;
    unsigned parent_off = SFS_ROOTDIR_OFF;
    
    char *name, *rest_path;
    rest_path = (char *)path;

    name = strtok_r(rest_path, "/", &rest_path);
    char *prev_name = name;


    while(name) {
        prev_name = name;
        get_entry(name, &ret_entry, &ret_entry_off, parent_off, parent_size, 0, 0);
        name = strtok_r(NULL,"/", &rest_path);
        if(name) {
            parent_off = ret_entry.first_block*SFS_BLOCK_SIZE + SFS_DATA_OFF;   //if the entry exist res sould be 0 which can be used to not have 2 enries with he same name;
            parent_size = SFS_DIR_SIZE;
        }
    }

    if(strlen(prev_name) > SFS_MAGIC_SIZE) {
        ret_entry.size = 65535;
        return ret_entry;
    }
    *location_off = parent_off;
    if(parent_off == SFS_ROOTDIR_OFF) *entries = SFS_ROOTDIR_NENTRIES;
    else *entries = SFS_DIR_NENTRIES;
    *size = parent_size;

    return create_entry(prev_name, new_entry_type);
}

static int sfs_unlink(const char *path)
{
    log("unlink %s\n", path);
    struct sfs_entry ret_entry;
    unsigned ret_entry_off;
    char* copy = strdup(path);

    get_entry(copy, &ret_entry, &ret_entry_off, SFS_ROOTDIR_OFF, SFS_ROOTDIR_SIZE, 1, 1);
    // if(ret_entry.first_block != 65534) remove_blocks(ret_entry.first_block);

    // struct sfs_entry entry;
    // entry.filename[0] = '\0';
    // entry.first_block = SFS_BLOCKIDX_EMPTY;
    // entry.size = 0;

    // disk_write(&entry, sizeof(struct sfs_entry), ret_entry_off);     

    return 0;
}