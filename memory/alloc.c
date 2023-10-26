#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>


struct obj_metadata {
    size_t size;
    struct obj_metadata *next;
    struct obj_metadata *prev;
    int is_free;
};

struct obj_metadata *fir; 
struct obj_metadata *recently_freed_slot; 


size_t get_size(size_t size)
{
    size_t total_size = 8;
    if(size < 8) return total_size;
    else if(size % 8 != 0)
    {
        total_size = size - (size % 8) + total_size;
        return total_size;
    } 
    else return size;
}

void* init_extra_header(void* prev_header)
{
    struct obj_metadata *header;
    void *block;
    block = sbrk(sizeof(struct obj_metadata));
    header = (struct obj_metadata *)block;
    header->size = 0;
    header->prev = (struct obj_metadata *)prev_header;
    header->next = NULL;
    header->is_free = 1;
    return header;
}

void ini_headers(size_t size)
{
    void *block;
    block = sbrk(sizeof(struct obj_metadata) + get_size(size));
    fir = (struct obj_metadata *)block;
    fir->size = get_size(size);
    fir->next = (struct obj_metadata *) init_extra_header(fir);
    fir->prev = NULL;
    fir->is_free = 1;
}

void* split(void* ptr, size_t size)
{
    struct obj_metadata *header = (struct obj_metadata*) (ptr - sizeof(struct obj_metadata)); 
    struct obj_metadata *new_header = (struct obj_metadata *)(ptr + size);

    new_header->next = header->next;
    new_header->size = header->size - size - sizeof(struct obj_metadata);
    new_header->prev = header;
    new_header->is_free = 1;

    header->next = new_header;
    header->size = size;
    header->is_free = 0;

    return header;
}

int is_splittable(void* ptr, size_t size)
{
    struct obj_metadata *header = (struct obj_metadata *)ptr;
    long int remaining_space = (long int)(header->size - size - sizeof(struct obj_metadata));
    if(remaining_space >= 8) return 1;   
    return -1;                            
}  

void* find_space(size_t size)
{
    if(!fir) ini_headers(size); 
    struct obj_metadata *header = fir;
    while(1)
    {
        if(header->size >= size && header->is_free == 1) 
        {
            
            if(header->size >= size && is_splittable(header, size) == -1) { //Dont forget this
                header->is_free = 0;
                return header + 1;
            }
            if(is_splittable(header, size) == 1) {
                header = (struct obj_metadata *) split(header + 1, size);
                return header + 1;
            }
        }
        else if (header->next->size != 0) header = header->next;
        else if (header->next->size == 0) {
            sbrk(get_size(size));
            header->next->next= (struct obj_metadata*) init_extra_header(header->next);
            header->next->size = get_size(size);
            header = header->next;
        }
    }
}

void* check_recently_freed_slot(size_t size)
{
    if(recently_freed_slot->size >= size) 
    {
        if(is_splittable(recently_freed_slot, size) == -1) { //Dont forget this
            recently_freed_slot->is_free = 0;
            return recently_freed_slot + 1;
        }
        if(is_splittable(recently_freed_slot, size) == 1) {
            recently_freed_slot = (struct obj_metadata *) split(recently_freed_slot + 1, size);
            return recently_freed_slot + 1;
        }
    }
    return(void*)-1;
}


void *mymalloc(size_t size)
{   
    if(recently_freed_slot)
    {
        void* memory_pointer = check_recently_freed_slot(get_size(size));
        if(memory_pointer != (void*)-1) return memory_pointer;
    }
    return find_space(get_size(size));
}

void *mycalloc(size_t nmemb, size_t size)
{
    void* block;
    int total_size = nmemb * size;
	block = mymalloc(total_size);
	return memset(block, 0, total_size);
}

void *forward_merge(void *ptr)
{
    struct obj_metadata *header = (struct obj_metadata*) (ptr - sizeof(struct obj_metadata)); 
    if(header->next->is_free == 1 && header->next->size != 0)
    {
        header->size = header->size + header->next->size + sizeof(struct obj_metadata);
        header->next->next->prev = header;
        header->next = header->next->next;
    }
    return header;
}

void *backword_merge(void *ptr)
{
    struct obj_metadata *header = (struct obj_metadata*) ptr; 
    if(header->prev)
    {
        if(header->prev->is_free == 1)
        {
            header->prev->next = header->next;
            header->next->prev = header->prev;
            header->prev->size = header->prev->size + header->size + sizeof(struct obj_metadata);
            header = header->prev;
        }
    }
    return header;
}


void myfree(void *ptr)
{
    if(ptr)
    {
        struct obj_metadata *header = (struct obj_metadata *)forward_merge(ptr); 
        header = (struct obj_metadata *) backword_merge(header);
        header->is_free = 1;
    }
}

void *myrealloc(void *ptr, size_t size)
{
    struct obj_metadata *header = (struct obj_metadata*) (ptr - sizeof(struct obj_metadata)); 
    if(!ptr) return mymalloc(get_size(size));
    if(get_size(size) > header->size)
    {
        void *new_header = mymalloc(get_size(size));
        memcpy(new_header, ptr, header->size);
        myfree(ptr);
        return new_header;
    }
    return ptr;
}


/*
 * Enable the code below to enable system allocator support for your allocator.
 * Doing so will make debugging much harder (e.g., using printf may result in
 * infinite loops).
 */
#if 1
void *malloc(size_t size) { return mymalloc(size); }
void *calloc(size_t nmemb, size_t size) { return mycalloc(nmemb, size); }
void *realloc(void *ptr, size_t size) { return myrealloc(ptr, size); }
void free(void *ptr) { myfree(ptr); }
#endif
