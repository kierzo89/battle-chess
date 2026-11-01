/* Minimum fields justified by consumer strides and checked byte counts.
   This deliberately omits unexplained bytes and does not claim the original type. */
struct partial_graphics_workspace {
    unsigned char slot_storage[4][3256];
    unsigned char translated[3248];
    unsigned char redraw[3248];
    unsigned char background[32000];
};
struct partial_graphics_workspace far graphics_workspace = { 0 };
unsigned partial_workspace_size = sizeof(struct partial_graphics_workspace);
unsigned minimum_text_storage = 32000;
