from openai import OpenAI


# this comes from train 0374
prompt = """### Instruction:
You are a code completion assistant and your task is to analyze user edits and then rewrite an excerpt that the user provides, suggesting the appropriate edits within the excerpt, taking into account the cursor location.

### User Edits:

User edited "external/libogg/src/bitwise.c":
```diff
index 563f989..1090dc2 100644
--- a/src/bitwise.c
+++ b/src/bitwise.c
@@ -60,7 +60,7 @@ void oggpack_writetrunc(oggpack_buffer *b,long bits){
 
   if(b->ptr){
     bits-=bytes*8;
-    b->ptr=b->buffer
+    b->ptr=b->buffer+bytes;
     b->endbit=bits;
     b->endbyte=bytes;
     *b->ptr&=mask[bits];
```
### User Excerpt:

```external/libogg/src/bitwise.c
#include <string.h>
#include <stdlib.h>
#include <ogg/ogg.h>

#define BUFFER_INCREMENT 256

static const unsigned long mask[]=
{0x00000000,0x00000001,0x00000003,0x00000007,0x0000000f,
 0x0000001f,0x0000003f,0x0000007f,0x000000ff,0x000001ff,
 0x000003ff,0x000007ff,0x00000fff,0x00001fff,0x00003fff,
 0x00007fff,0x0000ffff,0x0001ffff,0x0003ffff,0x0007ffff,
 0x000fffff,0x001fffff,0x003fffff,0x007fffff,0x00ffffff,
 0x01ffffff,0x03ffffff,0x07ffffff,0x0fffffff,0x1fffffff,
 0x3fffffff,0x7fffffff,0xffffffff };

static const unsigned int mask8B[]=
{0x00,0x80,0xc0,0xe0,0xf0,0xf8,0xfc,0xfe,0xff};

void oggpack_writeinit(oggpack_buffer *b){
  memset(b,0,sizeof(*b));
  b->ptr=b->buffer=_ogg_malloc(BUFFER_INCREMENT);
  b->buffer[0]='\0';
  b->storage=BUFFER_INCREMENT;
}

void oggpackB_writeinit(oggpack_buffer *b){
  oggpack_writeinit(b);
}

int oggpack_writecheck(oggpack_buffer *b){
  if(!b->ptr || !b->storage)return -1;
  return 0;
}

int oggpackB_writecheck(oggpack_buffer *b){
  return oggpack_writecheck(b);
}
<|editable_region_start|>
void oggpack_writetrunc(oggpack_buffer *b,long bits){
  long
  if(b->ptr){
    bits-=bytes*8;   
    b->ptr=b->buffer+bytes;
    b->endbit=bits;
    b->endbyte=bytes;
    *b->ptr&=mask[bits];
  }
}
<|editable_region_end|>
void oggpackB_writetrunc(oggpack_buffer *b,long bits){
  long bytes=bits>>3;
  if(b->ptr){
    bits-=bytes*8;
    b->ptr=b->buffer+bytes;
    b->endbit=bits;
    b->endbyte=bytes;
    *b->ptr&=mask8B[bits];
  }
}
```

### Response:
"""


# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
completion_response = client.completions.create(model="zeta",
                                                  prompt=prompt,
                                                  max_tokens=2048,
                                                  temperature=0,
                                                  stop="<|editable_region_end|>")
print(completion_response.choices[0].text)
